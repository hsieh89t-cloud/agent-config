#!/usr/bin/env python3
"""
Context Cleanup Audit Script

This script analyzes OpenClaw workspace and state directory to identify
context bloat sources. It produces a JSON report with recommendations.

Safety: This script only reads metadata and counts characters - no deletions.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

def count_file_chars(filepath: Path) -> int:
    """Count characters in a file."""
    try:
        return filepath.stat().st_size
    except (OSError, IOError):
        return 0

def analyze_workspace_files(workspace_dir: Path) -> Dict[str, Any]:
    """Analyze workspace context files for bloat."""
    results = {
        "workspace_files": [],
        "total_chars": 0,
        "largest_files": []
    }
    
    # Core context files to check
    core_files = [
        "AGENTS.md", "SOUL.md", "IDENTITY.md", "USER.md",
        "TOOLS.md", "MEMORY.md", "HEARTBEAT.md"
    ]
    
    for filename in core_files:
        filepath = workspace_dir / filename
        if filepath.exists():
            char_count = count_file_chars(filepath)
            results["workspace_files"].append({
                "name": filename,
                "path": str(filepath),
                "char_count": char_count,
                "status": "WARNING" if char_count > 18000 else "OK"
            })
            results["total_chars"] += char_count
            
            if char_count > 5000:  # Consider large if >5K chars
                results["largest_files"].append({
                    "name": filename,
                    "char_count": char_count
                })
    
    # Sort largest files
    results["largest_files"].sort(key=lambda x: x["char_count"], reverse=True)
    
    return results

def analyze_state_directory(state_dir: Path) -> Dict[str, Any]:
    """Analyze OpenClaw state directory for session bloat."""
    results = {
        "sessions": [],
        "total_sessions": 0,
        "recent_sessions": 0,
        "old_sessions": 0
    }
    
    sessions_dir = state_dir / "sessions"
    if not sessions_dir.exists():
        return results
    
    cutoff_date = datetime.now() - timedelta(days=30)
    
    for session_file in sessions_dir.glob("*.json"):
        try:
            mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
            age_days = (datetime.now() - mtime).days
            
            session_info = {
                "name": session_file.name,
                "path": str(session_file),
                "size_bytes": session_file.stat().st_size,
                "modified": mtime.isoformat(),
                "age_days": age_days,
                "status": "OLD" if age_days > 30 else "RECENT"
            }
            
            results["sessions"].append(session_info)
            results["total_sessions"] += 1
            
            if age_days > 30:
                results["old_sessions"] += 1
            else:
                results["recent_sessions"] += 1
                
        except (OSError, IOError):
            continue
    
    # Sort by size (largest first)
    results["sessions"].sort(key=lambda x: x["size_bytes"], reverse=True)
    
    return results

def generate_recommendations(workspace_analysis: Dict, state_analysis: Dict) -> List[Dict]:
    """Generate cleanup recommendations based on analysis."""
    recommendations = []
    
    # Check for large workspace files
    for file_info in workspace_analysis.get("largest_files", []):
        if file_info["char_count"] > 18000:
            recommendations.append({
                "id": f"workspace_{file_info['name']}",
                "type": "WORKSPACE_FILE",
                "severity": "HIGH",
                "description": f"{file_info['name']} is {file_info['char_count']:,} characters (approaching 20K limit)",
                "action": "Consider moving non-critical content to reference files",
                "rollback": "Restore from git history if available"
            })
        elif file_info["char_count"] > 10000:
            recommendations.append({
                "id": f"workspace_{file_info['name']}",
                "type": "WORKSPACE_FILE",
                "severity": "MEDIUM",
                "description": f"{file_info['name']} is {file_info['char_count']:,} characters",
                "action": "Review for duplication or outdated content",
                "rollback": "Manual review before deletion"
            })
    
    # Check for old sessions
    if state_analysis.get("old_sessions", 0) > 10:
        recommendations.append({
            "id": "old_sessions",
            "type": "STATE_SESSIONS",
            "severity": "MEDIUM",
            "description": f"{state_analysis['old_sessions']} sessions older than 30 days",
            "action": "Consider archiving or deleting old sessions",
            "rollback": "Backup sessions before deletion"
        })
    
    # Check total workspace size
    total_chars = workspace_analysis.get("total_chars", 0)
    if total_chars > 50000:
        recommendations.append({
            "id": "total_workspace_size",
            "type": "WORKSPACE_TOTAL",
            "severity": "HIGH",
            "description": f"Total workspace context: {total_chars:,} characters",
            "action": "Review all context files for essential content only",
            "rollback": "Incremental cleanup with backups"
        })
    
    # Add general recommendations
    recommendations.append({
        "id": "general_hygiene",
        "type": "GENERAL",
        "severity": "LOW",
        "description": "Regular context maintenance",
        "action": "Schedule monthly context review",
        "rollback": "N/A"
    })
    
    return recommendations

def main():
    parser = argparse.ArgumentParser(description="OpenClaw Context Cleanup Audit")
    parser.add_argument("--workspace", default=".", help="Workspace directory path")
    parser.add_argument("--state-dir", default=None, help="OpenClaw state directory path")
    parser.add_argument("--out", default="context-cleanup-audit.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    # Determine state directory
    if args.state_dir:
        state_dir = Path(args.state_dir)
    else:
        # Default OpenClaw state directory
        state_dir = Path.home() / ".openclaw"
    
    workspace_dir = Path(args.workspace).resolve()
    
    print(f"Analyzing workspace: {workspace_dir}")
    print(f"Analyzing state directory: {state_dir}")
    
    # Run analyses
    workspace_analysis = analyze_workspace_files(workspace_dir)
    state_analysis = analyze_state_directory(state_dir)
    
    # Generate recommendations
    recommendations = generate_recommendations(workspace_analysis, state_analysis)
    
    # Prepare final report
    report = {
        "timestamp": datetime.now().isoformat(),
        "workspace_dir": str(workspace_dir),
        "state_dir": str(state_dir),
        "workspace_analysis": workspace_analysis,
        "state_analysis": state_analysis,
        "recommendations": recommendations,
        "summary": {
            "total_recommendations": len(recommendations),
            "high_severity": len([r for r in recommendations if r["severity"] == "HIGH"]),
            "medium_severity": len([r for r in recommendations if r["severity"] == "MEDIUM"]),
            "low_severity": len([r for r in recommendations if r["severity"] == "LOW"])
        }
    }
    
    # Write JSON report
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n=== Context Cleanup Audit Report ===")
    print(f"Generated: {report['timestamp']}")
    print(f"Workspace context files: {len(workspace_analysis['workspace_files'])}")
    print(f"Total characters in workspace: {workspace_analysis['total_chars']:,}")
    
    if workspace_analysis['largest_files']:
        print(f"\nLargest workspace files:")
        for file_info in workspace_analysis['largest_files'][:3]:  # Top 3
            print(f"  - {file_info['name']}: {file_info['char_count']:,} chars")
    
    print(f"\nSessions analysis:")
    print(f"  Total sessions: {state_analysis['total_sessions']}")
    print(f"  Recent sessions (<30 days): {state_analysis['recent_sessions']}")
    print(f"  Old sessions (>30 days): {state_analysis['old_sessions']}")
    
    print(f"\nRecommendations: {len(recommendations)} total")
    for rec in recommendations:
        print(f"  [{rec['severity']}] {rec['description']}")
    
    print(f"\nFull report saved to: {args.out}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())