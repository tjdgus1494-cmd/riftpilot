# Master+ Build Stats Collector

RiftPilot includes an optional local collector for Master+ build statistics. The collector can generate `data/master_plus_build_stats.json`, which the overlay can use for 1-core, 2-core, and 3-core build path comparison.

This data is not bundled as a production dataset. Users must generate it locally with their own Riot API key.

## Requirements

- Python 3
- Riot API key
- Network access to Riot APIs
- Enough API quota for League-V4, Match-V5, and timeline requests

## Basic Usage

```powershell
$env:RIOT_API_KEY = "RGAPI-..."
python collect_master_build_stats.py
```

The generated file is written to:

```text
data/master_plus_build_stats.json
```

The example schema is available at:

```text
data/master_plus_build_stats.example.json
```

The example file documents the shape of the data. It is not treated as a production dataset.

## Environment Variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `RIOT_API_KEY` | none | Required Riot API key. |
| `RIOT_PLATFORM` | `kr` | Platform routing value for League-V4 requests. |
| `RIOT_REGION` | `asia` | Regional routing value for Match-V5 requests. |
| `RIOT_QUEUE` | `RANKED_SOLO_5x5` | Queue used when reading high-tier league entries. |
| `RIOT_SUMMONER_LIMIT` | `80` | Maximum number of high-tier summoners to scan. |
| `RIOT_MATCH_COUNT` | `20` | Number of recent ranked matches requested per summoner. |
| `RIOT_PATCH` | empty | Optional patch filter, such as `16.13`. |

## What the Collector Does

1. Reads Master, Grandmaster, and Challenger entries from Riot League-V4.
2. Resolves summoner entries to PUUIDs when needed.
3. Requests ranked Match-V5 match IDs.
4. Reads match and timeline data.
5. Extracts finished item purchase sequences from timeline events.
6. Aggregates first, second, and third core item paths.
7. Writes local statistics for the overlay recommendation logic.

Generated rows can include win rate, pick rate, sample count, position, patch, and stage-level winrates when enough timeline data is available.

## Patch Filtering

Set `RIOT_PATCH` to keep only matches from a specific major/minor game version.

```powershell
$env:RIOT_PATCH = "16.13"
python collect_master_build_stats.py
```

This avoids mixing build statistics across patches, but it can reduce sample size.

## Current Limitations

- The collector depends on Riot API availability and rate limits.
- The generated data quality depends on the number of matches scanned.
- Small samples should not be treated as reliable build recommendations.
- The repository does not include a live, automatically refreshed high-tier dataset.
- The collector does not prove that a build is optimal; it provides optional context for the heuristic recommendation engine.
- Users should not commit private API keys or generated data that they do not intend to publish.
