# USPORTS

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A Python package that retrieves current cumulative sport statistics from USPORTS.

This lightweight tool helps you easily access and analyze the latest statistical data from Canadian University Sports League.

## 🚀 Installation

```bash
pip install git+https://github.com/ojadeyemi/usports.git
# OR
poetry add git+https://github.com/ojadeyemi/usports.git
```

## Supported Sports

| Sport      | Status         | League      |
| ---------- | -------------- | ----------- |
| Basketball | ✅ Available   | Men & Women |
| Football   | ✅ Available   | Men         |
| Ice Hockey | ✅ Available   | Men & Women |
| Volleyball | ✅ Available   | Men & Women |
| Soccer     | 🔄 In Progress | Men & Women |

## Usage

```python
from usports.basketball import usports_bball_players, usports_bball_teams, usports_bball_standings
from usports.football import usports_fball_teams, usports_fball_players, usports_fball_standings

# Men's basketball player stats
men_bball_player_stats = usports_bball_players('m')

# Women's basketball player stats for the U Sports Championship Final 8
women_bball_championship_stats = usports_bball_players('w', 'championship')

# Men's football playoffs team stats
men_fball_team_stats = usports_fball_teams('playoffs')

# Women's basketball team stats for playoffs
women_playoffs_stats = usports_bball_teams('w', 'playoffs')

# Men's basketball standings
men_bball_standings = usports_bball_standings('m')

# Football standings
fball_standings = usports_fball_standings()
```

Both functions return **pandas DataFrames** with the requested statistics.
