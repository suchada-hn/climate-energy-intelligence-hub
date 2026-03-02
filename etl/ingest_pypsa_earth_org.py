#!/usr/bin/env python3
"""
ETL Script: Ingest PyPSA-Earth Ecosystem
Ingests PyPSA-Earth organization repositories and ecosystem data into YAML registries.
"""
import requests
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# PyPSA-Earth ecosystem repositories
PYPSA_EARTH_REPOS = [
    'pypsa-earth', 'pypsa-distribution', 'pypsa-meets-earth', 'earth-osm',
    'powerplantmatching', 'technology-data', 'pypsa-usa', 'pypsa-earth-sec',
    'pypsa-arb', 'pypsa-eur', 'earthengine-layer', 'renewable-timeseries',
    'demand-data', 'gadm-layer', 'osm-data-extractor', 'load-data',
    'pypsa-africa', 'pypsa-europe', 'pypsa-meets-africa'
]

def fetch_github_repo_data(org: str, repo: str, token: str = None) -> Dict[str, Any]:
    """
    Fetch repository metadata from GitHub API.
    
    Args:
        org: GitHub organization name
        repo: Repository name
        token: Optional GitHub API token for higher rate limits
    
    Returns:
        Dict with repo metadata
    """
    url = f'https://api.github.com/repos/{org}/{repo}'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {
                'name': data['name'],
                'description': data['description'] or '',
                'url': data['html_url'],
                'stars': data['stargazers_count'],
                'language': data['language'],
                'license': data['license']['name'] if data.get('license') else 'unknown',
                'last_updated': data['updated_at'],
                'topics': data.get('topics', [])
            }
        else:
            print(f"\u26a0\ufe0f  Failed to fetch {org}/{repo}: {response.status_code}")
            return None
    except Exception as e:
        print(f"\u26a0\ufe0f  Error fetching {org}/{repo}: {e}")
        return None

def ingest_pypsa_earth_org(output_yaml: str, github_token: str = None):
    """
    Ingest PyPSA-Earth ecosystem repositories into YAML registry.
    
    Args:
        output_yaml: Target YAML registry file
        github_token: Optional GitHub API token
    """
    entries = []
    
    for repo_name in PYPSA_EARTH_REPOS:
        print(f"Fetching pypsa-earth/{repo_name}...")
        repo_data = fetch_github_repo_data('pypsa-earth', repo_name, github_token)
        
        if repo_data:
            entry = {
                'id': f'pypsa-earth-{repo_name}',
                'name': repo_name,
                'type': 'model' if 'pypsa' in repo_name else 'pipeline',
                'domain': 'energy-system-modeling',
                'description': repo_data['description'],
                'url': repo_data['url'],
                'repo': repo_data['url'],
                'license': repo_data['license'],
                'tags': ['pypsa-earth', 'energy-modeling'] + repo_data['topics'],
                'source': 'pypsa-earth-org',
                'metadata': {
                    'github_stars': repo_data['stars'],
                    'primary_language': repo_data['language'],
                    'ecosystem': 'pypsa-earth'
                },
                'last_updated': repo_data['last_updated'],
                'ingested_at': datetime.utcnow().isoformat() + 'Z'
            }
            entries.append(entry)
    
    # Load existing YAML or create new structure
    output_path = Path(output_yaml)
    if output_path.exists():
        with open(output_path, 'r') as f:
            existing = yaml.safe_load(f) or {'models': [], 'pipelines': []}
    else:
        existing = {'models': [], 'pipelines': []}
    
    # Categorize and merge entries
    existing_ids = {e['id'] for cat in ['models', 'pipelines'] for e in existing.get(cat, [])}
    
    new_models = [e for e in entries if e['type'] == 'model' and e['id'] not in existing_ids]
    new_pipelines = [e for e in entries if e['type'] == 'pipeline' and e['id'] not in existing_ids]
    
    if 'models' not in existing:
        existing['models'] = []
    if 'pipelines' not in existing:
        existing['pipelines'] = []
    
    existing['models'].extend(new_models)
    existing['pipelines'].extend(new_pipelines)
    
    # Write updated YAML
    with open(output_path, 'w') as f:
        yaml.dump(existing, f, default_flow_style=False, sort_keys=False)
    
    print(f"\u2705 Ingested {len(new_models)} models and {len(new_pipelines)} pipelines")
    print(f"   Total models: {len(existing['models'])}, Total pipelines: {len(existing['pipelines'])}")

if __name__ == '__main__':
    # Example usage - set GITHUB_TOKEN env var for higher rate limits
    import os
    token = os.getenv('GITHUB_TOKEN')
    
    ingest_pypsa_earth_org(
        output_yaml='data/models.yaml',
        github_token=token
    )
