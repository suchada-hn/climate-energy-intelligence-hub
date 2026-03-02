# PyPSA-Earth Ecosystem

Complete mapping of every repository in the [pypsa-meets-earth](https://github.com/pypsa-meets-earth) GitHub organisation, including their role, integration layer, and relationships.

---

## Core models

### pypsa-earth
- **Repo:** https://github.com/pypsa-meets-earth/pypsa-earth
- **Kind:** energy_model / capacity_expansion
- **Scale:** global
- **Description:** End-to-end workflow that builds a PyPSA network for any country or region using OpenStreetMap grid data, atlite resource time series, and demand projections. The reference backbone of the ecosystem.
- **Key inputs:** OSM grid lines, atlite capacity factors, demand time series, technology cost assumptions
- **Key outputs:** Optimised generation/storage investment, hourly dispatch, emissions, LCOEs
- **Platform role:** Primary scenario engine for RIFFAI Scenario Explorer

### pypsa-earth-sec
- **Repo:** https://github.com/pypsa-meets-earth/pypsa-earth-sec
- **Kind:** energy_model / capacity_expansion / sector_coupling
- **Scale:** national / regional
- **Description:** Extends pypsa-earth with sector coupling (heating, transport, industry, hydrogen). Analogous to PyPSA-Eur-Sec applied to the global south.
- **Platform role:** Multi-sector scenario extension module

### pypsa-distribution
- **Repo:** https://github.com/pypsa-meets-earth/pypsa-distribution
- **Kind:** energy_model / power_flow
- **Scale:** project / local
- **Description:** Distribution-network extension of PyPSA-Earth, enabling LV/MV level power flow studies integrated with the transmission-level model.
- **Platform role:** Grid Explorer distribution analysis

---

## Regional / country models

| Repo | Region | Notes |
|---|---|---|
| pypsa-asean | ASEAN | Full PyPSA-Earth run for South-East Asia |
| pypsa-colombia | Colombia | Case study / validated national model |
| PyPSA-BO | Bolivia | Jupyter-notebook based Bolivian model |

---

## Data pipelines & extraction

### earth-osm
- **Repo:** https://github.com/pypsa-meets-earth/earth-osm
- **Kind:** pipeline
- **Description:** Python library that extracts power infrastructure (lines, substations, generators) from OpenStreetMap for any bounding box or country polygon.
- **Outputs to:** `grid_topology_vector` store in platform data lake
- **Platform role:** Grid topology ingestion pipeline

### pypsa-earth-osm
- **Repo:** https://github.com/pypsa-meets-earth/pypsa-earth-osm
- **Kind:** pipeline
- **Description:** Exploration of synergies between OSM data quality and energy planning accuracy.
- **Platform role:** OSM data quality assessment pipeline

### pypsa-kz-data
- **Repo:** https://github.com/pypsa-meets-earth/pypsa-kz-data
- **Kind:** country_data_bundle
- **Region:** KAZ (Kazakhstan)
- **Description:** Curated extra input data for the Kazakhstan PyPSA-Earth model.

### pypsa-zm-data
- **Repo:** https://github.com/pypsa-meets-earth/pypsa-zm-data
- **Kind:** country_data_bundle
- **Region:** ZMB (Zambia)
- **Description:** Country-specific data bundle for Zambia.

---

## Demand tools

### pydemand
- **Repo:** https://github.com/pypsa-meets-earth/pydemand
- **Kind:** pipeline / demand
- **Description:** Python tool to generate country-level electricity demand time series for PyPSA-Earth scenarios.
- **Outputs to:** `electricity_demand_timeseries` store

### demand-creator
- **Repo:** https://github.com/pypsa-meets-earth/demand-creator
- **Kind:** pipeline / demand
- **Description:** Tooling to create and adjust demand profiles from socio-economic indicators.

### demand-comp-cntry
- **Repo:** https://github.com/pypsa-meets-earth/demand-comp-cntry
- **Kind:** benchmark
- **Description:** Competition framework for backtesting country-level electricity demand forecasts against historical data.

---

## Detection & EO ML

### detect-energy
- **Repo:** https://github.com/pypsa-meets-earth/detect-energy
- **Kind:** pipeline / eo_detection
- **Description:** Prototype pipeline using semi-supervised object detection (Unbiased Teacher) to identify power infrastructure (lines, substations) in satellite imagery. Feeds QA and gap-filling of OSM-derived grids.
- **Platform role:** EO-based grid asset detection for data-sparse countries

### unbiased-teacher
- **Repo:** https://github.com/pypsa-meets-earth/unbiased-teacher
- **Kind:** model component
- **Description:** PyTorch fork of the ICLR 2021 Unbiased Teacher paper used by detect-energy.

---

## Validation & QA

### country-validation
- **Repo:** https://github.com/pypsa-meets-earth/country-validation
- **Kind:** benchmark
- **Description:** Repository of filled validation notebooks comparing PyPSA-Earth outputs against official national statistics for various countries.

### network-comparison
- **Repo:** https://github.com/pypsa-meets-earth/network-comparison
- **Kind:** benchmark
- **Description:** Tools for comparing alternative grid topologies (e.g. OSM vs. ENTSO-E vs. gridfinder).

### pypsa-earth-status
- **Repo:** https://github.com/pypsa-meets-earth/pypsa-earth-status
- **Kind:** governance
- **Description:** Tracks build and test status of the pypsa-earth pipeline across countries.

---

## UI & Visualization

### tauritron
- **Repo:** https://github.com/pypsa-meets-earth/tauritron
- **Kind:** pipeline / visualization
- **Description:** Open-source web interface for running worldwide energy system planning scenarios. Reference UI for RIFFAI Scenario Explorer.

### pypsa-earth-lit
- **Repo:** https://github.com/pypsa-meets-earth/pypsa-earth-lit
- **Kind:** pipeline / visualization
- **Description:** Streamlit module for interactive exploration of PyPSA-Earth results against a stable package version.

### mrio
- **Repo:** https://github.com/pypsa-meets-earth/mrio
- **Kind:** model
- **Description:** Multi-Regional Input-Output analysis tools for PyPSA-Earth scenarios.

---

## Knowledge & governance

| Repo | Kind | Description |
|---|---|---|
| documentation | doc | Hackathon material, Jupyter notebooks, visualisations |
| pypsa-africa-hackathon | doc | Self-learning material for PyPSA-Earth/Eur/Africa |
| governance | governance | Governance framework for the initiative |
| pypsa-meets-earth.github.io | doc | Initiative website source |
| pypsa-meets-africa.github.io | doc | Archived Africa initiative website |

---

## Dependency graph

```
owid-energy-data ──┐
global-power-plant-db ──┐  |
atlas / ERA5 ──> atlite ──> pypsa-earth ──> results
OpenStreetMap ──> earth-osm ──┘         |
pydemand / demand-creator ──────────────┘
                                         |
              pypsa-earth-sec (sector) ──┘
              pypsa-distribution (LV) ──┘
                                         |
              country-validation <────────
              tauritron / pypsa-earth-lit <─
```

---

## Integration checklist for RIFFAI-Energy

- [ ] Register all repos in `data/models.yaml`, `data/pipelines.yaml`, `data/datasets.yaml`
- [ ] Add `pypsa-earth-ecosystem` collection in `data/collections.yaml`
- [ ] Implement `scenario-engine-pypsa` microservice wrapping pypsa-earth
- [ ] Implement `grid-ingestion-pipeline` using earth-osm
- [ ] Implement `demand-timeseries-service` using pydemand + demand-creator
- [ ] Link `atlite` as resource time-series service feeding pypsa-earth
- [ ] Integrate `detect-energy` as satellite-based QA step for data-sparse countries
- [ ] Import `country-validation` notebooks as benchmark baselines
