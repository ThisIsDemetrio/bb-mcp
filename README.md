# bb-mcp

Experimental and unofficial MCP server that wraps the [BuzzerBeater](https://play.buzzerbeater.com/) public API. It uses BuzzerBeater data but was not made by BuzzerBeater. It is read-only.

## Requirements

- Python 3.13+ and [uv](https://docs.astral.sh/uv/)
- A BuzzerBeater **Personal Access Token (PAT)**, created in the game under Settings → API & third-party apps → Personal tokens

## Tools

- `get_me`: your manager profile, team ids and granted token scopes (start here)
- `get_team`: club summary: name, country, league, arena, record
- `get_team_roster`: a club's players (skills only for your own club)
- `get_team_schedule`: a club's matches, oldest first
- `get_team_stats`: team statistics for a season, as averages or totals
- `get_team_arena`: arena seats and ticket prices
- `get_arena_attendance`: attendance and gate revenue of your own club
- `get_team_training`: your club's current training drill
- `get_team_training_history`: your club's past training sessions
- `get_team_staff`: your club's staff, levels and salaries
- `get_team_facilities`: your club's buildings and upkeep
- `get_team_economy`: your club's balance and transactions
- `get_team_salaries`: weekly player and staff salaries
- `scout_team`: a club's tactics over its recent games
- `get_player`: a player's page (skills only for your own players)
- `get_player_training`: training sessions of one of your players
- `search_market_players`: search the transfer list with filters
- `get_auction`: auction details of a listed player
- `get_match`: match header: teams, date, score by period
- `get_boxscore`: box score of a finished match
- `get_match_events`: play-by-play of a finished match, paged
- `get_match_shooting`: shot zones and attempts of a finished match
- `get_standings`: competition standings for a season
- `get_seasons`: list of seasons
- `get_countries`: list of countries
- `get_country_leagues`: leagues of a country, by level or division
- `get_country_national_teams`: senior and junior national teams of a country
- `get_national_team_roster`: a national team's called-up squad
- `get_national_team_training_history`: squad skill changes for a national team you coach

## Run

1. Copy `.env.example` to `.env` and set `BB_PAT` (the file explains each variable). `.env` is gitignored.
2. Install and start:

```sh
make sync
make start
```

The server speaks MCP over stdio, so on its own it just waits for a client. Your AI client normally starts it for you, as described below. In the examples, replace `/path/to/bb-mcp` with the absolute path of this folder.

## Add to Claude Code

```sh
claude mcp add bb-mcp -- uv --directory /path/to/bb-mcp run --env-file .env bb-mcp
```

Or put this in a `.mcp.json` at the root of your project:

```json
{
  "mcpServers": {
    "bb-mcp": {
      "command": "uv",
      "args": ["--directory", "/path/to/bb-mcp", "run", "--env-file", ".env", "bb-mcp"]
    }
  }
}
```

## Add to GitHub Copilot (VS Code)

Create `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "bb-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "/path/to/bb-mcp", "run", "--env-file", ".env", "bb-mcp"]
    }
  }
}
```

## Add to Codex

```sh
codex mcp add bb-mcp -- uv --directory /path/to/bb-mcp run --env-file .env bb-mcp
```

Or add this to `~/.codex/config.toml`:

```toml
[mcp_servers.bb-mcp]
command = "uv"
args = ["--directory", "/path/to/bb-mcp", "run", "--env-file", ".env", "bb-mcp"]
```
