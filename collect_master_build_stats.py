#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Collect Master+ 1/2/3-core build order stats with Riot's official API.

Required environment:
  RIOT_API_KEY=RGAPI-...

Optional environment:
  RIOT_PLATFORM=kr
  RIOT_REGION=asia
  RIOT_SUMMONER_LIMIT=80
  RIOT_MATCH_COUNT=20
  RIOT_PATCH=16.13
"""

import collections
import datetime as dt
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = APP_DIR / "data" / "master_plus_build_stats.json"

API_KEY = os.environ.get("RIOT_API_KEY", "").strip()
PLATFORM = os.environ.get("RIOT_PLATFORM", "kr").strip()
REGION = os.environ.get("RIOT_REGION", "asia").strip()
QUEUE = os.environ.get("RIOT_QUEUE", "RANKED_SOLO_5x5").strip()
SUMMONER_LIMIT = int(os.environ.get("RIOT_SUMMONER_LIMIT", "80"))
MATCH_COUNT = int(os.environ.get("RIOT_MATCH_COUNT", "20"))
PATCH_FILTER = os.environ.get("RIOT_PATCH", "").strip()
SOLO_QUEUE_ID = 420


def request_json(url, token=True, retry=3):
    headers = {"User-Agent": "codex-lol-item-recommender/0.1"}
    if token:
        headers["X-Riot-Token"] = API_KEY
    request = urllib.request.Request(url, headers=headers)
    for attempt in range(retry):
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            if error.code == 429 and attempt < retry - 1:
                wait = int(error.headers.get("Retry-After", "2"))
                time.sleep(max(1, wait))
                continue
            raise


def riot_get(path, regional=False, params=None):
    host = REGION if regional else PLATFORM
    query = urllib.parse.urlencode(params or {})
    url = f"https://{host}.api.riotgames.com{path}"
    if query:
        url += f"?{query}"
    return request_json(url)


def load_finished_item_ids():
    versions = request_json("https://ddragon.leagueoflegends.com/api/versions.json", token=False)
    version = versions[0]
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
    payload = request_json(url, token=False)
    finished = set()
    names = {}
    for raw_id, item in (payload.get("data") or {}).items():
        item_id = int(raw_id)
        tags = set(item.get("tags") or [])
        gold = item.get("gold") or {}
        maps = item.get("maps") or {}
        if maps.get("11") is False:
            continue
        if tags.intersection({"Boots", "Consumable", "Trinket"}):
            continue
        if gold.get("total", 0) < 1800:
            continue
        if item.get("into"):
            continue
        finished.add(item_id)
        names[item_id] = item.get("name", str(item_id))
    return finished, names, version


def league_entries():
    endpoints = [
        "/lol/league/v4/challengerleagues/by-queue/{queue}",
        "/lol/league/v4/grandmasterleagues/by-queue/{queue}",
        "/lol/league/v4/masterleagues/by-queue/{queue}",
    ]
    entries = []
    for endpoint in endpoints:
        payload = riot_get(endpoint.format(queue=QUEUE))
        tier = payload.get("tier") or "MASTER+"
        for entry in payload.get("entries", []):
            entry = dict(entry)
            entry["tier"] = tier
            entries.append(entry)
    entries.sort(key=lambda entry: entry.get("leaguePoints", 0), reverse=True)
    return entries[:SUMMONER_LIMIT]


def entry_puuid(entry):
    if entry.get("puuid"):
        return entry["puuid"]
    summoner_id = entry.get("summonerId")
    if not summoner_id:
        return None
    payload = riot_get(f"/lol/summoner/v4/summoners/{urllib.parse.quote(summoner_id)}")
    return payload.get("puuid")


def match_ids_for_puuid(puuid):
    return riot_get(
        f"/lol/match/v5/matches/by-puuid/{urllib.parse.quote(puuid)}/ids",
        regional=True,
        params={"queue": SOLO_QUEUE_ID, "type": "ranked", "start": 0, "count": MATCH_COUNT},
    )


def participant_core_sequence(timeline, participant_id, finished_item_ids):
    sequence = []
    for frame in timeline.get("info", {}).get("frames", []):
        for event in frame.get("events", []):
            if event.get("participantId") != participant_id:
                continue
            event_type = event.get("type")
            item_id = event.get("itemId")
            if event_type == "ITEM_PURCHASED" and item_id in finished_item_ids and item_id not in sequence:
                sequence.append(item_id)
            elif event_type in {"ITEM_SOLD", "ITEM_DESTROYED"} and item_id in sequence:
                sequence = [value for value in sequence if value != item_id]
            elif event_type == "ITEM_UNDO":
                before_id = event.get("beforeId")
                if before_id in sequence:
                    sequence = [value for value in sequence if value != before_id]
            if len(sequence) >= 3:
                return tuple(sequence[:3])
    return tuple(sequence[:3])


def collect():
    if not API_KEY:
        raise SystemExit("RIOT_API_KEY 환경 변수가 필요합니다.")

    finished_item_ids, item_names, ddragon_version = load_finished_item_ids()
    stats = collections.defaultdict(lambda: {"wins": 0, "games": 0})
    prefix_stats = collections.defaultdict(lambda: {"wins": 0, "games": 0})
    totals = collections.Counter()
    seen_matches = set()
    patches = collections.Counter()
    skipped_patch = 0

    for index, entry in enumerate(league_entries(), start=1):
        puuid = entry_puuid(entry)
        if not puuid:
            continue
        print(f"[{index}/{SUMMONER_LIMIT}] {entry.get('summonerName', 'summoner')} matches...")
        for match_id in match_ids_for_puuid(puuid):
            if match_id in seen_matches:
                continue
            seen_matches.add(match_id)
            match = riot_get(f"/lol/match/v5/matches/{match_id}", regional=True)
            info = match.get("info") or {}
            if info.get("queueId") != SOLO_QUEUE_ID or info.get("mapId") != 11:
                continue
            timeline = riot_get(f"/lol/match/v5/matches/{match_id}/timeline", regional=True)
            patch = ".".join(str(info.get("gameVersion", "")).split(".")[:2])
            if patch:
                patches[patch] += 1
            if PATCH_FILTER and patch != PATCH_FILTER:
                skipped_patch += 1
                continue
            for participant in info.get("participants", []):
                participant_id = participant.get("participantId")
                core = participant_core_sequence(timeline, participant_id, finished_item_ids)
                if len(core) < 2:
                    continue
                champion = participant.get("championName")
                position = participant.get("teamPosition") or "ANY"
                group_key = (champion, position)
                totals[group_key] += 1
                stat_key = (champion, position, core)
                stats[stat_key]["games"] += 1
                stats[stat_key]["wins"] += 1 if participant.get("win") else 0
                for stage in range(1, min(3, len(core)) + 1):
                    prefix_key = (champion, position, core[:stage])
                    prefix_stats[prefix_key]["games"] += 1
                    prefix_stats[prefix_key]["wins"] += 1 if participant.get("win") else 0

    champions = {}
    for (champion, position, core), values in stats.items():
        games = values["games"]
        if games < 3:
            continue
        wins = values["wins"]
        stage_winrates = {}
        for stage in range(1, min(3, len(core)) + 1):
            prefix = core[:stage]
            prefix_values = prefix_stats.get((champion, position, prefix), {"wins": 0, "games": 0})
            prefix_games = prefix_values["games"]
            prefix_wins = prefix_values["wins"]
            stage_winrates[str(stage)] = {
                "wins": prefix_wins,
                "games": prefix_games,
                "winrate": round(prefix_wins / prefix_games, 4) if prefix_games else None,
            }
        champion_block = champions.setdefault(champion, {})
        position_rows = champion_block.setdefault(position, [])
        total = max(1, totals[(champion, position)])
        position_rows.append({
            "core": list(core),
            "itemNames": [item_names.get(item_id, str(item_id)) for item_id in core],
            "wins": wins,
            "games": games,
            "winrate": round(wins / games, 4),
            "stageWinrates": stage_winrates,
            "pickrate": round(games / total, 4),
            "position": position,
            "rank": "MASTER+",
        })

    for champion_block in champions.values():
        for rows in champion_block.values():
            rows.sort(key=lambda row: (row["games"], row["winrate"]), reverse=True)
            del rows[8:]

    payload = {
        "version": 1,
        "source": "riot-match-v5-local-collector",
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "patch": patches.most_common(1)[0][0] if patches else "unknown",
        "rank": "MASTER+",
        "platform": PLATFORM,
        "region": REGION,
        "queue": QUEUE,
        "ddragonVersion": ddragon_version,
        "matchesScanned": len(seen_matches),
        "patchFilter": PATCH_FILTER or None,
        "matchesSkippedByPatch": skipped_patch,
        "champions": champions,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    print(f"saved {OUTPUT_PATH}")


if __name__ == "__main__":
    collect()
