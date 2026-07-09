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

def caitlyn_profile_prioritizes_rapid_firecannon_after_two_cores():
    players = [
        {"team": "ORDER", "championName": "Caitlyn", "rawChampionName": "Caitlyn", "position": "BOTTOM", "level": 13, "scores": {"kills": 6, "deaths": 2, "assists": 5, "creepScore": 230}, "items": [{"itemID": 6672}, {"itemID": 3031}]},
        {"team": "CHAOS", "championName": "Ezreal", "rawChampionName": "Ezreal", "position": "BOTTOM", "level": 12, "scores": {"kills": 2, "deaths": 5, "assists": 4, "creepScore": 190}, "items": [{"itemID": 3004}, {"itemID": 3078}]},
    ]
    result = overlay.recommend(players[0], players, {"gold": 1800, "source": "test", "detail": "mock", "spent": 6500})
    assert_true(result[4][0]["item"]["id"] == 3094, f"Caitlyn should see Rapid Firecannon as 3rd core, got {result[4][0]['item']['name']}")


def lane_armor_stack_pushes_penetration_choice():
    players = [
        {"team": "ORDER", "championName": "Caitlyn", "rawChampionName": "Caitlyn", "position": "BOTTOM", "level": 14, "scores": {"kills": 7, "deaths": 2, "assists": 5, "creepScore": 245}, "items": [{"itemID": 6672}, {"itemID": 3031}]},
        {"team": "CHAOS", "championName": "Rammus", "rawChampionName": "Rammus", "position": "BOTTOM", "level": 15, "scores": {"kills": 5, "deaths": 1, "assists": 8, "creepScore": 205}, "items": [{"itemID": 3143}, {"itemID": 3110}, {"itemID": 3047}]},
        {"team": "CHAOS", "championName": "Lux", "rawChampionName": "Lux", "position": "MIDDLE", "level": 13, "scores": {"kills": 2, "deaths": 4, "assists": 7, "creepScore": 160}, "items": [{"itemID": 6655}]},
    ]
    result = overlay.recommend(players[0], players, {"gold": 2300, "source": "test", "detail": "mock", "spent": 6500})
    top = result[4][0]
    assert_true(top["item"]["id"] == 3036, f"Lord Dominik's Regards should lead into lane armor stack, got {top['item']['name']}")
    assert_true(any("라인 상대 방어력" in reason for reason in top["breakdown"]), top["breakdown"])


def off_path_crit_item_counts_as_core_progress():
    players = [
        {"team": "ORDER", "championName": "Caitlyn", "rawChampionName": "Caitlyn", "position": "BOTTOM", "level": 10, "scores": {"kills": 4, "deaths": 1, "assists": 3, "creepScore": 160}, "items": [{"itemID": 6676}]},
        {"team": "CHAOS", "championName": "Ezreal", "rawChampionName": "Ezreal", "position": "BOTTOM", "level": 10, "scores": {"kills": 1, "deaths": 4, "assists": 2, "creepScore": 140}, "items": [{"itemID": 3004}]},
    ]
    result = overlay.recommend(players[0], players, {"gold": 1500, "source": "test", "detail": "mock", "spent": 3000})
    assert_true(result[6] == 1, f"Collector should count as one marksman core-equivalent, got {result[6]}")
    assert_true(result[4][0]["item"]["id"] == 3031, f"Caitlyn should move toward Infinity Edge after off-path crit core, got {result[4][0]['item']['name']}")


def defensive_item_does_not_count_as_marksman_core_progress():
    players = [
        {"team": "ORDER", "championName": "Caitlyn", "rawChampionName": "Caitlyn", "position": "BOTTOM", "level": 10, "scores": {"kills": 2, "deaths": 4, "assists": 2, "creepScore": 135}, "items": [{"itemID": 3026}]},
        {"team": "CHAOS", "championName": "Ezreal", "rawChampionName": "Ezreal", "position": "BOTTOM", "level": 10, "scores": {"kills": 3, "deaths": 2, "assists": 4, "creepScore": 150}, "items": [{"itemID": 3004}]},
    ]
    result = overlay.recommend(players[0], players, {"gold": 1500, "source": "test", "detail": "mock", "spent": 3200})
    assert_true(result[6] == 0, f"Guardian Angel should not count as Caitlyn core progress, got {result[6]}")
    assert_true(result[4][0]["item"]["id"] == 6672, f"Caitlyn should still see Kraken as first core, got {result[4][0]['item']['name']}")


