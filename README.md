# USPORTS

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A Python package that scrapes current cumulative sport statistics from the University Sports website (universitysport.prestosports.com). It provides a clean pandas DataFrame interface for accessing Canadian university sports data across multiple sports and seasons.

## 🚀 Installation

```bash
pip install git+https://github.com/ojadeyemi/usports.git
# OR
poetry add git+https://github.com/ojadeyemi/usports.git
```

## 📊 Supported Sports

| Sport      | Status       | League      | Data Types                |
| ---------- | ------------ | ----------- | ------------------------- |
| Basketball | ✅ Available | Men & Women | Players, Teams, Standings |
| Ice Hockey | ✅ Available | Men & Women | Players, Teams, Standings |
| Volleyball | ✅ Available | Men & Women | Players, Teams, Standings |
| Soccer     | ✅ Available | Men & Women | Players, Teams, Standings |
| Football   | 🚧 Coming soon | Men         | Players, Teams, Standings |

## 🎯 Usage

### Basketball

```python
from usports.basketball import usports_bball_players, usports_bball_teams, usports_bball_standings

# Men's basketball player stats
men_players = usports_bball_players('m')

# Women's basketball player stats for championship
women_championship_players = usports_bball_players('w', 'championship')

# Women's team stats for playoffs
women_team_stats = usports_bball_teams('w', 'playoffs')

# Men's standings
men_standings = usports_bball_standings('m')
```

### Football

```python
from usports.football import usports_fball_players, usports_fball_teams, usports_fball_standings

# Regular season team stats
team_stats = usports_fball_teams('regular')

# Playoff player stats
playoff_players = usports_fball_players('playoffs')

# Standings
standings = usports_fball_standings()
```

### Ice Hockey

```python
from usports.ice_hockey import usports_ice_hockey_players, usports_ice_hockey_teams, usports_ice_hockey_standings

# Men's regular season team stats
men_teams = usports_ice_hockey_teams('m', 'regular')

# Women's player stats
women_players = usports_ice_hockey_players('w')

# Women's standings
women_standings = usports_ice_hockey_standings('w')
```

### Volleyball

```python
from usports.volleyball import usports_vball_players, usports_vball_teams, usports_vball_standings

# Men's team stats
men_teams = usports_vball_teams('m', 'regular')

# Women's championship players
women_championship = usports_vball_players('w', 'championship')

# Standings
standings = usports_vball_standings('m')
```

### Soccer

```python
from usports.soccer import usports_soccer_players, usports_soccer_teams, usports_soccer_standings

# Men's team stats
men_teams = usports_soccer_teams('m', 'regular')

# Women's players
women_players = usports_soccer_players('w')

# Men's standings
men_standings = usports_soccer_standings('m')
```

## 🏗️ Development

This project uses Poetry for dependency management:

```bash
# Install dependencies
poetry install --with dev

# Run tests
poetry run pytest tests/ -v

# Lint code
poetry run pylint --rcfile=.pylintrc $(git ls-files '*.py') --fail-under=9.5
# Formatting

This project uses the Ruff VSCode extension for code formatting. When you save a Python file (Ctrl+S), Ruff automatically formats your code according to the configured rules.


```
