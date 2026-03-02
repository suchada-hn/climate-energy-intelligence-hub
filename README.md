# Climate & Energy Intelligence Hub

> A systematic, open knowledge registry mapping every major open-source tool, dataset, pipeline, and foundation model in the climate & energy intelligence space — structured for direct integration into the RIFFAI-Energy platform and beyond.

[![Schema Validation](https://github.com/suchada-hn/climate-energy-intelligence-hub/actions/workflows/validate-schema.yml/badge.svg)](https://github.com/suchada-hn/climate-energy-intelligence-hub/actions/workflows/validate-schema.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

---

## What this hub is

This repository is a **curated, machine-readable knowledge registry** covering:

- 150+ open-source energy system models and simulation tools
- 50+ climate and weather foundation models (AI/ML)
- Global and regional grid, generation, and resource datasets
- End-to-end data and modeling pipelines (PyPSA-Earth ecosystem and others)
- Governance, benchmarks, and learning resources

Every entry follows a **common metadata schema** so the hub can be queried programmatically by any platform, dashboard, or research workflow.

---

## Repository structure

```
climate-energy-intelligence-hub/
  README.md                        # This file
  CONTRIBUTING.md                  # How to add or update entries
  LICENSE
  docs/
    overview.md                    # Full narrative overview & taxonomy
    schema.md                      # Field-by-field schema reference
    pypsa-earth-ecosystem.md       # PyPSA-Earth org deep-dive
    climate-foundation-models.md   # Weather & climate FM catalog
  data/
    models.yaml                    # Energy system models & tools (150+)
    datasets.yaml                  # Grid, generation & resource datasets
    pipelines.yaml                 # Data extraction & scenario pipelines
    climate_fms.yaml               # Climate & weather foundation models
    collections.yaml               # Named groupings / ecosystems
  etl/
    ingest_energy_tools.py         # From energy-tools.csv
    ingest_awesomelist.py          # From awesomelist.csv
    ingest_datasources_md.py       # From DATA_SOURCES.md
    ingest_pypsa_earth_org.py      # From pypsa-meets-earth GitHub org
    ingest_climate_fms.py          # From Awesome FM README
  api/
    app.py                         # FastAPI read-only catalog API
    schemas.py                     # Pydantic models
    requirements.txt
  .github/
    workflows/
      validate-schema.yml          # CI: validate all YAML against schemas
      build-api.yml                # CI: lint & test API
    ISSUE_TEMPLATE/
      add_model.md
      add_dataset.md
      bug_report.md
```

---

## Four top-level domains

| Domain | What it contains |
|---|---|
| **Data & Datasets** | Climate/weather reanalysis, EO, socio-economic, grid topology, resource maps |
| **Models & Engines** | Energy system models, climate FMs, demand forecasting, detection/EO models |
| **Pipelines & Tooling** | Data extraction, scenario building, validation, training scripts |
| **Knowledge, Docs & Governance** | Tutorials, hackathons, notebooks, governance, status tracking |

---

## Quick start

### Browse the registry

```bash
git clone https://github.com/suchada-hn/climate-energy-intelligence-hub.git
cd climate-energy-intelligence-hub
```

All entries live in `data/*.yaml` — human-readable and machine-queryable.

### Run the catalog API locally

```bash
cd api
pip install -r requirements.txt
uvicorn app:app --reload
# Open http://localhost:8000/docs
```

### Run ETL to refresh data

```bash
pip install pyyaml requests
python etl/ingest_energy_tools.py
python etl/ingest_pypsa_earth_org.py
python etl/ingest_climate_fms.py
```

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/models` | List all energy models with optional filters |
| GET | `/models/{id}` | Single model entry |
| GET | `/datasets` | List all datasets with optional filters |
| GET | `/datasets/{id}` | Single dataset entry |
| GET | `/climate-fms` | List climate & weather foundation models |
| GET | `/collections` | List all named collections |
| GET | `/collections/{id}` | All members of a collection |
| GET | `/search?q=` | Full-text search across all entries |

Key filter parameters: `domain`, `scale`, `region`, `language`, `model_type`, `layer`, `license`

---

## Collections

- `pypsa-earth-ecosystem` — all PyPSA-Earth org repos, data packs, demand tools, detection pipelines
- `power-system-tools` — 150+ energy system models from energy-tools.csv
- `climate-foundation-models` — weather/climate FMs from the Awesome FM survey
- `grid-datasets-global` — transmission, distribution, generation datasets worldwide
- `demand-tools` — demand forecasting and time-series generation tools
- `rl-environments` — Grid2Op, pypownet, SustainGym, energy-py and related RL envs
- `microgrid-tools` — python-microgrid, MicroGridsPy, microgrids.py, OpenDER

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The fastest way to add an entry is to open an issue using one of the templates in `.github/ISSUE_TEMPLATE/`.

---

## License

Registry content (YAML files and docs): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
Code (ETL scripts, API): [MIT](LICENSE)

---

## Acknowledgements

This hub consolidates resources from:
- [PyPSA-Meets-Earth](https://github.com/pypsa-meets-earth) initiative
- [Awesome Foundation Models for Weather and Climate](https://github.com/shengchaochen82/Awesome-Foundation-Models-for-Weather-and-Climate)
- [Open Energy Modelling Initiative](https://openmod-initiative.org/)
- NREL, IIASA, RLI, TU Berlin, TU Munich and many other institutions
- The open energy modelling community
