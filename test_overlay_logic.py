#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import overlay


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def zed_recommends_ad_assassin_items():
    players = [
        {"team": "ORDER", "championName": "Zed", "rawChampionName": "Zed", "position": "MIDDLE", "level": 8, "scores": {"kills": 3, "deaths": 1, "assists": 2, "creepScore": 85}, "items": [{"itemID": 3134}]},
        {"team": "CHAOS", "championName": "Lux", "rawChampionName": "Lux", "position": "MIDDLE", "level": 8, "scores": {"kills": 1, "deaths": 3, "assists": 2, "creepScore": 80}, "items": [{"itemID": 3802}]},
    ]
    result = overlay.recommend(players[0], players, {"gold": 900, "source": "test", "detail": "mock", "spent": 1000})
    names = [entry["item"]["name"] for entry in result[4]]
    assert_true("요우무의 유령검" in names, f"Zed should see Youmuu first, got {names}")
    assert_true("라바돈의 죽음모자" not in names, f"Zed should not see AP mage items, got {names}")


def antiheal_accounts_for_allied_coverage():
    def recommend_with_allies(ally_items):
        players = [
            {"team": "ORDER", "championName": "Aphelios", "rawChampionName": "Aphelios", "position": "BOTTOM", "level": 15, "scores": {"kills": 8, "deaths": 3, "assists": 6, "creepScore": 260}, "items": [{"itemID": 6672}, {"itemID": 3031}, {"itemID": 3036}]},
            {"team": "ORDER", "championName": "Lux", "rawChampionName": "Lux", "position": "MIDDLE", "level": 14, "scores": {"kills": 3, "deaths": 3, "assists": 8, "creepScore": 180}, "items": [{"itemID": item_id} for item_id in ally_items[:1]]},
            {"team": "ORDER", "championName": "Darius", "rawChampionName": "Darius", "position": "TOP", "level": 15, "scores": {"kills": 3, "deaths": 4, "assists": 4, "creepScore": 210}, "items": [{"itemID": item_id} for item_id in ally_items[1:2]]},
            {"team": "CHAOS", "championName": "Aatrox", "rawChampionName": "Aatrox", "position": "TOP", "level": 16, "scores": {"kills": 10, "deaths": 2, "assists": 5, "creepScore": 220}, "items": [{"itemID": 3072}, {"itemID": 6610}, {"itemID": 3053}]},
            {"team": "CHAOS", "championName": "Vladimir", "rawChampionName": "Vladimir", "position": "MIDDLE", "level": 16, "scores": {"kills": 9, "deaths": 2, "assists": 4, "creepScore": 220}, "items": [{"itemID": 3089}, {"itemID": 3102}, {"itemID": 6653}]},
        ]
        return overlay.recommend(players[0], players, {"gold": 1800, "source": "test", "detail": "mock", "spent": 9100})

    no_coverage = recommend_with_allies([])
    covered = recommend_with_allies([3165, 3075])
    assert_true(no_coverage[4][0]["item"]["id"] == 3033, "Mortal Reminder should lead when team has no antiheal")
    assert_true(covered[4][0]["item"]["id"] != 3033, "Mortal Reminder should drop when two allies already have antiheal")


def crit_threat_pushes_anti_crit_items():
    players = [
        {"team": "ORDER", "championName": "Tahm Kench", "rawChampionName": "TahmKench", "position": "TOP", "level": 13, "scores": {"kills": 2, "deaths": 3, "assists": 7, "creepScore": 150}, "items": [{"itemID": 3068}, {"itemID": 6665}]},
        {"team": "CHAOS", "championName": "Yasuo", "rawChampionName": "Yasuo", "position": "MIDDLE", "level": 15, "scores": {"kills": 9, "deaths": 2, "assists": 4, "creepScore": 210}, "items": [{"itemID": 3031}, {"itemID": 3046}]},
        {"team": "CHAOS", "championName": "Draven", "rawChampionName": "Draven", "position": "BOTTOM", "level": 14, "scores": {"kills": 8, "deaths": 3, "assists": 2, "creepScore": 190}, "items": [{"itemID": 3031}, {"itemID": 6676}]},
    ]
    result = overlay.recommend(players[0], players, {"gold": 1300, "source": "test", "detail": "mock", "spent": 5900})
    names = [entry["item"]["name"] for entry in result[4]]
    assert_true(names[0] in {"판금 장화", "란두인의 예언"}, f"Anti-crit item should lead, got {names}")


def stage_winrates_are_displayed():
    meta = [{
        "core": [6655, 4645, 3089],
        "winrate": 0.544,
        "games": 180,
        "stageWinrates": {
            1: {"winrate": 0.542, "games": 240},
            2: {"winrate": 0.553, "games": 190},
            3: {"winrate": 0.544, "games": 180},
        },
    }]
    text = overlay.format_meta_comparison(meta, set())
    assert_true("1C 54.2%" in text and "2C 55.3%" in text and "3C 54.4%" in text, text)


def main():
    tests = [
        zed_recommends_ad_assassin_items,
        antiheal_accounts_for_allied_coverage,
        crit_threat_pushes_anti_crit_items,
        stage_winrates_are_displayed,
    ]
    for test in tests:
        test()
        print(f"ok {test.__name__}")


if __name__ == "__main__":
    main()
