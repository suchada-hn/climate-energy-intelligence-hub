#!/usr/bin/env python3
"""
ETL script to ingest energy-tools.csv into data/models.yaml

Usage:
  python etl/ingest_energy_tools.py path/to/energy-tools.csv
"""
import csv
import sys
import yaml
from pathlib import Path

def map_category_to_model_type(category):
    """Map energy-tools category to our model_type enum."""
    mapping = {
        'Capacity Expansion': 'capacity_expansion',
        'Production Cost': 'production_cost',
        'Power Flow': 'power_flow',
        'Optimal Power Flow': 'opf',
        'Unit Commitment': 'unit_commitment',
        'Dynamics': 'dynamics',
        'Microgrid': 'microgrid',
    }
    return mapping.get(category, 'capacity_expansion')

def ingest_energy_tools(csv_path, output_path='data/models.yaml'):
    """Read CSV and append to models.yaml."""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        entries = []
        
        for row in reader:
            # Skip if already exists
            id_slug = row['name'].lower().replace(' ', '-').replace('.', '')
            
            entry = {
                'id': id_slug,
                'name': row['name'],
                'kind': 'energy_model',
                'short_description': row.get('description', ''),
                'repo_url': row.get('repo_url', ''),
                'docs_url': row.get('docs_url', ''),
                'license': row.get('license', ''),
                'maturity': 'research',  # default
                'domain': 'power_system',  # default
                'scale': 'national',  # default
                'model_type': map_category_to_model_type(row.get('category', '')),
                'language': row.get('language', 'python').lower(),
                'collections': ['power-system-tools']
            }
            entries.append(entry)
    
    # Load existing, append, write
    existing = []
    if Path(output_path).exists():
        with open(output_path, 'r') as f:
            existing = yaml.safe_load(f) or []
    
    # Dedupe by id
    existing_ids = {e['id'] for e in existing}
    new_entries = [e for e in entries if e['id'] not in existing_ids]
    
    with open(output_path, 'w') as f:
        yaml.dump(existing + new_entries, f, sort_keys=False, default_flow_style=False)
    
    print(f"Added {len(new_entries)} new entries to {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python etl/ingest_energy_tools.py path/to/energy-tools.csv")
        sys.exit(1)
    
    ingest_energy_tools(sys.argv[1])
