"""
Generate and update the leaderboard from evaluation results.

This script reads all evaluation results and generates a leaderboard HTML page.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any
import sys


def load_all_results(results_dir: Path) -> List[Dict[str, Any]]:
    """
    Load all evaluation results from the results directory.
    
    Args:
        results_dir: Directory containing result JSON files
        
    Returns:
        List of result dictionaries
    """
    results = []
    
    if not results_dir.exists():
        return results
    
    for result_file in results_dir.glob("*.json"):
        if result_file.name == "latest_evaluation.json":
            continue  # Skip the latest evaluation file
        
        try:
            with open(result_file, 'r') as f:
                data = json.load(f)
                if data.get("success", False):
                    results.append(data)
        except Exception as e:
            print(f"Warning: Failed to load {result_file}: {e}", file=sys.stderr)
    
    return results


def calculate_combined_score(prey_score: float, predator_score: float) -> float:
    """
    Calculate a combined score from prey and predator scores.
    
    Args:
        prey_score: Average reward as prey
        predator_score: Average reward as predator
        
    Returns:
        Combined score
    """
    # Simple average - you can customize this weighting
    return (prey_score + predator_score) / 2


def generate_leaderboard_html(results: List[Dict[str, Any]], output_path: Path):
    """
    Generate HTML leaderboard page.
    
    Args:
        results: List of evaluation results
        output_path: Path to save HTML file
    """
    # Sort by combined score (descending)
    for result in results:
        result["combined_score"] = calculate_combined_score(
            result["prey_score"],
            result["predator_score"]
        )
    
    sorted_results = sorted(results, key=lambda x: x["combined_score"], reverse=True)
    
    # Generate HTML
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Tag Competition Leaderboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .leaderboard {
            padding: 40px;
        }
        
        .leaderboard h2 {
            margin-bottom: 20px;
            color: #2c3e50;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        th {
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 0.5px;
        }
        
        td {
            padding: 15px;
            border-bottom: 1px solid #dee2e6;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .rank {
            font-weight: bold;
            font-size: 1.2em;
            color: #667eea;
        }
        
        .rank-1 { color: #FFD700; }
        .rank-2 { color: #C0C0C0; }
        .rank-3 { color: #CD7F32; }
        
        .student-name {
            font-weight: 600;
            color: #2c3e50;
        }
        
        .score {
            font-weight: 600;
        }
        
        .score-positive {
            color: #28a745;
        }
        
        .score-negative {
            color: #dc3545;
        }
        
        .timestamp {
            color: #6c757d;
            font-size: 0.85em;
        }
        
        footer {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #6c757d;
            font-size: 0.9em;
        }
        
        .last-updated {
            text-align: center;
            padding: 20px;
            color: #6c757d;
            font-style: italic;
        }
        
        @media (max-width: 768px) {
            .stats {
                flex-direction: column;
                gap: 20px;
            }
            
            table {
                font-size: 0.9em;
            }
            
            th, td {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Simple Tag Competition</h1>
            <p>RL Class Leaderboard</p>
        </header>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{total_submissions}</div>
                <div class="stat-label">Total Submissions</div>
            </div>
            <div class="stat">
                <div class="stat-value">{total_students}</div>
                <div class="stat-label">Participants</div>
            </div>
            <div class="stat">
                <div class="stat-value">{total_episodes}</div>
                <div class="stat-label">Episodes Evaluated</div>
            </div>
        </div>
        
        <div class="leaderboard">
            <h2>Rankings</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Student</th>
                        <th>Combined Score</th>
                        <th>Prey Score</th>
                        <th>Predator Score</th>
                        <th>Last Submission</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add rows
    for i, result in enumerate(sorted_results, 1):
        rank_class = f"rank-{i}" if i <= 3 else "rank"
        prey_class = "score-positive" if result["prey_score"] > 0 else "score-negative"
        predator_class = "score-positive" if result["predator_score"] > 0 else "score-negative"
        
        timestamp = datetime.fromisoformat(result["timestamp"]).strftime("%Y-%m-%d %H:%M")
        
        html += f"""
                    <tr>
                        <td class="{rank_class}">#{i}</td>
                        <td class="student-name">{result['student']}</td>
                        <td class="score">{result['combined_score']:.4f}</td>
                        <td class="score {prey_class}">{result['prey_score']:.4f}</td>
                        <td class="score {predator_class}">{result['predator_score']:.4f}</td>
                        <td class="timestamp">{timestamp}</td>
                    </tr>
"""
    
    total_episodes = sum(r.get("num_episodes", 0) for r in results)
    total_students = len(set(r["student"] for r in results))
    
    html += f"""
                </tbody>
            </table>
        </div>
        
        <div class="last-updated">
            Last updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")} UTC
        </div>
        
        <footer>
            <p>Scores represent average rewards over {results[0].get('num_episodes', 0) if results else 0} episodes</p>
            <p>Combined score is the average of prey and predator scores</p>
        </footer>
    </div>
</body>
</html>
"""
    
    # Replace placeholders
    html = html.replace("{total_submissions}", str(len(results)))
    html = html.replace("{total_students}", str(total_students))
    html = html.replace("{total_episodes}", str(total_episodes))
    
    # Save HTML
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"Leaderboard generated: {output_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate leaderboard from evaluation results")
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("results"),
        help="Directory containing evaluation results"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/index.html"),
        help="Path to save leaderboard HTML"
    )
    
    args = parser.parse_args()
    
    results = load_all_results(args.results_dir)
    
    if not results:
        print("Warning: No evaluation results found", file=sys.stderr)
        # Generate empty leaderboard
        results = []
    
    generate_leaderboard_html(results, args.output)
    print(f"Successfully generated leaderboard with {len(results)} entries")


if __name__ == "__main__":
    main()
