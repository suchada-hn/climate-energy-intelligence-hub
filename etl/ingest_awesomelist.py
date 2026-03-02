#!/usr/bin/env python3
"""
ETL Script: Ingest Awesome Climate/Energy Lists
Ingests curated awesome-lists from CSV files into YAML registries.
"""
import csv
import yaml
from pathlib import Path
from datetime import datetime

def ingest_awesomelist(csv_path: str, output_yaml: str, entry_type: str):
    """
    Ingest awesome-list CSV entries into YAML registry.
    
    Args:
        csv_path: Path to awesomelist CSV file
        output_yaml: Target YAML registry file
        entry_type: Type of entries (models, datasets, pipelines)
    """
    entries = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = {
                'id': row.get('id', '').strip(),
                'name': row.get('name', '').strip(),
                'type': row.get('type', entry_type).strip(),
                'domain': row.get('domain', 'general').strip(),
                'description': row.get('description', '').strip(),
                'url': row.get('url', '').strip(),
                'repo': row.get('repo', '').strip(),
                'license': row.get('license', 'unknown').strip(),
                'tags': [t.strip() for t in row.get('tags', '').split(',') if t.strip()],
                'source': 'awesomelist',
                'ingested_at': datetime.utcnow().isoformat() + 'Z'
            }
            
            # Add optional fields if present
            if row.get('stars'):
                entry['metadata'] = {'github_stars': int(row['stars'])}
            if row.get('last_updated'):
                entry['last_updated'] = row['last_updated']
            
            entries.append(entry)
    
    # Load existing YAML or create new structure
    output_path = Path(output_yaml)
    if output_path.exists():
        with open(output_path, 'r') as f:
            existing = yaml.safe_load(f) or {}
    else:
        existing = {entry_type: []}
    
    # Merge entries (avoid duplicates by id)
    existing_ids = {e['id'] for e in existing.get(entry_type, [])}
    new_entries = [e for e in entries if e['id'] not in existing_ids]
    
    if entry_type not in existing:
        existing[entry_type] = []
    existing[entry_type].extend(new_entries)
    
    # Write updated YAML
    with open(output_path, 'w') as f:
        yaml.dump(existing, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Ingested {len(new_entries)} new entries into {output_yaml}")
    print(f"   Total {entry_type}: {len(existing[entry_type])}")

if __name__ == '__main__':
    # Example usage - adjust paths as needed
    ingest_awesomelist(
        csv_path='source_data/awesomelist.csv',
        output_yaml='data/models.yaml',
        entry_type='models'
    )
