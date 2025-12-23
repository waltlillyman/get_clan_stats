# Clash Royale Clan Stats

Fetch Clash Royale clan member statistics from the Supercell API and automatically post them to Discord as an Excel spreadsheet.

## Features

- Fetches real-time clan member data from Clash Royale API
- Generates formatted Excel workbook with member stats
- Posts results directly to a Discord channel
- Runs as a containerized application via Docker Compose
- Designed for automated scheduling via cron jobs

## Setup

### Prerequisites

- Docker and Docker Compose
- Clash Royale API credentials (personal token)
- Discord webhook URL for the target channel

### Configuration

1. Copy environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   - `BEARER_TOKEN`: Your Clash Royale API token
   - `WEBHOOK_URL`: Your Discord webhook URL
   - `CLAN_TAG`: The clan tag (URL-encoded)
   - `WORKBOOK_NAME`: Output Excel filename
   - `WORKSHEET_NAME`: Name of the worksheet sheet

3. Build the Docker image:
   ```bash
   docker-compose build
   ```

## Usage

### Run Once

```bash
docker-compose run --rm get-clan-stats
```

### Schedule with Cron

Add to crontab:
```bash
23 6,18 * * * cd /path/to/get_clan_stats && docker-compose run --rm get-clan-stats >/dev/null 2>&1
```

This example runs at 6:23 AM and 6:23 PM daily.

## Files

- `settings.py` - Configuration loader (reads from environment variables)
- `fetch_stats.py` - Clash Royale API client
- `create_excel.py` - Excel spreadsheet generator
- `upload_discord.py` - Discord webhook uploader
- `get_clan_stats.py` - Main orchestrator
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Service configuration

## Security

Sensitive values are managed via environment variables in `.env` (git-ignored). The `.env.example` file provides a template with placeholder values.
