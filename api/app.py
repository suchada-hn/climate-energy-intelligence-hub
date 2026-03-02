"""FastAPI catalog service for Climate & Energy Intelligence Hub."""
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yaml
from pathlib import Path
from typing import List, Optional

app = FastAPI(
    title="Climate & Energy Intelligence Hub API",
    description="Read-only API for querying energy models, datasets, pipelines and climate FMs",
    version="0.1.0"
)

DATA_DIR = Path("../data")

def load_yaml(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, 'r') as f:
        return yaml.safe_load(f) or []

@app.get("/")
def root():
    return {
        "message": "Climate & Energy Intelligence Hub API",
        "endpoints": [
            "/models",
            "/datasets",
            "/pipelines",
            "/climate-fms",
            "/collections",
            "/search"
        ]
    }

@app.get("/models")
def get_models(
    domain: Optional[str] = Query(None),
    scale: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    model_type: Optional[str] = Query(None)
):
    """Get all energy models with optional filters."""
    models = load_yaml("models.yaml")
    
    if domain:
        models = [m for m in models if m.get('domain') == domain]
    if scale:
        models = [m for m in models if m.get('scale') == scale]
    if language:
        models = [m for m in models if m.get('language') == language]
    if model_type:
        models = [m for m in models if m.get('model_type') == model_type]
    
    return {"count": len(models), "models": models}

@app.get("/models/{model_id}")
def get_model(model_id: str):
    models = load_yaml("models.yaml")
    model = next((m for m in models if m.get('id') == model_id), None)
    if not model:
        return JSONResponse(status_code=404, content={"error": "Model not found"})
    return model

@app.get("/datasets")
def get_datasets(
    kind: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    layer: Optional[str] = Query(None)
):
    datasets = load_yaml("datasets.yaml")
    
    if kind:
        datasets = [d for d in datasets if d.get('kind') == kind]
    if region:
        datasets = [d for d in datasets if region in d.get('region_tags', [])]
    if layer:
        datasets = [d for d in datasets if d.get('layer') == layer]
    
    return {"count": len(datasets), "datasets": datasets}

@app.get("/pipelines")
def get_pipelines():
    pipelines = load_yaml("pipelines.yaml")
    return {"count": len(pipelines), "pipelines": pipelines}

@app.get("/climate-fms")
def get_climate_fms(
    task: Optional[str] = Query(None)
):
    fms = load_yaml("climate_fms.yaml")
    
    if task:
        fms = [f for f in fms if f.get('task') == task]
    
    return {"count": len(fms), "climate_fms": fms}

@app.get("/collections")
def get_collections():
    collections = load_yaml("collections.yaml")
    return {"count": len(collections), "collections": collections}

@app.get("/collections/{collection_id}")
def get_collection(collection_id: str):
    collections = load_yaml("collections.yaml")
    collection = next((c for c in collections if c.get('id') == collection_id), None)
    if not collection:
        return JSONResponse(status_code=404, content={"error": "Collection not found"})
    return collection

@app.get("/search")
def search(q: str = Query(..., min_length=2)):
    """Simple full-text search across all entries."""
    q_lower = q.lower()
    results = []
    
    for kind, filename in [("model", "models.yaml"), ("dataset", "datasets.yaml"), 
                            ("pipeline", "pipelines.yaml"), ("climate_fm", "climate_fms.yaml")]:
        entries = load_yaml(filename)
        for entry in entries:
            if (q_lower in entry.get('name', '').lower() or 
                q_lower in entry.get('short_description', '').lower()):
                entry['_type'] = kind
                results.append(entry)
    
    return {"query": q, "count": len(results), "results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
