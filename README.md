# U Sports

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A Python package for fetching current cumulative sports statistics from U Sports.

## 🚀 Installation

```bash
pip install git+https://github.com/ojadeyemi/usports.git
```

## 🎓 Supported Sports

- **Basketball (Men's & Women's)** _(Available)_
- **Football** _(In Progress)_
- **Volleyball (Men's & Women's)** _(In Progress)_
- **Ice Hockey (Men's & Women's)** _(In Progress)_
- **Soccer (Men's & Women's)** _(In Progress)_

## 📈 Usage

```python
from usports.basketball import usport_players_stats, usport_team_stats

# Men's player stats
men_player_stats = usport_players_stats('m')

# Women's player stats for the U Sports Championship Final 8
women_championship_stats = usport_players_stats('w', 'championship')

# Men's team stats
men_team_stats = usport_team_stats('m')

# Women's team stats for playoffs
women_playoffs_stats = usport_team_stats('w', 'playoffs')
```

Both functions return **pandas DataFrames** with the requested statistics.

## 👤 Author

**OJ Adeyemi**  
_Created on February 1, 2025_
