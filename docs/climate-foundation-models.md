# Climate & Weather Foundation Models

Catalog of foundation models (large pre-trained neural networks) for weather forecasting, climate projection, downscaling, and related tasks. Sourced from [Awesome-Foundation-Models-for-Weather-and-Climate](https://github.com/shengchaochen82/Awesome-Foundation-Models-for-Weather-and-Climate).

All entries are registered in `data/climate_fms.yaml`.

---

## Why these models matter for energy intelligence

| Use case | Example models | How they feed energy models |
|---|---|---|
| Wind/solar resource forecasting | GraphCast, Pangu-Weather, FourCastNet | Short-term capacity factor inputs for dispatch |
| Long-term climate projection | ClimaX (CMIP6 fine-tuned) | Climate-adjusted resource time series for planning |
| Extreme event probability | NeuralGCM, probabilistic diffusion models | Stress-test scenarios for adequacy studies |
| Downscaling | DDPM-based, CNN super-resolution | High-resolution local resource maps |
| Demand forecasting | Temperature-conditioned transformers | Load profile generation under climate scenarios |

---

## Category 1: Global weather forecasting FMs

Models that predict atmospheric state variables at global scale.

| Model | Architecture | Input | Resolution | Lead time | Repo |
|---|---|---|---|---|---|
| GraphCast (DeepMind) | Graph Neural Network | ERA5 | 0.25° | 10 days | https://github.com/google-deepmind/graphcast |
| Pangu-Weather | 3D Earth Transformer | ERA5 | 0.25° | 7 days | https://github.com/198808xc/Pangu-Weather |
| FourCastNet (NVIDIA) | Adaptive Fourier Neural Operator | ERA5 | 0.25° | 2 weeks | https://github.com/NVlabs/FourCastNet |
| Aurora (Microsoft) | Transformer | ERA5, CMIP6, GFS | 0.1° | 15 days | https://github.com/microsoft/aurora |
| ClimaX (Microsoft) | Transformer (pre-trained CMIP6) | CMIP6, ERA5 | 1.4° | 10 days | https://github.com/microsoft/ClimaX |
| Stormer | Transformer | ERA5 | 1.4° | 10 days | — |
| NeuralGCM (Google) | Differentiable GCM + ML | ERA5 | Variable | Seasonal | https://github.com/google-research/neuralgcm |
| GenCast (DeepMind) | Diffusion | ERA5 | 0.25° | 15 days | — |
| WeatherGFM | Generative FM | ERA5 | 0.25° | 10 days | — |

---

## Category 2: Regional & downscaling models

| Model | Task | Region | Architecture | Repo |
|---|---|---|---|---|
| Deep SD | Statistical downscaling | Global | CNN | — |
| SWIN-SD | Downscaling | Europe | Swin Transformer | — |
| DiffESM | Climate emulation | Global | Diffusion | — |
| CorrDiff (NVIDIA) | Probabilistic downscaling | CONUS | Diffusion | https://github.com/NVlabs/edm |

---

## Category 3: Climate projection & emulation FMs

Models that emulate or project multi-decadal climate trajectories.

| Model | Task | Input | Output | Repo |
|---|---|---|---|---|
| ClimaX (CMIP6) | Climate emulation | CMIP6 scenarios | T, P, wind | https://github.com/microsoft/ClimaX |
| ACE (Allen AI) | Atmospheric emulation | CMIP6 | Full atm state | https://github.com/ai2cm/ace |
| NeuralGCM | Full GCM hybrid | ERA5 | Full atm state | https://github.com/google-research/neuralgcm |
| ClimateLearn | Benchmark suite | ERA5, CMIP6 | Multiple | https://github.com/aditya-grover/climate-learn |

---

## Category 4: Specialized / application models

| Model | Task | Notes |
|---|---|---|
| ENSO prediction transformers | ENSO index forecast | Regime change detection for long-range planning |
| Precipitation nowcasting GNNs | Short-range precip | Hydropower inflow forecasting |
| Air quality foundation models | Pollution + PM2.5 | Grid siting, health co-benefits analysis |
| Land surface / soil moisture | Soil state | Biomass and agriculture energy nexus |
| Arctic sea ice prediction | Sea ice extent | Shipping route, offshore wind |

---

## Category 5: Benchmarks & evaluation datasets

| Benchmark | Description | Repo |
|---|---|---|
| WeatherBench 2 | Standardized global forecast evaluation | https://github.com/google-research/weatherbench2 |
| ClimART | Climate model emulation benchmark | https://github.com/RolnickLab/climart |
| ClimateLearn | ML for climate benchmark suite | https://github.com/aditya-grover/climate-learn |
| ClimateBench | Multi-variable climate projection benchmark | https://github.com/duncanwp/ClimateBench |

---

## Integration into RIFFAI-Energy

### Pattern 1: Climate-conditioned resource time series
```
ClimaX / Aurora (climate scenario) → atlite (resource conversion) → PyPSA-Earth
```
Use a climate FM to generate temperature/wind/irradiance fields under a 2°C or 4°C scenario, feed them into atlite to produce hourly capacity factors, then into PyPSA-Earth for climate-adjusted capacity expansion.

### Pattern 2: Stress-test dispatch scenarios
```
GenCast / NeuralGCM (ensemble forecast) → Grid2Op (RL operations env)
```
Sample 50 weather trajectories from a probabilistic FM; run each through Grid2Op as separate episodes to estimate reliability and tail-risk metrics.

### Pattern 3: Demand forecasting under climate change
```
ClimaX temperature projections → demand model → PyPSA-Earth load timeseries
```
Climate-adjusted cooling/heating degree days feed a demand model to generate future load profiles that account for temperature shifts.

---

## Catalog source

All models are catalogued in `data/climate_fms.yaml`. The ETL script `etl/ingest_climate_fms.py` parses the [Awesome FM README](https://github.com/shengchaochen82/Awesome-Foundation-Models-for-Weather-and-Climate) and keeps this registry up to date.
