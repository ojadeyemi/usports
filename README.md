# U Sports

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A Python package that retrieves current cumulative team sports statistics from U Sports.

This lightweight tool helps you easily access and analyze the latest statistical data from Canadian university sports leagues.

## 🚀 Installation

```bash
pip install git+https://github.com/ojadeyemi/usports.git
# OR
poetry add git+https://github.com/ojadeyemi/usports.git
```

## Supported Sports

| Sport        | Status         | League      |
| ------------ | -------------- | ----------- |
| Basketball   | ✅ Available   | Men & Women |
| Football     | ✅ Available | Men         |
| Volleyball   | 🔄 In Progress | Men & Women |
| Ice Hockey   | 🔄 In Progress | Men & Women |
| Soccer       | 🔄 In Progress | Men & Women |
| Field Hockey | 🔄 In Progress | Women       |

## Usage

```python
from usports.basketball import usport_bball_players_stats, usport_bball_team_stats

# Men's player stats
men_player_stats = usport_bball_players_stats('m')

# Women's player stats for the U Sports Championship Final 8
women_championship_stats = usport_bball_players_stats('w', 'championship')

# Men's team stats
men_team_stats = usport_bball_team_stats('m')

# Women's team stats for playoffs
women_playoffs_stats = usport_bball_team_stats('w', 'playoffs')
```

Both functions return **pandas DataFrames** with the requested statistics.

## 👤 Author

**OJ Adeyemi**  
_Created on February 1, 2025_
