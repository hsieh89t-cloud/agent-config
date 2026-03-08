#!/usr/bin/env python3
"""
Academic paper search using OpenAlex API (free, no key needed).
Supports search by topic, author, DOI, and citation chains.
"""

import argparse
import json
import sys
import requests
from typing import Dict, List, Optional, Any
from urllib.parse import quote_plus
import time

BASE_URL = "https://api.openalex.org"

def make_request(endpoint: str, params: Optional[Dict] = None) -> Dict:
    """Make HTTP request to OpenAlex API with rate limiting."""
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

def search_papers(query: str, limit: int = 10, sort_by: str = "relevance_score") -> List[Dict]:
    """Search papers by topic/query."""
    params = {
        "search": query,
        "per_page": limit
    }
    # OpenAlex sorts by relevance by default
    if sort_by == "cited_by_count":
        params["sort"] = "cited_by_count:desc"
    data = make_request("works", params)
    return data.get("results", [])

def search_by_author(author_name: str, limit: int = 5) -> List[Dict]:
    """Search papers by author name."""
    params = {
        "search": author_name,
        "per_page": limit
    }
    data = make_request("works", params)
    # Filter results to include only papers by this author
    filtered = []
    for paper in data.get("results", []):
        authors = [author.get("author", {}).get("display_name", "").lower() 
                  for author in paper.get("authorships", [])]
        if any(author_name.lower() in author for author in authors):
            filtered.append(paper)
    return filtered[:limit]

def get_by_doi(doi: str) -> Optional[Dict]:
    """Get paper metadata by DOI."""
    # Remove https://doi.org/ prefix if present
    if doi.startswith("https://doi.org/"):
        doi = doi[16:]
    endpoint = f"works/https://doi.org/{doi}"
    data = make_request(endpoint)
    return data

def get_citations(doi: str, direction: str = "cited_by", limit: int = 10) -> List[Dict]:
    """Get papers that cite or are cited by a given paper."""
    if doi.startswith("https://doi.org/"):
        doi = doi[16:]
    
    paper = get_by_doi(doi)
    if not paper:
        return []
    
    if direction == "cited_by":
        endpoint = f"works/{paper['id'].split('/')[-1]}/cited_by"
    elif direction == "references":
        endpoint = f"works/{paper['id'].split('/')[-1]}/references"
    else:  # both
        # Get both citing and cited papers
        cited_by = get_citations(doi, "cited_by", limit)
        references = get_citations(doi, "references", limit)
        return cited_by + references
    
    params = {"per_page": limit}
    data = make_request(endpoint, params)
    return data.get("results", [])

def deep_read(doi: str) -> Dict:
    """Get detailed paper info including abstract and open access URL."""
    paper = get_by_doi(doi)
    if not paper:
        return {}
    
    # Try to get full text if open access
    full_text = None
    if paper.get("open_access", {}).get("is_oa", False):
        full_text = paper.get("open_access", {}).get("oa_url")
    
    return {
        "title": paper.get("title"),
        "authors": [author.get("author", {}).get("display_name") for author in paper.get("authorships", [])],
        "abstract": paper.get("abstract"),
        "citation_count": paper.get("cited_by_count"),
        "doi": paper.get("doi"),
        "open_access_url": full_text,
        "publication_year": paper.get("publication_year"),
        "journal": paper.get("host_venue", {}).get("display_name"),
        "url": paper.get("id")
    }

def format_paper(paper: Dict, detailed: bool = False) -> str:
    """Format paper information for display."""
    title = paper.get("title", "Unknown title")
    authors = ", ".join([author.get("author", {}).get("display_name", "Unknown") 
                        for author in paper.get("authorships", [])[:3]])
    year = paper.get("publication_year", "Unknown year")
    citations = paper.get("cited_by_count", 0)
    doi = paper.get("doi", "No DOI")
    
    output = f"Title: {title}\n"
    output += f"Authors: {authors}\n"
    output += f"Year: {year} | Citations: {citations}\n"
    output += f"DOI: {doi}\n"
    
    if detailed:
        abstract = paper.get("abstract", "No abstract available")
        output += f"Abstract: {abstract[:500]}...\n" if len(abstract) > 500 else f"Abstract: {abstract}\n"
        
        if paper.get("open_access", {}).get("is_oa", False):
            output += f"Open Access: {paper['open_access']['oa_url']}\n"
    
    output += "-" * 80 + "\n"
    return output

def main():
    parser = argparse.ArgumentParser(description="Search academic papers via OpenAlex")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search papers by topic")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", type=int, default=10, help="Number of results")
    search_parser.add_argument("--sort", choices=["relevance_score", "cited_by_count"], 
                             default="relevance_score", help="Sort order (relevance_score or cited_by_count)")
    search_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # Author search
    author_parser = subparsers.add_parser("author", help="Search papers by author")
    author_parser.add_argument("name", help="Author name")
    author_parser.add_argument("--limit", type=int, default=5, help="Number of results")
    author_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # DOI lookup
    doi_parser = subparsers.add_parser("doi", help="Look up paper by DOI")
    doi_parser.add_argument("doi", help="DOI of the paper")
    doi_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # Citations
    cite_parser = subparsers.add_parser("citations", help="Get citation chain")
    cite_parser.add_argument("doi", help="DOI of the paper")
    cite_parser.add_argument("--direction", choices=["cited_by", "references", "both"], 
                           default="cited_by", help="Citation direction")
    cite_parser.add_argument("--limit", type=int, default=10, help="Number of results")
    cite_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # Deep read
    deep_parser = subparsers.add_parser("deep", help="Get detailed paper info")
    deep_parser.add_argument("doi", help="DOI of the paper")
    deep_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    if args.command == "search":
        papers = search_papers(args.query, args.limit, args.sort)
        if args.json:
            print(json.dumps(papers, indent=2))
        else:
            for paper in papers:
                print(format_paper(paper))
    
    elif args.command == "author":
        papers = search_by_author(args.name, args.limit)
        if args.json:
            print(json.dumps(papers, indent=2))
        else:
            for paper in papers:
                print(format_paper(paper))
    
    elif args.command == "doi":
        paper = get_by_doi(args.doi)
        if args.json:
            print(json.dumps(paper, indent=2))
        elif paper:
            print(format_paper(paper, detailed=True))
        else:
            print(f"No paper found with DOI: {args.doi}")
    
    elif args.command == "citations":
        papers = get_citations(args.doi, args.direction, args.limit)
        if args.json:
            print(json.dumps(papers, indent=2))
        else:
            direction_str = "citing" if args.direction == "cited_by" else "cited by"
            print(f"Papers {direction_str}: {args.doi}\n")
            for paper in papers:
                print(format_paper(paper))
    
    elif args.command == "deep":
        details = deep_read(args.doi)
        if args.json:
            print(json.dumps(details, indent=2))
        else:
            if details:
                print(f"Title: {details.get('title')}")
                print(f"Authors: {', '.join(details.get('authors', []))}")
                print(f"Year: {details.get('publication_year')}")
                print(f"Citations: {details.get('citation_count')}")
                print(f"DOI: {details.get('doi')}")
                print(f"Journal: {details.get('journal')}")
                print(f"Abstract: {details.get('abstract', 'No abstract available')}")
                if details.get('open_access_url'):
                    print(f"Open Access URL: {details.get('open_access_url')}")
            else:
                print(f"No paper found with DOI: {args.doi}")

if __name__ == "__main__":
    main()