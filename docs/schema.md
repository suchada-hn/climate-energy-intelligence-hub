# Schema Reference

All YAML files under `data/` share a common schema. This document is the authoritative field-by-field reference.

---

## Universal fields (all entry types)

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | URL-safe unique slug. Use lowercase + hyphens. |
| `name` | string | yes | Human-readable display name. |
| `kind` | enum | yes | See Kind values below. |
| `short_description` | string | yes | One or two sentences. Plain text. |
| `repo_url` | string | no | GitHub / GitLab URL of the source code. |
| `docs_url` | string | no | Documentation site URL. |
| `data_url` | string | no | Direct link to dataset download or API (for datasets). |
| `license` | string | no | SPDX identifier (e.g. `MIT`, `Apache-2.0`, `CC-BY-4.0`). |
| `maturity` | enum | no | `experimental`, `research`, `production`. |
| `collections` | list[string] | no | IDs of collections this entry belongs to. |
| `tags` | list[string] | no | Free-form supplementary tags. |

---

## Kind values

| Kind | Used in file | Description |
|---|---|---|
| `energy_model` | models.yaml | Optimization, simulation, or dispatch model for energy systems |
| `climate_fm` | climate_fms.yaml | Foundation model for weather or climate prediction / emulation |
| `grid_dataset` | datasets.yaml | Static or semi-static dataset describing grid infrastructure |
| `resource_dataset` | datasets.yaml | Renewable resource potential, weather, or EO raster data |
| `socioeconomic_dataset` | datasets.yaml | Demand, population, economic activity data |
| `country_data_bundle` | datasets.yaml | Country or region-specific curated input bundle |
| `pipeline` | pipelines.yaml | Script or workflow connecting data sources to model inputs |
| `benchmark` | models.yaml / climate_fms.yaml | Evaluation dataset or competition framework |
| `rl_environment` | models.yaml | Reinforcement learning environment for grid/energy control |
| `doc` | — | Tutorial, notebook, hackathon, or survey |
| `governance` | — | Governance document, roadmap, contribution guide |

---

## Additional fields for `energy_model`

| Field | Type | Required | Description |
|---|---|---|---|
| `domain` | enum | yes | `power_system`, `multi_sector`, `microgrid`, `market`, `socioeconomic` |
| `scale` | enum | yes | `global`, `continental`, `national`, `regional`, `project` |
| `model_type` | enum | yes | See Model type values below |
| `language` | enum | yes | `python`, `julia`, `java`, `matlab`, `modelica`, `gams`, `other` |
| `solver_interface` | list[string] | no | e.g. `linopy`, `pyomo`, `jump`, `cplex` |
| `inputs` | list[string] | no | Standardized input data tags (see Input / Output tags) |
| `outputs` | list[string] | no | Standardized output data tags |
| `region_tags` | list[string] | no | ISO3 codes or region names (`ASEAN`, `Africa`, `EU`) |

### Model type values

`capacity_expansion`, `production_cost`, `power_flow`, `opf`, `dynamics`, `stability`, `microgrid`, `market_dispatch`, `unit_commitment`, `rl_env`, `demand_forecast`, `eo_detection`, `multi_vector`

---

## Additional fields for `climate_fm`

| Field | Type | Required | Description |
|---|---|---|---|
| `task` | enum | yes | `forecasting`, `downscaling`, `emulation`, `detection`, `impact`, `reanalysis` |
| `architecture` | string | no | e.g. `transformer`, `graph-neural-network`, `diffusion`, `unet` |
| `input_data` | list[string] | no | e.g. `ERA5`, `CMIP6`, `GFS` |
| `output_vars` | list[string] | no | e.g. `temperature`, `wind_speed`, `precipitation` |
| `spatial_resolution` | string | no | e.g. `0.25deg`, `1km` |
| `temporal_resolution` | string | no | e.g. `6h`, `1h`, `daily` |
| `lead_time` | string | no | Maximum forecast lead time, e.g. `10days`, `seasonal` |

