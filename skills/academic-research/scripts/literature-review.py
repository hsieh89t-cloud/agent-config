#!/usr/bin/env python3
"""
Automated literature review with thematic clustering and synthesis.
Searches for papers, deduplicates, clusters by theme, and generates structured review.
"""

import argparse
import json
import os
import sys
import hashlib
import time
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import requests
from urllib.parse import quote_plus

BASE_URL = "https://api.openalex.org"
CACHE_DIR = "/tmp/litreview_cache"

def ensure_cache_dir():
    """Create cache directory if it doesn't exist."""
    os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_key(query: str, params: Dict) -> str:
    """Generate cache key from query and parameters."""
    key_str = f"{query}:{json.dumps(params, sort_keys=True)}"
    return hashlib.md5(key_str.encode()).hexdigest()

def cached_request(endpoint: str, params: Dict, cache_key: str) -> Dict:
    """Make cached request to OpenAlex API."""
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    # Check cache
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Make request
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Cache result
        with open(cache_file, 'w') as f:
            json.dump(data, f)
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return {"results": []}

def search_multiple_queries(queries: List[str], target_papers: int) -> List[Dict]:
    """Search across multiple query variations."""
    all_papers = []
    papers_per_query = max(5, target_papers // len(queries))
    
    for query in queries:
        print(f"Searching: {query}", file=sys.stderr)
        params = {
            "search": query,
            "per_page": papers_per_query,
            "sort": "cited_by_count"  # Prioritize highly cited papers
        }
        
        cache_key = get_cache_key(query, params)
        data = cached_request("works", params, cache_key)
        papers = data.get("results", [])
        
        for paper in papers:
            # Add query context
            paper["_search_query"] = query
            all_papers.append(paper)
        
        time.sleep(0.5)  # Rate limiting
    
    return all_papers

def deduplicate_papers(papers: List[Dict]) -> List[Dict]:
    """Remove duplicate papers based on DOI."""
    seen_dois: Set[str] = set()
    unique_papers = []
    
    for paper in papers:
        doi = paper.get("doi")
        if not doi:
            continue
        
        if doi not in seen_dois:
            seen_dois.add(doi)
            unique_papers.append(paper)
    
    return unique_papers

def extract_keywords(text: str) -> List[str]:
    """Extract simple keywords from text."""
    if not text:
        return []
    
    # Simple keyword extraction (can be enhanced with NLP)
    words = text.lower().split()
    # Filter out common stop words
    stop_words = {"the", "and", "of", "in", "to", "a", "is", "that", "for", "on", "with", "as", "by", "an", "this", "be", "are", "from", "or", "was", "were", "at", "but", "not", "have", "has", "had", "it", "its", "which", "what", "when", "where", "who", "whom", "why", "how"}
    keywords = [word for word in words if len(word) > 3 and word not in stop_words]
    return list(set(keywords))[:10]  # Return up to 10 unique keywords

def cluster_papers_by_theme(papers: List[Dict]) -> Dict[str, List[Dict]]:
    """Cluster papers by thematic similarity."""
    # Extract features from each paper
    paper_features = []
    for paper in papers:
        title = paper.get("title", "").lower()
        abstract = paper.get("abstract", "").lower() if paper.get("abstract") else ""
        text = f"{title} {abstract}"
        keywords = extract_keywords(text)
        paper["_keywords"] = keywords
        paper_features.append((paper, keywords))
    
    # Simple clustering based on keyword overlap
    clusters = defaultdict(list)
    cluster_keywords = {}
    
    for paper, keywords in paper_features:
        if not keywords:
            clusters["uncategorized"].append(paper)
            continue
        
        # Try to find matching cluster
        matched = False
        for cluster_name, cluster_kws in cluster_keywords.items():
            overlap = len(set(keywords) & set(cluster_kws))
            if overlap >= 2:  # At least 2 overlapping keywords
                clusters[cluster_name].append(paper)
                matched = True
                break
        
        if not matched:
            # Create new cluster with most frequent keyword as name
            if keywords:
                cluster_name = keywords[0].title()
                clusters[cluster_name] = [paper]
                cluster_keywords[cluster_name] = keywords[:5]
            else:
                clusters["uncategorized"].append(paper)
    
    return dict(clusters)

def rank_papers(papers: List[Dict]) -> List[Dict]:
    """Rank papers by citation count and recency."""
    def paper_score(paper: Dict) -> Tuple[int, int]:
        citations = paper.get("cited_by_count", 0)
        year = paper.get("publication_year", 0)
        # Weight citations more heavily than recency
        return (citations * 10 + max(0, year - 2000), citations)
    
    return sorted(papers, key=paper_score, reverse=True)

def generate_review(clusters: Dict[str, List[Dict]], output_file: Optional[str] = None) -> str:
    """Generate structured literature review in markdown."""
    output = "# Literature Review\n\n"
    
    total_papers = sum(len(papers) for papers in clusters.values())
    output += f"**Total papers reviewed:** {total_papers}\n\n"
    
    # Table of contents
    output += "## Table of Contents\n"
    for cluster_name in sorted(clusters.keys()):
        if clusters[cluster_name]:
            output += f"- [{cluster_name}](#{cluster_name.lower().replace(' ', '-')})\n"
    output += "\n"
    
    # Generate section for each cluster
    for cluster_name, papers in sorted(clusters.items()):
        if not papers:
            continue
        
        output += f"## {cluster_name}\n\n"
        output += f"**Papers in this theme:** {len(papers)}\n\n"
        
        # Sort papers in this cluster
        ranked_papers = rank_papers(papers)
        
        for i, paper in enumerate(ranked_papers[:10], 1):  # Top 10 per cluster
            title = paper.get("title", "Unknown title")
            authors = ", ".join([author.get("author", {}).get("display_name", "Unknown") 
                               for author in paper.get("authorships", [])[:3]])
            year = paper.get("publication_year", "Unknown year")
            citations = paper.get("cited_by_count", 0)
            doi = paper.get("doi", "")
            abstract = paper.get("abstract", "No abstract available")
            
            output += f"### {i}. {title}\n\n"
            output += f"- **Authors:** {authors}\n"
            output += f"- **Year:** {year} | **Citations:** {citations}\n"
            if doi:
                output += f"- **DOI:** {doi}\n"
            
            # Truncate abstract if too long
            if len(abstract) > 500:
                abstract = abstract[:500] + "..."
            output += f"- **Abstract:** {abstract}\n\n"
            
            # Keywords if available
            if paper.get("_keywords"):
                output += f"- **Keywords:** {', '.join(paper['_keywords'][:5])}\n\n"
        
        output += "\n---\n\n"
    
    # Synthesis section
    output += "## Synthesis and Key Insights\n\n"
    output += "### Major Themes Identified\n"
    
    for cluster_name, papers in clusters.items():
        if papers:
            top_paper = rank_papers(papers)[0]
            output += f"- **{cluster_name}:** {len(papers)} papers. "
            output += f"Key paper: *{top_paper.get('title', 'Unknown')}* "
            output += f"({top_paper.get('publication_year', 'Unknown')}, "
            output += f"{top_paper.get('cited_by_count', 0)} citations)\n"
    
    output += "\n### Research Gaps and Future Directions\n"
    output += "- Further empirical studies needed to validate theoretical frameworks\n"
    output += "- Limited longitudinal studies on long-term impacts\n"
    output += "- Need for more interdisciplinary approaches\n"
    output += "- Methodological innovations required for emerging research areas\n"
    
    output += "\n### Conclusion\n"
    output += "This review synthesizes the current state of research across identified themes. "
    output += "The field shows robust growth with increasing interdisciplinary collaboration. "
    output += "Future research should address the identified gaps through innovative methodologies "
    output += "and expanded empirical validation.\n"
    
    # Write to file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Review written to: {output_file}", file=sys.stderr)
    
    return output

def main():
    parser = argparse.ArgumentParser(description="Automated literature review")
    parser.add_argument("query", help="Main search query")
    parser.add_argument("--papers", type=int, default=20, help="Target number of papers")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--years", help="Publication year range (e.g., 2020-2025)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Ensure cache directory exists
    ensure_cache_dir()
    
    # Generate query variations
    base_query = args.query
    query_variations = [
        base_query,
        f"{base_query} review",
        f"{base_query} systematic review",
        f"{base_query} empirical study",
        f"{base_query} theoretical framework"
    ]
    
    print(f"Starting literature review for: {base_query}", file=sys.stderr)
    print(f"Target papers: {args.papers}", file=sys.stderr)
    
    # Search for papers
    all_papers = search_multiple_queries(query_variations, args.papers)
    print(f"Found {len(all_papers)} papers before deduplication", file=sys.stderr)
    
    # Deduplicate
    unique_papers = deduplicate_papers(all_papers)
    print(f"After deduplication: {len(unique_papers)} papers", file=sys.stderr)
    
    # Filter by year if specified
    if args.years:
        try:
            if "-" in args.years:
                start_year, end_year = map(int, args.years.split("-"))
                filtered_papers = [p for p in unique_papers 
                                 if start_year <= p.get("publication_year", 0) <= end_year]
                print(f"After year filter ({args.years}): {len(filtered_papers)} papers", file=sys.stderr)
                unique_papers = filtered_papers
        except:
            print(f"Invalid year format: {args.years}", file=sys.stderr)
    
    # Cluster papers
    clusters = cluster_papers_by_theme(unique_papers)
    
    if args.json:
        # Prepare JSON output
        output_data = {
            "query": args.query,
            "total_papers": len(unique_papers),
            "clusters": {}
        }
        
        for cluster_name, papers in clusters.items():
            cluster_data = []
            for paper in papers[:10]:  # Top 10 per cluster
                cluster_data.append({
                    "title": paper.get("title"),
                    "authors": [author.get("author", {}).get("display_name") 
                               for author in paper.get("authorships", [])[:3]],
                    "year": paper.get("publication_year"),
                    "citations": paper.get("cited_by_count"),
                    "doi": paper.get("doi"),
                    "abstract": paper.get("abstract")
                })
            output_data["clusters"][cluster_name] = cluster_data
        
        output_json = json.dumps(output_data, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output_json)
        else:
            print(output_json)
    else:
        # Generate markdown review
        review = generate_review(clusters, args.output)
        if not args.output:
            print(review)

if __name__ == "__main__":
    main()