# Overview

## Purpose

The Climate & Energy Intelligence Hub is a **single, unified registry** for every open-source tool, dataset, pipeline, foundation model, and learning resource relevant to climate and energy intelligence. It exists to:

1. Eliminate the fragmentation of discovering these resources across dozens of GitHub organizations, spreadsheets, awesome-lists, and paper appendices.
2. Provide **machine-readable metadata** (YAML + FastAPI) so any platform or notebook can query the registry instead of hard-coding resource paths.
3. Establish **common integration patterns** so tools can be wired together consistently (e.g., atlite → PyPSA → pandapower → Grid2Op).

---

## Taxonomy

All entries belong to one of four top-level domains:

### 1. Data & Datasets

Raw inputs consumed by models and pipelines.

| Sub-category | Examples |
|---|---|
| Climate / weather reanalysis | ERA5, MERRA-2, CMIP6 |
| Earth observation (EO) | Sentinel-2, Landsat, Microsoft AI for Earth |
| Grid topology | OpenStreetMap lines, gridfinder synthetic grids, national TSO data |
| Power plants & generation | Global Power Plant Database, GEM coal/gas trackers |
| Resource potential | Global Solar Atlas, Global Wind Atlas, GlobalEnergyGIS |
| Demand & socio-economic | OWID energy data, World Bank, UN population grids |
| Country / region bundles | pypsa-kz-data, pypsa-zm-data, GermanRenewableEnergy |

### 2. Models & Engines

Computational tools that take structured inputs and produce optimized or simulated outputs.

| Sub-category | Examples |
|---|---|
| Capacity expansion | PyPSA, Calliope, GenX, GridPath, OSeMOSYS, ReEDS |
| Production cost / dispatch | oemof-solph, Dispa-SET, psst, Nempy |
| Power flow | pandapower, PowerModels.jl, PYPOWER, Power Grid Model |
| Dynamics & stability | PowerSimulationsDynamics.jl, Dynaωo, DPSim, PowerDynamics.jl |
| Microgrid & DER | python-microgrid, MicroGridsPy, OpenDER, REopt.jl |
| Multi-energy / sector coupling | PyPSA-Earth-sec, FINE, oemof-thermal, DISPATCHES |
| RL environments | Grid2Op, pypownet, energy-py, SustainGym |
| Demand forecasting | pydemand, demand-creator |
| Climate / weather FMs | ClimaX, Aurora, GraphCast, Pangu-Weather, FourCastNet |
| Detection / EO ML | detect-energy, WPGNN |

### 3. Pipelines & Tooling

Scripts, workflows, and utilities that connect data to models.

| Sub-category | Examples |
|---|---|
| Resource time-series | atlite (weather → capacity factors) |
| OSM extraction | earth-osm, pypsa-earth-osm |
| Grid inference | gridfinder |
| Scenario configuration | PyPSA-Earth config system, pypsa-earth-status |
| Validation & benchmarking | country-validation, network-comparison, demand-comp-cntry |
| Visualization | deckGlDashboard, tauritron, pypsa-earth-lit |
| Co-simulation / orchestration | Mosaik, VILLASframework |

### 4. Knowledge, Docs & Governance

Human-readable resources that help contributors and users learn and collaborate.

| Sub-category | Examples |
|---|---|
| Tutorials & notebooks | pypsa-meets-earth/documentation, pypsa-africa-hackathon |
| Survey / awesome lists | Awesome Foundation Models for Weather and Climate |
| Governance | pypsa-meets-earth/governance |
| Status tracking | pypsa-earth-status |
| Websites | pypsa-meets-earth.github.io, energytransitionmodel.com |

---

## Entry metadata fields

See [schema.md](schema.md) for the full reference. Core fields:

- `id` – unique slug (e.g. `pypsa-earth`)
- `name` – human display name
- `kind` – `energy_model | climate_fm | grid_dataset | pipeline | benchmark | doc | governance`
- `domain` – `power_system | multi_sector | climate | socio_economic | eo`
- `scale` – `global | continental | national | regional | project`
- `model_type` – only for models: `capacity_expansion | production_cost | power_flow | dynamics | microgrid | rl_env | demand | detection`
- `language` – `python | julia | java | matlab | modelica | gams | other`
- `inputs` / `outputs` – list of standardized data type tags
- `collections` – which named groupings this entry belongs to
- `region_tags` – ISO3 or region codes
- `license` – SPDX identifier
- `maturity` – `experimental | research | production`
- `docs_url`, `repo_url`, `data_url`

---

## Integration architecture (platform view)

```
[Data & Datasets layer]
  owid-energy-data, GlobalEnergyGIS, OSM, ERA5/atlite,
  gridfinder, AIforEarthDataSets, pypsa-kz-data ...
          |
          v
[Pipeline layer]
  earth-osm  -->  grid topology store
  atlite     -->  resource timeseries store
  pydemand   -->  demand timeseries store
          |
          v
[Model layer]
  PyPSA-Earth  (global/country capacity expansion)
  pandapower   (grid power flow)
  Grid2Op      (RL operations env)
  python-microgrid (project / microgrid)
  Climate FMs  (weather scenarios, risk)
          |
          v
[API / Registry layer]  <-- THIS HUB
  GET /models  GET /datasets  GET /climate-fms
  GET /collections  GET /search
          |
          v
[Platform UIs]
  Scenario Explorer, Grid Explorer,
  Agent Lab, Policy Sandbox, Map Explorer
```

---

## Phased build-out

| Phase | Milestone |
|---|---|
| 0 – Schema | Finalize YAML schemas, CI validation, empty YAML stubs |
| 1 – Backfill | Run all ETL scripts; 150+ models, 80+ datasets populated |
| 2 – API | FastAPI service live; filters by domain, scale, region, language |
| 3 – UI | Search/browse front-end; deep-link to platform scenario engine |
| 4 – Contributions | Community PRs; automated GitHub Actions to detect new awesome-list entries |