---

## Additional fields for datasets

| Field | Type | Required | Description |
|---|---|---|---|
| `modality` | enum | yes | `vector`, `raster`, `timeseries`, `tabular`, `mixed` |
| `region_tags` | list[string] | no | ISO3 codes or region names |
| `layer` | enum | no | `transmission`, `distribution`, `generation`, `demand`, `resource`, `socioeconomic` |
| `update_frequency` | string | no | e.g. `static`, `annual`, `monthly`, `realtime` |
| `resolution` | string | no | Spatial or temporal resolution |
| `format` | list[string] | no | e.g. `geojson`, `csv`, `netcdf`, `parquet` |

---

## Additional fields for `pipeline`

| Field | Type | Required | Description |
|---|---|---|---|
| `inputs_from` | list[string] | no | IDs of datasets or tools this pipeline consumes |
| `outputs_to` | list[string] | no | IDs of models or stores this pipeline feeds |
| `trigger` | enum | no | `manual`, `scheduled`, `event` |
| `runtime` | string | no | e.g. `python`, `snakemake`, `airflow` |

---

## Standardized Input / Output tags

Use these consistently in `inputs` and `outputs` fields of models.

**Data type tags**
- `electricity_demand_timeseries`
- `renewable_potential_timeseries`
- `grid_topology_vector`
- `generator_fleet_tabular`
- `weather_reanalysis_raster`
- `climate_projection_raster`
- `eo_satellite_raster`
- `fuel_price_timeseries`
- `co2_price_timeseries`
- `policy_constraints_tabular`

**Output type tags**
- `generation_timeseries`
- `storage_timeseries`
- `network_flows_timeseries`
- `investment_decisions_tabular`
- `emissions_timeseries`
- `electricity_prices_timeseries`
- `adequacy_metrics_tabular`
- `stability_indicators_tabular`

---

## Example: full energy model entry

```yaml
- id: pypsa-earth
  name: PyPSA-Earth
  kind: energy_model
  short_description: >-
    Open optimisation model for studying energy system futures worldwide,
    built on the PyPSA framework with global OSM-based network data.
  repo_url: https://github.com/pypsa-meets-earth/pypsa-earth
  docs_url: https://pypsa-earth.readthedocs.io
  license: MIT
  maturity: research
  domain: power_system
  scale: global
  model_type: capacity_expansion
  language: python
  solver_interface: [linopy]
  inputs:
    - electricity_demand_timeseries
    - renewable_potential_timeseries
    - grid_topology_vector
    - generator_fleet_tabular
  outputs:
    - generation_timeseries
    - investment_decisions_tabular
    - emissions_timeseries
    - network_flows_timeseries
  region_tags: [global]
  collections:
    - pypsa-earth-ecosystem
    - power-system-tools
```

## Example: full climate FM entry

```yaml
- id: climax
  name: ClimaX
  kind: climate_fm
  short_description: >-
    Foundation model for weather and climate science, pre-trained on
    heterogeneous CMIP6 climate simulations and fine-tuned on ERA5.
  repo_url: https://github.com/microsoft/ClimaX
  license: MIT
  maturity: research
  task: forecasting
  architecture: transformer
  input_data: [CMIP6, ERA5]
  output_vars: [temperature, wind_speed, geopotential, precipitation]
  spatial_resolution: 1.40625deg
  temporal_resolution: 6h
  lead_time: 10days
  collections: [climate-foundation-models]
```

## Example: full dataset entry

```yaml
- id: global-power-plant-database
  name: Global Power Plant Database
  kind: grid_dataset
  short_description: >-
    Open database of power plants worldwide with capacity, fuel type,
    location and generation estimates.
  data_url: https://datasets.wri.org/dataset/globalpowerplantdatabase
  license: CC-BY-4.0
  maturity: production
  modality: tabular
  region_tags: [global]
  layer: generation
  update_frequency: annual
  format: [csv]
  collections: [grid-datasets-global]
```
