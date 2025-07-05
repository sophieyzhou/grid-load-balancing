# Hydrogen Storage Cost Analysis in Low VRE Penetration Grids

This project investigates the cost-effectiveness and carbon implications of deploying hydrogen storage systems in generation fleets with limited renewable energy (VRE) penetration, focusing on California’s energy market. The work was completed for IOE 491 at the University of Michigan and combines real-world energy data, economic dispatch modeling, and scenario analysis to assess when and how hydrogen storage aligns with environmental and financial goals.

## Overview

Green hydrogen has been promoted as a solution to mitigate seasonal volatility in renewable energy, but real-world deployment remains dominated by gray hydrogen from fossil fuels. This project models how fossil-fueled hydrogen storage competes with other generation assets across varying system efficiencies and carbon pricing schemes.

### Key Questions:
- What are the main cost drivers of hydrogen storage in non-high-renewable grids?
- Under what conditions does hydrogen outperform traditional baseload sources like nuclear?
- How does carbon taxation or policy incentives affect hydrogen's role?

## Methodology

- **Region**: California (EIA + CAISO data)
- **Model**: Weekly-resolution economic dispatch with system-wide cost minimization
- **Simplifications**: Grouped generation assets, simplified storage assumptions, max daily solar as proxy for short-term storage
- **Hydrogen Unit**: Based on ACES Delta storage specs, with round-trip efficiency (RTE) and O&M costs from PNNL

## Data Sources

- EIA Open Data: https://www.eia.gov/opendata/browser/electricity/electric-power-operational-data
- ACES Delta Project: https://aces-delta.com/sites/
- PNNL Hydrogen Storage Cost Reports: https://www.pnnl.gov/sites/default/files/media/file/Hydrogen_Methodology.pdf
- MIT Carbon Emissions Policy: https://news.mit.edu/2024/cutting-carbon-emissions-us-power-grid-0311

Full list of sources in the References section below.

## Project Structure

├── Auxiliary_Data/ # Raw solar, wind, hydro, and demand time series
├── clean_data.py # Cleans and processes raw EIA data
├── download_fleet.py # Retrieves fleet-level generation assets
├── getdata.py # Data collection utility
├── model.py # Core economic dispatch model
├── visuals.py # Plotting utilities
├── Demand_Data.csv # Final processed demand inputs
├── h2storage.csv # Hydrogen storage specifications
├── fleet.csv # Asset-level fleet parameters
├── Model_outputs.csv # CSV results from model runs
├── *.png # Visual outputs and result plots


## Key Findings

- Gray hydrogen + natural gas outperforms nuclear at high RTEs (>0.65) and low CO₂ tax, but this can backfire environmentally.
- Carbon taxes effectively realign cost-optimized dispatch with emissions goals, suppressing gray hydrogen use.
- In current tech bounds (RTE < 0.5), nuclear remains preferable unless green hydrogen input increases.
- Model suggests opportunities for policy interventions to prevent unintended pro-fossil behavior in hybrid hydrogen systems.

## References

1. Jaradat, M. et al. (2022). *Potential of producing green hydrogen in Jordan*. Energies, 15(23), 9039. https://doi.org/10.3390/en15239039  
2. U.S. Energy Information Administration. (n.d.). Open Data Portal. https://www.eia.gov/opendata/browser/electricity/electric-power-operational-data  
3. ACES Delta. (n.d.). Advanced Clean Energy Storage Site. https://aces-delta.com/sites/  
4. Mongird, K. et al. (2020). *Hydrogen Energy Storage: A Methodology to Assess Regional Hydrogen Resources*. PNNL. https://www.pnnl.gov/sites/default/files/media/file/Hydrogen_Methodology.pdf  
5. Martínez de León, C. et al. (2024). *Levelized Cost of Storage (LCOS) for a hydrogen system*. International Journal of Hydrogen Energy, 52, 1274-1284.  
6. Stauffer, N. (2024). *Cutting Carbon Emissions on the US Power Grid*. MIT News. https://news.mit.edu/2024/cutting-carbon-emissions-us-power-grid-0311

## Author

**Sophie Zhou**  
University of Michigan  
BSE Computer Science 2026
https://github.com/sophieyzhou