def jhin_profile_starts_youmuu_before_collector():
    players = [
        {"team": "ORDER", "championName": "Jhin", "rawChampionName": "Jhin", "position": "BOTTOM", "level": 9, "scores": {"kills": 4, "deaths": 1, "assists": 3, "creepScore": 135}, "items": [{"itemID": 3134}]},
        {"team": "CHAOS", "championName": "Jinx", "rawChampionName": "Jinx", "position": "BOTTOM", "level": 9, "scores": {"kills": 1, "deaths": 4, "assists": 2, "creepScore": 120}, "items": [{"itemID": 6672}]},
    ]
    result = overlay.recommend(players[0], players, {"gold": 1500, "source": "test", "detail": "mock", "spent": 1000})
    assert_true(result[4][0]["item"]["id"] == 3142, f"Jhin should start Youmuu path, got {result[4][0]['item']['name']}")

def shield_threat_surfaces_serpents_fang():
    players = [
        {"team": "ORDER", "championName": "Zed", "rawChampionName": "Zed", "position": "MIDDLE", "level": 13, "scores": {"kills": 7, "deaths": 3, "assists": 4, "creepScore": 170}, "items": [{"itemID": 3142}, {"itemID": 3134}]},
        {"team": "CHAOS", "championName": "Sett", "rawChampionName": "Sett", "position": "TOP", "level": 15, "scores": {"kills": 7, "deaths": 2, "assists": 5, "creepScore": 190}, "items": [{"itemID": 3053}, {"itemID": 3078}]},
        {"team": "CHAOS", "championName": "Karma", "rawChampionName": "Karma", "position": "UTILITY", "level": 12, "scores": {"kills": 1, "deaths": 3, "assists": 14, "creepScore": 35}, "items": [{"itemID": 2065}, {"itemID": 6616}]},
        {"team": "CHAOS", "championName": "Lulu", "rawChampionName": "Lulu", "position": "UTILITY", "level": 12, "scores": {"kills": 1, "deaths": 4, "assists": 16, "creepScore": 30}, "items": [{"itemID": 6616}, {"itemID": 3504}]},
    ]
    result = overlay.recommend(players[0], players, {"gold": 2500, "source": "test", "detail": "mock", "spent": 5600})
    serpents = [entry for entry in result[4] if entry["item"]["id"] == 6695]
    assert_true(serpents, f"Serpent's Fang should be visible into heavy shields, got {[entry['item']['name'] for entry in result[4]]}")
    assert_true(any("보호막 위협" in reason for reason in serpents[0]["breakdown"]), serpents[0]["breakdown"])


def fed_assassin_burst_pushes_stasis():
    players = [
        {"team": "ORDER", "championName": "Lux", "rawChampionName": "Lux", "position": "MIDDLE", "level": 12, "scores": {"kills": 3, "deaths": 4, "assists": 5, "creepScore": 150}, "items": [{"itemID": 6655}, {"itemID": 1052}]},
        {"team": "CHAOS", "championName": "Zed", "rawChampionName": "Zed", "position": "MIDDLE", "level": 15, "scores": {"kills": 12, "deaths": 1, "assists": 4, "creepScore": 220}, "items": [{"itemID": 3142}, {"itemID": 6701}, {"itemID": 6694}]},
        {"team": "CHAOS", "championName": "Kha'Zix", "rawChampionName": "KhaZix", "position": "JUNGLE", "level": 14, "scores": {"kills": 9, "deaths": 2, "assists": 6, "creepScore": 160}, "items": [{"itemID": 3142}, {"itemID": 3814}, {"itemID": 6695}]},
    ]
    result = overlay.recommend(players[0], players, {"gold": 2500, "source": "test", "detail": "mock", "spent": 4500})
    top = result[4][0]
    assert_true(top["item"]["id"] == 3157, f"Zhonya should lead into fed AD assassins, got {top['item']['name']}")
    assert_true(any("예상 폭딜" in reason for reason in top["breakdown"]), top["breakdown"])

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
        caitlyn_profile_prioritizes_rapid_firecannon_after_two_cores,
        lane_armor_stack_pushes_penetration_choice,
        off_path_crit_item_counts_as_core_progress,
        defensive_item_does_not_count_as_marksman_core_progress,
        jhin_profile_starts_youmuu_before_collector,
        shield_threat_surfaces_serpents_fang,
        fed_assassin_burst_pushes_stasis,
        stage_winrates_are_displayed,
    ]
    for test in tests:
        test()
        print(f"ok {test.__name__}")


if __name__ == "__main__":
    main()
