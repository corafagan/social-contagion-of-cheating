# Social Contagion of Cheating in PUBG

**Author**: Cora Fagan  
**Date Created**: 2024-12-14
**Language**: Python 3  
**Project Type**: Simulation-based behavioral analysis using real-world game telemetry  

---

## Overview

This project investigates two social dynamics in online gaming:

1. **Homophily** — Do cheaters tend to play together more than expected by chance?  
2. **Contagion** — Do players who **observe**, **get killed by**, or **team up with** cheaters later become cheaters themselves?

Using real match data from *PlayerUnknown's Battlegrounds (PUBG)* between **March 1–10, 2019**, we simulate randomized counterfactuals and compare observed outcomes to what would be expected under random associations.

---

## Data Format (Required)

>  _Note: Original data is not public. You must provide your own data formatted as below._

| File Name        | Description                                             | Fields                                                   |
|------------------|---------------------------------------------------------|-----------------------------------------------------------|
| `cheaters.txt`   | Players caught cheating                                | Player ID, start date of cheating, ban date              |
| `kills.txt`      | Kill records from 6,000 matches                        | Match ID, Killer ID, Victim ID, Kill timestamp           |
| `team_ids.txt`   | Team composition for 5,419 team matches                | Match ID, Player ID, Team ID                             |

---

## Repository Structure

├── get_file_data.py # Functions to load and clean data files 

├── cheaters.py # Cheating behavior logic and filters 

├── shuffle.py # Functions to simulate randomized match events

├── summarize.py # Metrics, mean estimates, and confidence intervals

├── social-contagion-of-cheating.ipnyb # Core analysis logic and output (or use IPython/Notebook)

└── README.md # This file
