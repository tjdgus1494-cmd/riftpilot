#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math
import os
import queue
import threading
import time
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


API_URL = "http://127.0.0.1:5177/api/replay"
POLL_MS = 1400
APP_DIR = Path(__file__).resolve().parent
BUILD_STATS_PATH = APP_DIR / "data" / "master_plus_build_stats.json"
LATEST_RECOMMENDATION_PATH = APP_DIR / "data" / "latest_recommendation.json"

COLORS = {
    "bg": "#111712",
    "panel": "#182019",
    "panel_alt": "#202a22",
    "line": "#3a473c",
    "text": "#eef4ed",
    "muted": "#aeb9b0",
    "green": "#2f7d65",
    "gold": "#bd861e",
    "red": "#bd4a3a",
}

CHAMPION_HINTS = {
    "Aatrox": {"archetype": "fighter", "damage": "physical", "heal": 4, "tank": 2},
    "Ahri": {"archetype": "mage", "damage": "magic", "burst": 3, "cc": 2},
    "Akali": {"archetype": "assassin", "damage": "magic", "burst": 4},
    "Alistar": {"archetype": "support", "damage": "magic", "tank": 4, "cc": 5},
    "Amumu": {"archetype": "tank", "damage": "magic", "tank": 4, "cc": 4},
    "Aphelios": {"archetype": "marksman", "damage": "physical", "burst": 2},
    "Ashe": {"archetype": "marksman", "damage": "physical", "cc": 3},
    "Azir": {"archetype": "mage", "damage": "magic", "burst": 2},
    "Blitzcrank": {"archetype": "support", "damage": "magic", "tank": 3, "cc": 4},
    "Brand": {"archetype": "mage", "damage": "magic", "burst": 4},
    "Caitlyn": {"archetype": "marksman", "damage": "physical", "burst": 2},
    "Camille": {"archetype": "fighter", "damage": "physical", "burst": 3, "tank": 2},
    "Darius": {"archetype": "fighter", "damage": "physical", "heal": 2, "tank": 2},
    "Draven": {"archetype": "marksman", "damage": "physical", "burst": 4},
    "Ekko": {"archetype": "assassin", "damage": "magic", "burst": 4},
    "Ezreal": {"archetype": "marksman", "damage": "physical", "burst": 2},
    "Fiora": {"archetype": "fighter", "damage": "physical", "heal": 3, "burst": 2},
    "Galio": {"archetype": "tank", "damage": "magic", "tank": 3, "cc": 4},
    "Garen": {"archetype": "fighter", "damage": "physical", "tank": 3},
    "Graves": {"archetype": "marksman", "damage": "physical", "burst": 3},
    "Hwei": {"archetype": "mage", "damage": "magic", "burst": 4, "cc": 2},
    "Irelia": {"archetype": "fighter", "damage": "physical", "heal": 2, "burst": 3},
    "Janna": {"archetype": "support", "damage": "magic", "cc": 3},
    "Jax": {"archetype": "fighter", "damage": "physical", "tank": 2, "burst": 2},
    "Jayce": {"archetype": "fighter", "damage": "physical", "burst": 3},
    "Jhin": {"archetype": "marksman", "damage": "physical", "burst": 3, "cc": 2},
    "Jinx": {"archetype": "marksman", "damage": "physical"},
    "KaiSa": {"archetype": "marksman", "damage": "mixed", "burst": 3},
    "Karma": {"archetype": "support", "damage": "magic", "cc": 2},
    "Kassadin": {"archetype": "assassin", "damage": "magic", "burst": 4},
    "Katarina": {"archetype": "assassin", "damage": "magic", "heal": 2, "burst": 5},
    "Kayle": {"archetype": "mage", "damage": "mixed", "burst": 2},
    "KhaZix": {"archetype": "assassin", "damage": "physical", "burst": 5},
    "LeeSin": {"archetype": "fighter", "damage": "physical", "burst": 3},
    "Leona": {"archetype": "support", "damage": "magic", "tank": 4, "cc": 5},
    "Lillia": {"archetype": "mage", "damage": "magic", "cc": 2},
    "Lulu": {"archetype": "support", "damage": "magic", "cc": 2},
    "Lucian": {"archetype": "marksman", "damage": "physical", "burst": 3},
    "Lux": {"archetype": "mage", "damage": "magic", "burst": 4, "cc": 2},
    "Malphite": {"archetype": "tank", "damage": "magic", "tank": 4, "cc": 3},
    "MasterYi": {"archetype": "fighter", "damage": "physical", "heal": 2, "burst": 3},
    "Mel": {"archetype": "mage", "damage": "magic", "burst": 4},
    "Milio": {"archetype": "support", "damage": "magic"},
    "MissFortune": {"archetype": "marksman", "damage": "physical", "burst": 3},
    "Mordekaiser": {"archetype": "fighter", "damage": "magic", "heal": 2, "tank": 3},
    "Morgana": {"archetype": "mage", "damage": "magic", "cc": 3},
    "Nami": {"archetype": "support", "damage": "magic", "cc": 3},
    "Nautilus": {"archetype": "support", "damage": "magic", "tank": 4, "cc": 5},
    "Nidalee": {"archetype": "mage", "damage": "magic", "heal": 2, "burst": 3},
    "Orianna": {"archetype": "mage", "damage": "magic", "burst": 3},
    "Ornn": {"archetype": "tank", "damage": "magic", "tank": 5, "cc": 4},
    "Pyke": {"archetype": "support", "damage": "physical", "burst": 4, "cc": 3},
    "Qiyana": {"archetype": "assassin", "damage": "physical", "burst": 5, "cc": 2},
    "Rakan": {"archetype": "support", "damage": "magic", "cc": 4},
    "Rammus": {"archetype": "tank", "damage": "magic", "tank": 5, "cc": 4},
    "Rell": {"archetype": "support", "damage": "magic", "tank": 4, "cc": 5},
    "Renekton": {"archetype": "fighter", "damage": "physical", "heal": 2, "tank": 2},
    "Riven": {"archetype": "fighter", "damage": "physical", "burst": 3, "cc": 2},
    "Samira": {"archetype": "marksman", "damage": "physical", "heal": 2, "burst": 4},
    "Senna": {"archetype": "support", "damage": "physical", "heal": 2},
    "Seraphine": {"archetype": "support", "damage": "magic", "cc": 3},
    "Sett": {"archetype": "fighter", "damage": "physical", "tank": 3, "cc": 2},
    "Shen": {"archetype": "tank", "damage": "mixed", "tank": 4, "cc": 3},
    "Sion": {"archetype": "tank", "damage": "physical", "tank": 5, "cc": 3},
    "Sivir": {"archetype": "marksman", "damage": "physical"},
    "Sylas": {"archetype": "fighter", "damage": "magic", "heal": 4, "burst": 3},
    "Syndra": {"archetype": "mage", "damage": "magic", "burst": 5, "cc": 2},
    "TahmKench": {"archetype": "tank", "damage": "magic", "tank": 5, "cc": 2},
    "Talon": {"archetype": "assassin", "damage": "physical", "burst": 5},
    "Thresh": {"archetype": "support", "damage": "magic", "tank": 2, "cc": 4},
    "Tristana": {"archetype": "marksman", "damage": "physical", "burst": 3},
    "Tryndamere": {"archetype": "fighter", "damage": "physical", "heal": 2, "burst": 3},
    "TwistedFate": {"archetype": "mage", "damage": "magic", "cc": 2},
    "Varus": {"archetype": "marksman", "damage": "mixed", "burst": 3, "cc": 2},
    "Vayne": {"archetype": "marksman", "damage": "physical", "burst": 3},
    "Veigar": {"archetype": "mage", "damage": "magic", "burst": 5, "cc": 2},
    "Viego": {"archetype": "fighter", "damage": "physical", "heal": 2, "burst": 3},
    "Vi": {"archetype": "fighter", "damage": "physical", "burst": 3, "cc": 3},
    "Viktor": {"archetype": "mage", "damage": "magic", "burst": 4},
    "Vladimir": {"archetype": "mage", "damage": "magic", "heal": 5, "burst": 3},
    "Yasuo": {"archetype": "fighter", "damage": "physical", "burst": 3},
    "Yone": {"archetype": "fighter", "damage": "mixed", "burst": 4},
    "Yunara": {"archetype": "marksman", "damage": "physical", "burst": 2},
    "Yuumi": {"archetype": "support", "damage": "magic", "heal": 4},
    "Zed": {"archetype": "assassin", "damage": "physical", "burst": 5},
    "Ziggs": {"archetype": "mage", "damage": "magic", "burst": 3},
    "Zilean": {"archetype": "support", "damage": "magic", "cc": 2},
    "Zoe": {"archetype": "mage", "damage": "magic", "burst": 5},
    "Zyra": {"archetype": "mage", "damage": "magic", "cc": 3},
}

ITEM_CANDIDATES = [
    {"id": 3006, "name": "광전사의 군화", "cost": 1100, "roles": ["marksman", "fighter"], "tags": ["boots", "attackSpeed", "tempo"], "priority": 42},
    {"id": 3047, "name": "판금 장화", "cost": 1200, "roles": ["marksman", "fighter", "tank", "support"], "tags": ["boots", "armor", "antiAuto", "defense"], "priority": 42},
    {"id": 3111, "name": "헤르메스의 발걸음", "cost": 1250, "roles": ["mage", "assassin", "fighter", "tank", "support"], "tags": ["boots", "magicResist", "tenacity", "defense"], "priority": 42},
    {"id": 3020, "name": "마법사의 신발", "cost": 1100, "roles": ["mage", "assassin"], "tags": ["boots", "magicPen", "tempo"], "priority": 38},
    {"id": 3158, "name": "명석함의 아이오니아 장화", "cost": 900, "roles": ["mage", "fighter", "support", "assassin"], "tags": ["boots", "haste", "utility"], "priority": 36},
    {"id": 3031, "name": "무한의 대검", "cost": 3500, "roles": ["marksman"], "tags": ["attackDamage", "crit", "burst", "scaling"], "priority": 80},
    {"id": 6672, "name": "크라켄 학살자", "cost": 3000, "roles": ["marksman", "fighter"], "tags": ["attackDamage", "attackSpeed", "antiTank", "duel", "tempo"], "priority": 78},
    {"id": 3033, "name": "필멸자의 운명", "cost": 3000, "roles": ["marksman", "fighter"], "tags": ["attackDamage", "crit", "antiheal", "armorPen"], "priority": 62},
    {"id": 3036, "name": "도미닉 경의 인사", "cost": 3300, "roles": ["marksman"], "tags": ["attackDamage", "crit", "armorPen", "antiTank"], "priority": 65},
    {"id": 3072, "name": "피바라기", "cost": 3400, "roles": ["marksman", "fighter"], "tags": ["attackDamage", "lifesteal", "shield", "defense"], "priority": 58},
    {"id": 3026, "name": "수호 천사", "cost": 3200, "roles": ["marksman", "assassin", "fighter"], "tags": ["attackDamage", "armor", "antiBurst", "defense"], "priority": 54},
    {"id": 6676, "name": "징수의 총", "cost": 3000, "roles": ["marksman", "assassin"], "tags": ["attackDamage", "crit", "execute", "burst"], "components": [1037, 3134, 1018], "priority": 69},
    {"id": 3004, "name": "마나무네", "cost": 2900, "roles": ["marksman", "fighter"], "tags": ["attackDamage", "mana", "haste", "scaling", "core"], "components": [3070, 3133, 1036], "priority": 72},
    {"id": 3094, "name": "고속 연사포", "cost": 2650, "roles": ["marksman"], "tags": ["attackSpeed", "crit", "range", "poke"], "components": [3086, 3144], "priority": 55},
    {"id": 3085, "name": "루난의 허리케인", "cost": 2650, "roles": ["marksman"], "tags": ["attackSpeed", "crit", "teamfight", "waveclear"], "components": [3086, 3144], "priority": 55},
    {"id": 3046, "name": "유령 무희", "cost": 2650, "roles": ["marksman", "fighter"], "tags": ["attackSpeed", "crit", "duel", "speed"], "components": [1042, 3086, 1042], "priority": 56},
    {"id": 3089, "name": "라바돈의 죽음모자", "cost": 3500, "roles": ["mage", "assassin"], "tags": ["abilityPower", "burst", "scaling"], "priority": 80},
    {"id": 3135, "name": "공허의 지팡이", "cost": 3000, "roles": ["mage"], "tags": ["abilityPower", "magicPen", "antiTank"], "priority": 66},
    {"id": 3165, "name": "모렐로노미콘", "cost": 2850, "roles": ["mage", "support"], "tags": ["abilityPower", "antiheal", "haste"], "components": [3916, 1026], "priority": 58},
    {"id": 3157, "name": "존야의 모래시계", "cost": 3250, "roles": ["mage", "assassin", "support"], "tags": ["abilityPower", "armor", "antiBurst", "stasis", "defense"], "priority": 64},
    {"id": 3100, "name": "리치베인", "cost": 2900, "roles": ["mage", "assassin"], "tags": ["abilityPower", "haste", "burst", "spellblade", "core"], "components": [3057, 1026], "priority": 74},
    {"id": 6655, "name": "루덴의 메아리", "cost": 2750, "roles": ["mage"], "tags": ["abilityPower", "mana", "haste", "burst", "core"], "components": [3802, 1026], "priority": 78},
    {"id": 4645, "name": "그림자불꽃", "cost": 3200, "roles": ["mage", "assassin"], "tags": ["abilityPower", "magicPen", "burst", "core"], "components": [2508, 1026], "priority": 74},
    {"id": 4628, "name": "지평선의 초점", "cost": 2700, "roles": ["mage"], "tags": ["abilityPower", "haste", "burst"], "components": [1052, 1026], "priority": 62},
    {"id": 6653, "name": "리안드리의 고통", "cost": 3000, "roles": ["mage"], "tags": ["abilityPower", "health", "antiTank", "burn"], "priority": 67},
    {"id": 3102, "name": "밴시의 장막", "cost": 3000, "roles": ["mage"], "tags": ["abilityPower", "magicResist", "antiBurst", "defense"], "priority": 56},
    {"id": 3071, "name": "칠흑의 양날 도끼", "cost": 3000, "roles": ["fighter", "assassin"], "tags": ["attackDamage", "health", "haste", "armorShred", "antiTank"], "priority": 73},
    {"id": 3078, "name": "삼위일체", "cost": 3333, "roles": ["fighter"], "tags": ["attackDamage", "health", "haste", "duel", "spellblade", "core"], "components": [3057, 3044, 1036], "priority": 84},
    {"id": 6692, "name": "월식", "cost": 2900, "roles": ["fighter", "assassin"], "tags": ["attackDamage", "shield", "duel", "antiBurst", "core"], "components": [3133, 1036], "priority": 72},
    {"id": 6610, "name": "갈라진 하늘", "cost": 3100, "roles": ["fighter", "tank"], "tags": ["attackDamage", "health", "healingAmp", "duel", "defense"], "components": [1037, 3044], "priority": 68},
    {"id": 3161, "name": "쇼진의 창", "cost": 3100, "roles": ["fighter"], "tags": ["attackDamage", "health", "haste", "scaling"], "components": [3133, 3067], "priority": 66},
    {"id": 3074, "name": "굶주린 히드라", "cost": 3300, "roles": ["fighter", "assassin"], "tags": ["attackDamage", "lifesteal", "waveclear", "duel"], "components": [1053, 1037], "priority": 62},
    {"id": 3153, "name": "몰락한 왕의 검", "cost": 3200, "roles": ["marksman", "fighter"], "tags": ["attackDamage", "attackSpeed", "lifesteal", "antiTank", "duel"], "components": [1053, 1043], "priority": 67},
    {"id": 3091, "name": "마법사의 최후", "cost": 2800, "roles": ["marksman", "fighter"], "tags": ["attackSpeed", "magicResist", "duel", "defense"], "components": [1043, 1057], "priority": 58},
    {"id": 3053, "name": "스테락의 도전", "cost": 3200, "roles": ["fighter", "tank"], "tags": ["attackDamage", "health", "shield", "antiBurst", "defense"], "priority": 63},
    {"id": 6333, "name": "죽음의 무도", "cost": 3300, "roles": ["fighter", "assassin"], "tags": ["attackDamage", "armor", "antiBurst", "haste"], "priority": 60},
    {"id": 3156, "name": "맬모셔스의 아귀", "cost": 3100, "roles": ["fighter", "assassin", "marksman"], "tags": ["attackDamage", "magicResist", "shield", "antiBurst"], "priority": 58},
    {"id": 3142, "name": "요우무의 유령검", "cost": 2800, "roles": ["assassin", "fighter"], "tags": ["attackDamage", "lethality", "speed", "burst", "core"], "components": [3134, 6690, 1036], "priority": 78},
    {"id": 3814, "name": "밤의 끝자락", "cost": 3000, "roles": ["assassin", "fighter"], "tags": ["attackDamage", "lethality", "spellShield", "antiBurst", "defense"], "components": [3134, 2021], "priority": 62},
    {"id": 6694, "name": "세릴다의 원한", "cost": 3000, "roles": ["assassin", "fighter"], "tags": ["attackDamage", "haste", "armorPen", "antiTank", "slow"], "components": [3133, 3035], "priority": 66},
    {"id": 6695, "name": "독사의 송곳니", "cost": 2500, "roles": ["assassin", "fighter"], "tags": ["attackDamage", "lethality", "antiShield"], "components": [3134, 1037], "priority": 54},
    {"id": 6701, "name": "기회", "cost": 2700, "roles": ["assassin"], "tags": ["attackDamage", "lethality", "speed", "burst", "core"], "components": [1037, 3134, 1036], "priority": 72},
    {"id": 3075, "name": "가시 갑옷", "cost": 2700, "roles": ["tank", "support", "fighter"], "tags": ["armor", "antiheal", "antiAuto", "defense"], "priority": 67},
    {"id": 3068, "name": "태양불꽃 방패", "cost": 2700, "roles": ["tank", "fighter"], "tags": ["health", "armor", "waveclear", "damage"], "priority": 62},
    {"id": 4401, "name": "대자연의 힘", "cost": 2800, "roles": ["tank", "fighter", "support"], "tags": ["magicResist", "health", "speed", "defense"], "priority": 64},
    {"id": 3143, "name": "란두인의 예언", "cost": 2700, "roles": ["tank", "fighter", "support"], "tags": ["armor", "health", "antiCrit", "antiAuto", "defense"], "priority": 61},
    {"id": 3110, "name": "얼어붙은 심장", "cost": 2500, "roles": ["tank", "support", "fighter"], "tags": ["armor", "haste", "antiAuto", "defense"], "priority": 58},
    {"id": 3065, "name": "정령의 형상", "cost": 2900, "roles": ["tank", "fighter"], "tags": ["magicResist", "health", "healingAmp", "defense"], "priority": 57},
    {"id": 6665, "name": "작쇼", "cost": 3200, "roles": ["tank", "fighter"], "tags": ["armor", "magicResist", "health", "scaling", "defense"], "priority": 69},
    {"id": 3190, "name": "강철의 솔라리 펜던트", "cost": 2200, "roles": ["support", "tank"], "tags": ["armor", "magicResist", "shield", "utility", "teamfight"], "priority": 64},
    {"id": 3107, "name": "구원", "cost": 2300, "roles": ["support"], "tags": ["healShield", "utility", "teamfight"], "priority": 62},
    {"id": 6617, "name": "월석 재생기", "cost": 2200, "roles": ["support"], "tags": ["healShield", "abilityPower", "teamfight"], "priority": 63},
    {"id": 3222, "name": "미카엘의 축복", "cost": 2300, "roles": ["support"], "tags": ["magicResist", "cleanse", "healShield", "utility"], "priority": 58},
    {"id": 3504, "name": "불타는 향로", "cost": 2200, "roles": ["support"], "tags": ["healShield", "attackSpeed", "utility"], "priority": 56},
]

ITEM_COSTS = {
    1001: 300, 1011: 900, 1018: 600, 1026: 850, 1031: 800, 1033: 450,
    1036: 350, 1037: 875, 1038: 1300, 1042: 300, 1043: 700, 1052: 400,
    1053: 900, 1055: 450, 1056: 400, 1057: 900, 1058: 1250, 2003: 50,
    2022: 250, 2031: 150, 2420: 750, 2422: 300, 3004: 2900, 3006: 1100, 3020: 1100,
    3026: 3200, 3031: 3500, 3033: 3000, 3035: 1450, 3036: 3300, 3044: 1100,
    3046: 2650, 3047: 1200, 3053: 3200, 3057: 900, 3065: 2900, 3067: 800, 3068: 2700,
    3070: 400, 3071: 3000, 3072: 3400, 3074: 3300, 3075: 2700, 3078: 3333,
    3085: 2650, 3086: 1200, 3089: 3500, 3091: 2800, 3094: 2650, 3100: 2900, 3102: 3000, 3107: 2300, 3110: 2500,
    3111: 1250, 3133: 1100, 3134: 1000, 3135: 3000, 3143: 2700, 3144: 600, 3153: 3200,
    3156: 3100, 3157: 3250, 3158: 900, 3161: 3100, 3190: 2200,
    3222: 2300, 3504: 2200, 3802: 1200, 3916: 800, 4401: 2800, 4628: 2700,
    4645: 3200, 6333: 3300, 6610: 3100, 6617: 2200, 6653: 3000, 6655: 2750,
    6665: 3200, 6670: 1300, 6672: 3000, 6676: 3000,
    6690: 775, 6692: 2900, 6694: 3000, 6695: 2500, 6701: 2700,
}

COMPONENT_ITEMS = {
    1001: {"name": "장화", "cost": 300},
    1011: {"name": "거인의 허리띠", "cost": 900},
    1018: {"name": "민첩성의 망토", "cost": 600},
    1026: {"name": "방출의 마법봉", "cost": 850},
    1031: {"name": "쇠사슬 조끼", "cost": 800},
    1033: {"name": "마법무효화의 망토", "cost": 450},
    1036: {"name": "롱소드", "cost": 350},
    1037: {"name": "곡괭이", "cost": 875},
    1038: {"name": "B. F. 대검", "cost": 1300},
    1042: {"name": "단검", "cost": 300},
    1043: {"name": "곡궁", "cost": 700},
    1052: {"name": "증폭의 고서", "cost": 400},
    1053: {"name": "흡혈의 낫", "cost": 900},
    1057: {"name": "음전자 망토", "cost": 900},
    1058: {"name": "쓸데없이 큰 지팡이", "cost": 1250},
    2022: {"name": "빛나는 티끌", "cost": 250},
    2021: {"name": "땅굴 채굴기", "cost": 1150},
    2420: {"name": "초시계", "cost": 750},
    3035: {"name": "최후의 속삭임", "cost": 1450},
    3070: {"name": "여신의 눈물", "cost": 400},
    3086: {"name": "열정의 검", "cost": 1200},
    3044: {"name": "탐식의 망치", "cost": 1100},
    3057: {"name": "광휘의 검", "cost": 900},
    3067: {"name": "점화석", "cost": 800},
    3133: {"name": "콜필드의 전투 망치", "cost": 1100},
    3134: {"name": "톱날 단검", "cost": 1000},
    3144: {"name": "정찰병의 새총", "cost": 600},
    2508: {"name": "운명의 재", "cost": 900},
    3802: {"name": "사라진 양피지", "cost": 1200},
    3916: {"name": "망각의 구", "cost": 800},
    4630: {"name": "역병의 보석", "cost": 1100},
    6670: {"name": "절정의 화살", "cost": 1300},
    6690: {"name": "꽁지깃", "cost": 775},
}

BUILD_PROFILES = {
    "Camille": {
        "core": [3078, 6610, 3053, 6333],
        "situational": [3156, 3071, 4401, 3143],
        "boots": {"physical": 3047, "magic": 3111, "default": 3047},
    },
    "Yone": {"core": [6672, 3031, 3153], "situational": [3091, 3026, 3156], "boots": {"default": 3006, "physical": 3047, "magic": 3111}},
    "Yasuo": {"core": [6672, 3031, 3153], "situational": [3091, 3026, 3156], "boots": {"default": 3006, "physical": 3047, "magic": 3111}},
    "Aphelios": {"core": [6672, 3031, 3036], "situational": [3033, 3072, 3026], "boots": {"default": 3006, "physical": 3047, "magic": 3111}},
    "Caitlyn": {"core": [6672, 3031, 3094], "situational": [3036, 3033, 3072, 3026], "boots": {"default": 3006, "physical": 3047, "magic": 3111}},
    "Jhin": {"core": [3142, 6676, 3031, 3094], "situational": [3036, 3033, 3026], "boots": {"default": 3006, "physical": 3047, "magic": 3111}},
    "Lucian": {"core": [6672, 3031, 3036], "situational": [3033, 3072, 3026], "boots": {"default": 3006, "physical": 3047, "magic": 3111}},
    "Ezreal": {"core": [3004, 3078, 6694], "situational": [3156, 3026, 3033], "boots": {"default": 3158, "physical": 3047, "magic": 3111}},
    "KaiSa": {"core": [6672, 3031, 3036], "situational": [3033, 3072, 3026], "boots": {"default": 3006, "physical": 3047, "magic": 3111}},
    "Jinx": {"core": [6672, 3031, 3036], "situational": [3033, 3072, 3026], "boots": {"default": 3006, "physical": 3047, "magic": 3111}},
    "Viego": {"core": [3153, 3078, 3053], "situational": [6333, 3091, 3156], "boots": {"default": 3006, "physical": 3047, "magic": 3111}},
    "Darius": {"core": [3071, 3053, 6333], "situational": [4401, 3143, 3156], "boots": {"default": 3047, "magic": 3111}},
    "Aatrox": {"core": [6692, 3161, 6333], "situational": [3053, 3156, 4401], "boots": {"default": 3047, "magic": 3111}},
    "Lux": {"core": [6655, 4645, 3089], "situational": [3135, 3157, 3102, 3165], "boots": {"default": 3020, "magic": 3111}},
    "Syndra": {"core": [6655, 4645, 3089], "situational": [3135, 3157, 3102, 3165], "boots": {"default": 3020, "magic": 3111}},
    "Ahri": {"core": [6655, 4645, 3157], "situational": [3135, 3089, 3102, 3165], "boots": {"default": 3020, "magic": 3111}},
    "Mel": {"core": [6655, 4645, 3089], "situational": [3135, 3157, 3102, 3165], "boots": {"default": 3020, "magic": 3111}},
    "Nidalee": {"core": [3100, 3089, 3135], "situational": [3157, 3102, 3165], "boots": {"default": 3020, "magic": 3111}},
    "Ekko": {"core": [3100, 3089, 3157], "situational": [3135, 3102, 3165], "boots": {"default": 3020, "magic": 3111}},
    "Zed": {"core": [3142, 6701, 6694], "situational": [3814, 6695, 3026, 3156], "boots": {"default": 3158, "physical": 3047, "magic": 3111}},
    "Talon": {"core": [3142, 6701, 6694], "situational": [3814, 6695, 3026, 3156], "boots": {"default": 3158, "physical": 3047, "magic": 3111}},
    "KhaZix": {"core": [3142, 6701, 6694], "situational": [3814, 6695, 3026, 3156], "boots": {"default": 3158, "physical": 3047, "magic": 3111}},
    "Qiyana": {"core": [3142, 6701, 6694], "situational": [3814, 6695, 3026, 3156], "boots": {"default": 3158, "physical": 3047, "magic": 3111}},
    "Pyke": {"core": [3142, 6701, 6694], "situational": [3814, 6695, 3026], "boots": {"default": 3158, "physical": 3047, "magic": 3111}},
    "Mordekaiser": {"core": [6653, 3065, 6665], "situational": [3075, 4401, 3157], "boots": {"default": 3047, "magic": 3111}},
    "TahmKench": {"core": [3068, 6665, 3065], "situational": [3075, 3143, 4401], "boots": {"default": 3047, "magic": 3111}},
    "Milio": {"core": [6617, 3107, 3504], "situational": [3222, 3190], "boots": {"default": 3158, "magic": 3111}},
    "Lulu": {"core": [3504, 6617, 3222], "situational": [3107, 3190], "boots": {"default": 3158, "magic": 3111}},
}

DEFAULT_BUILD_PROFILES = {
    "marksman": {"core": [6672, 3031, 3036], "situational": [3033, 3072, 3026], "boots": {"default": 3006, "physical": 3047, "magic": 3111}},
    "fighter": {"core": [3078, 3053, 6333], "situational": [3071, 3156, 4401, 3143], "boots": {"default": 3047, "magic": 3111}},
    "mage": {"core": [6655, 4645, 3089], "situational": [3135, 3157, 3102, 3165, 6653], "boots": {"default": 3020, "magic": 3111}},
    "assassin": {"core": [3142, 6701, 6694], "situational": [3814, 6695, 3026, 3156], "boots": {"default": 3158, "physical": 3047, "magic": 3111}},
    "tank": {"core": [3068, 6665, 3065], "situational": [3075, 3143, 4401], "boots": {"default": 3047, "magic": 3111}},
    "support": {"core": [6617, 3107, 3190], "situational": [3222, 3504], "boots": {"default": 3158, "magic": 3111}},
}

ITEM_BY_ID = {item["id"]: item for item in ITEM_CANDIDATES}

ITEM_THREAT_HINTS = {
    1053: {"healing": 1, "physical": 1},
    1058: {"magic": 2, "burst": 1},
    3071: {"physical": 1, "tank": 1},
    3072: {"physical": 2, "healing": 2},
    3075: {"tank": 2, "healing": 1},
    3089: {"magic": 3, "burst": 2},
    3102: {"magic": 1, "tank": 1},
    3143: {"tank": 2},
    3031: {"physical": 3, "burst": 2, "crit": 3},
    3036: {"physical": 2, "tank": 1, "crit": 2},
    3046: {"physical": 2, "crit": 2},
    3085: {"physical": 2, "crit": 2},
    3094: {"physical": 2, "crit": 2},
    3053: {"tank": 2, "burst": 1, "shielding": 2},
    3156: {"magic": 1, "burst": 1, "shielding": 2},
    3190: {"tank": 1, "shielding": 2},
    6617: {"healing": 2},
}

CHAMPION_CRIT_HINTS = {
    "Aphelios": 3,
    "Ashe": 2,
    "Caitlyn": 3,
    "Draven": 4,
    "Jhin": 4,
    "Jinx": 3,
    "Lucian": 2,
    "MissFortune": 2,
    "Samira": 3,
    "Tryndamere": 5,
    "Tristana": 3,
    "Yasuo": 5,
    "Yone": 4,
}

CHAMPION_SHIELD_HINTS = {
    "Janna": 4,
    "Karma": 3,
    "Lulu": 5,
    "Milio": 4,
    "Morgana": 2,
    "Orianna": 2,
    "Rakan": 2,
    "Seraphine": 3,
    "Sett": 2,
    "Shen": 3,
    "TahmKench": 2,
    "Yuumi": 4,
}

ITEM_DEFENSE_STATS = {
    1011: {"health": 350},
    1031: {"armor": 40},
    1033: {"magicResist": 25},
    1057: {"magicResist": 40},
    2420: {"stasis": 1},
    3026: {"armor": 45, "antiBurst": 1},
    3047: {"armor": 25, "antiAuto": 1},
    3053: {"health": 400, "antiBurst": 1},
    3065: {"health": 450, "magicResist": 60},
    3068: {"health": 350, "armor": 50},
    3075: {"health": 350, "armor": 75, "antiheal": 1},
    3102: {"magicResist": 50, "antiBurst": 1},
    3110: {"armor": 75, "antiAuto": 1},
    3111: {"magicResist": 25, "tenacity": 1},
    3143: {"health": 350, "armor": 75, "antiCrit": 1},
    3156: {"magicResist": 40, "antiBurst": 1},
    3157: {"armor": 50, "stasis": 1},
    3190: {"armor": 30, "magicResist": 30, "shield": 1},
    3222: {"magicResist": 40, "cleanse": 1},
    4401: {"health": 400, "magicResist": 55},
    6665: {"health": 350, "armor": 45, "magicResist": 45},
}

ITEM_OFFENSE_STATS = {
    1026: {"ap": 45},
    1036: {"ad": 10},
    1037: {"ad": 25},
    1038: {"ad": 40},
    1058: {"ap": 70},
    3004: {"ad": 35},
    3031: {"ad": 75, "crit": 1, "burst": 1},
    3033: {"ad": 35, "armorPen": 1},
    3036: {"ad": 35, "armorPen": 1},
    3071: {"ad": 40, "armorShred": 1},
    3072: {"ad": 80, "lifesteal": 1},
    3074: {"ad": 65},
    3078: {"ad": 36, "spellblade": 1},
    3142: {"ad": 55, "burst": 1},
    3089: {"ap": 130, "burst": 2},
    3100: {"ap": 115, "spellblade": 1, "burst": 1},
    3135: {"ap": 95, "magicPen": 1},
    3153: {"ad": 40, "attackSpeed": 1},
    3157: {"ap": 105, "stasis": 1},
    3165: {"ap": 90},
    4645: {"ap": 110, "magicPen": 1, "burst": 1},
    6653: {"ap": 70, "burn": 1},
    6655: {"ap": 115, "burst": 1},
    6672: {"ad": 45, "attackSpeed": 1},
    6676: {"ad": 50, "crit": 1, "burst": 1},
    6692: {"ad": 60, "burst": 1},
    6694: {"ad": 45, "armorPen": 1},
    6695: {"ad": 50},
    6701: {"ad": 55, "burst": 1},
}

EXTRA_ITEM_TAGS = {
    3916: {"antiheal"},
    1018: {"crit"},
    2420: {"stasis"},
}

ARCHETYPE_DEFENSE_BASE = {
    "marksman": {"armor": 25, "armorGrowth": 4.3, "magicResist": 30, "mrGrowth": 1.3, "health": 590, "healthGrowth": 105},
    "mage": {"armor": 24, "armorGrowth": 4.5, "magicResist": 30, "mrGrowth": 1.3, "health": 600, "healthGrowth": 108},
    "assassin": {"armor": 28, "armorGrowth": 4.6, "magicResist": 32, "mrGrowth": 1.8, "health": 630, "healthGrowth": 112},
    "fighter": {"armor": 32, "armorGrowth": 4.8, "magicResist": 32, "mrGrowth": 2.0, "health": 650, "healthGrowth": 116},
    "tank": {"armor": 36, "armorGrowth": 5.0, "magicResist": 32, "mrGrowth": 2.1, "health": 680, "healthGrowth": 120},
    "support": {"armor": 30, "armorGrowth": 4.6, "magicResist": 31, "mrGrowth": 1.8, "health": 620, "healthGrowth": 110},
}


def item_name(item_id):
    item = ITEM_BY_ID.get(item_id) or COMPONENT_ITEMS.get(item_id)
    return item.get("name") if item else f"#{item_id}"


def clamp(value, low, high):
    return max(low, min(high, value))


def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def load_build_stats():
    if not BUILD_STATS_PATH.exists():
        return {}
    try:
        with BUILD_STATS_PATH.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
            return payload if isinstance(payload, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


BUILD_STATS = {}
BUILD_STATS_MTIME = None


def current_build_stats():
    global BUILD_STATS, BUILD_STATS_MTIME
    try:
        mtime = BUILD_STATS_PATH.stat().st_mtime
    except OSError:
        BUILD_STATS = {}
        BUILD_STATS_MTIME = None
        return BUILD_STATS
    if BUILD_STATS_MTIME != mtime:
        BUILD_STATS = load_build_stats()
        BUILD_STATS_MTIME = mtime
    return BUILD_STATS


current_build_stats()


def normalize_percent(value):
    if value is None:
        return None
    number = safe_float(value, None)
    if number is None:
        return None
    return number / 100 if number > 1.5 else number


def format_percent(value):
    number = normalize_percent(value)
    if number is None:
        return "n/a"
    return f"{number * 100:.1f}%"


def sample_confidence_label(games):
    games = safe_int(games, 0)
    if games >= 120:
        return "신뢰 높음"
    if games >= 40:
        return "신뢰 보통"
    if games >= 10:
        return "신뢰 낮음"
    if games > 0:
        return "표본 매우 낮음"
    return "표본 n/a"


def normalize_item_sequence(value):
    if isinstance(value, str):
        chunks = value.replace(">", ",").replace("-", ",").replace("/", ",").split(",")
        raw_ids = [chunk.strip() for chunk in chunks]
    elif isinstance(value, (list, tuple)):
        raw_ids = value
    else:
        return []
    item_ids = []
    for raw_id in raw_ids:
        item_id = safe_int(raw_id, None)
        if item_id in ITEM_BY_ID and item_id not in item_ids:
            item_ids.append(item_id)
    return item_ids


def normalize_stage_winrates(raw_stage_winrates):
    result = {}
    if not isinstance(raw_stage_winrates, dict):
        return result
    for raw_key, raw_value in raw_stage_winrates.items():
        key = str(raw_key).lower().replace("core", "").replace("c", "").strip()
        stage = safe_int(key, None)
        if stage not in {1, 2, 3}:
            continue
        if isinstance(raw_value, dict):
            winrate = normalize_percent(raw_value.get("winrate") or raw_value.get("wr") or raw_value.get("winRate"))
            games = safe_int(raw_value.get("games") or raw_value.get("matches") or raw_value.get("sample"), 0)
            wins = safe_int(raw_value.get("wins"), 0)
            if winrate is None and games > 0 and wins >= 0:
                winrate = wins / games
            result[stage] = {"winrate": winrate, "games": games, "wins": wins}
        else:
            result[stage] = {"winrate": normalize_percent(raw_value), "games": 0, "wins": 0}
    return result


def canonical_position(position):
    value = str(position or "").upper()
    aliases = {
        "TOP": "TOP",
        "JUNGLE": "JUNGLE",
        "MIDDLE": "MIDDLE",
        "MID": "MIDDLE",
        "BOTTOM": "BOTTOM",
        "ADC": "BOTTOM",
        "UTILITY": "UTILITY",
        "SUPPORT": "UTILITY",
    }
    return aliases.get(value, "ANY")


def normalize_meta_entry(raw, source, position):
    if not isinstance(raw, dict):
        return None
    core = normalize_item_sequence(raw.get("core") or raw.get("items") or raw.get("sequence") or raw.get("build"))
    if not core:
        return None
    games = safe_int(raw.get("games") or raw.get("matches") or raw.get("sample") or raw.get("count"), 0)
    wins = safe_int(raw.get("wins"), 0)
    winrate = normalize_percent(raw.get("winrate") or raw.get("wr") or raw.get("winRate"))
    if winrate is None and games > 0 and wins > 0:
        winrate = wins / games
    pickrate = normalize_percent(raw.get("pickrate") or raw.get("pickRate") or raw.get("pr"))
    confidence = clamp(math.log10(max(1, games) + 1) / 3, 0, 1)
    if pickrate is not None:
        confidence = clamp(confidence + pickrate * 0.4, 0, 1)
    return {
        "core": core[:4],
        "winrate": winrate,
        "games": games,
        "wins": wins,
        "stageWinrates": normalize_stage_winrates(raw.get("stageWinrates") or raw.get("stage_winrates")),
        "pickrate": pickrate,
        "source": raw.get("source") or source,
        "patch": raw.get("patch"),
        "rank": raw.get("rank") or raw.get("tier") or "MASTER+",
        "position": canonical_position(raw.get("position") or position),
        "confidence": confidence,
    }


def get_meta_sequences(champion_key, position, archetype):
    stats = current_build_stats()
    champions = stats.get("champions") or stats.get("data") or {}
    if not isinstance(champions, dict):
        return []
    champion_blob = champions.get(champion_key)
    if champion_blob is None:
        champion_blob = next((value for key, value in champions.items() if str(key).lower() == champion_key.lower()), None)
    if champion_blob is None:
        return []

    position = canonical_position(position)
    source = stats.get("source") or "local"
    raw_entries = []
    if isinstance(champion_blob, list):
        raw_entries.extend((entry, position) for entry in champion_blob)
    elif isinstance(champion_blob, dict):
        keys = [position, "ANY", "ALL", archetype.upper()]
        for key in keys:
            value = champion_blob.get(key)
            if isinstance(value, list):
                raw_entries.extend((entry, key) for entry in value)
        generic = champion_blob.get("builds")
        if isinstance(generic, list):
            raw_entries.extend((entry, position) for entry in generic)

    entries = []
    seen = set()
    for raw, entry_position in raw_entries:
        entry = normalize_meta_entry(raw, source, entry_position)
        if not entry:
            continue
        key = tuple(entry["core"][:3])
        if key in seen:
            continue
        seen.add(key)
        entries.append(entry)

    def sort_key(entry):
        winrate = entry["winrate"] if entry["winrate"] is not None else 0.5
        return (entry["position"] == position, entry["confidence"], winrate, entry["games"])

    return sorted(entries, key=sort_key, reverse=True)[:5]


def first_missing_core(sequence, owned_ids):
    for index, item_id in enumerate(sequence):
        if item_id not in owned_ids:
            return index, item_id
    return len(sequence), None


def path_label(item_ids, limit=3):
    return " > ".join(item_name(item_id) for item_id in item_ids[:limit])


def stage_winrate_label(meta):
    stages = meta.get("stageWinrates") or {}
    if not stages:
        return f"승률 {format_percent(meta.get('winrate'))}"
    parts = []
    for stage in (1, 2, 3):
        stage_meta = stages.get(stage)
        if stage_meta:
            parts.append(f"{stage}C {format_percent(stage_meta.get('winrate'))}")
    return " / ".join(parts) if parts else f"승률 {format_percent(meta.get('winrate'))}"


def format_meta_comparison(meta_sequences, owned_ids):
    if not meta_sequences:
        return "고티어 빌드 비교: 아직 통계 없음"
    rows = []
    best_winrate = meta_sequences[0].get("winrate")
    for index, meta in enumerate(meta_sequences[:3], start=1):
        stage, next_id = first_missing_core(meta["core"], owned_ids)
        next_text = item_name(next_id) if next_id else "완성"
        games = f"{meta['games']}판" if meta.get("games") else "표본 n/a"
        delta = ""
        winrate = meta.get("winrate")
        if index > 1 and best_winrate is not None and winrate is not None:
            delta_value = (winrate - best_winrate) * 100
            delta = f" · 1위 대비 {delta_value:+.1f}%p"
        rows.append(f"#{index} {path_label(meta['core'])} · {stage_winrate_label(meta)}{delta} · {games} · {sample_confidence_label(meta.get('games'))} · 다음 {next_text}")
    return "고티어 빌드 비교:\n" + "\n".join(rows)


def recommendation_confidence(recommendations):
    if not recommendations:
        return {"label": "낮음", "detail": "추천 후보 없음"}
    top_score = recommendations[0]["score"]
    second_score = recommendations[1]["score"] if len(recommendations) > 1 else 0
    gap = top_score - second_score
    if top_score >= 250 and gap >= 45:
        label = "높음"
    elif top_score >= 180 and gap >= 20:
        label = "보통"
    else:
        label = "낮음"
    if len(recommendations) > 1:
        detail = f"1위 {top_score}점 / 2위와 {gap}점 차"
    else:
        detail = f"1위 {top_score}점 / 대안 없음"
    return {"label": label, "detail": detail, "gap": gap, "topScore": top_score}


def purchase_timing_label(entry, gold):
    next_buy = entry["next_buy"]
    if next_buy["kind"] == "component":
        shortage = next_buy["cost"] - gold
        if shortage <= 0:
            return "지금 귀환 구매"
        if shortage <= 250:
            return f"{shortage}g만 더 모으기"
        if shortage <= 650:
            return f"{shortage}g 부족, 한 웨이브 더"
        return "장기 목표"
    shortage = entry["missing"]
    if shortage <= 0:
        return "완성템 지금 구매"
    if shortage <= 250:
        return f"완성까지 {shortage}g"
    if shortage <= 650:
        return f"{shortage}g 더 모으면 완성"
    return "완성은 장기 목표"


def recommendation_snapshot(target, archetype, damage_profile, threat, recommendations, confidence, gold_info, completed_cores, profile, meta_sequences, ally_antiheal_count):
    return {
        "savedAt": time.strftime("%Y-%m-%d %H:%M:%S"),
        "target": {
            "champion": target.get("championName"),
            "position": target.get("position") or target.get("teamPosition"),
            "archetype": archetype,
            "damage": damage_profile.get("label"),
            "level": target.get("level") or target.get("championLevel"),
        },
        "gold": gold_info,
        "build": {
            "completedCores": completed_cores,
            "plannedCores": [item_name(item_id) for item_id in profile.get("core", [])],
            "metaPaths": [
                {
                    "path": [item_name(item_id) for item_id in meta.get("core", [])],
                    "winrate": meta.get("winrate"),
                    "games": meta.get("games"),
                    "stageWinrates": meta.get("stageWinrates"),
                }
                for meta in meta_sequences[:3]
            ],
        },
        "threat": threat,
        "allyCounters": {"antiheal": ally_antiheal_count},
        "confidence": confidence,
        "recommendations": [
            {
                "item": entry["item"]["name"],
                "nextBuy": entry["next_buy"]["name"],
                "score": entry["score"],
                "timing": purchase_timing_label(entry, gold_info["gold"]),
                "reasons": entry["breakdown"],
            }
            for entry in recommendations
        ],
    }


def save_latest_recommendation(snapshot):
    try:
        LATEST_RECOMMENDATION_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LATEST_RECOMMENDATION_PATH.open("w", encoding="utf-8") as handle:
            json.dump(snapshot, handle, ensure_ascii=False, indent=2)
    except OSError:
        pass


def fetch_json(url):
    with urlopen(url, timeout=3.5) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_champion_key(name):
    cleaned = str(name or "")
    cleaned = cleaned.replace("game_character_displayname_", "")
    cleaned = cleaned.replace("game_character_skin_displayname_", "")
    raw = "".join(ch for ch in cleaned if ch.isalpha() and ord(ch) < 128)
    special = {
        "Kaisa": "KaiSa",
        "Khazix": "KhaZix",
        "LeeSin": "LeeSin",
        "MasterYi": "MasterYi",
        "MissFortune": "MissFortune",
        "TahmKench": "TahmKench",
        "TwistedFate": "TwistedFate",
        "MonkeyKing": "Wukong",
        "Reksai": "RekSai",
    }
    if raw in CHAMPION_HINTS:
        return raw
    if raw in special:
        return special[raw]
    for key in CHAMPION_HINTS:
        if key.lower() == raw.lower():
            return key
    return raw or "KaiSa"


def player_value(player, index):
    return player.get("summonerName") or player.get("riotId") or f"{player.get('team', 'TEAM')}:{player.get('championName', 'Champion')}:{index}"


def player_label(player):
    side = "블루" if player.get("team") == "ORDER" else "레드"
    position = player.get("position") or "-"
    champion = player.get("championName") or "?"
    name = player.get("summonerName") or player.get("riotId") or "플레이어"
    return f"{side} {position} / {champion} / {name}"


def format_seconds(total_seconds):
    seconds = max(0, int(float(total_seconds or 0)))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def round_to_50(value):
    return int(max(0, round(value / 50) * 50))


def item_cost(item):
    item_id = item.get("itemID")
    count = max(1, int(item.get("count") or 1))
    cost = ITEM_COSTS.get(item_id, item.get("price") or 0)
    return cost * count


def inventory_value(player):
    return sum(item_cost(item) for item in (player.get("items") or []) if item.get("slot") != 6)


def same_player(candidate, active):
    if not candidate or not active:
        return False
    values = {
        str(candidate.get("summonerName") or "").lower(),
        str(candidate.get("riotId") or "").lower(),
        str(candidate.get("riotIdGameName") or "").lower(),
    }
    active_values = {
        str(active.get("summonerName") or "").lower(),
        str(active.get("riotId") or "").lower(),
        str(active.get("riotIdGameName") or "").lower(),
    }
    return bool(values.intersection(active_values) - {""})


def estimate_available_gold(player, live):
    active = live.get("activePlayer") or {}
    exact = active.get("currentGold")
    if isinstance(exact, (int, float)) and same_player(player, active):
        return {
            "gold": int(exact),
            "source": "정확",
            "detail": "Live Client API currentGold",
            "spent": inventory_value(player),
        }

    game_time = float((live.get("gameData") or {}).get("gameTime") or 0)
    scores = player.get("scores") or {}
    cs = float(scores.get("creepScore") or 0)
    kills = float(scores.get("kills") or 0)
    assists = float(scores.get("assists") or 0)
    position = player.get("position") or ""
    cs_value = 28 if position == "JUNGLE" else 12 if position == "UTILITY" else 21
    passive_gold = max(0, game_time - 90) * 2.04
    combat_gold = kills * 300 + assists * 150
    farm_gold = cs * cs_value
    support_income = min(1000, max(0, game_time - 120) * 0.55) if position == "UTILITY" else 0
    earned = 500 + passive_gold + farm_gold + combat_gold + support_income
    spent = inventory_value(player)
    available = round_to_50(earned - spent)
    return {
        "gold": available,
        "source": "추정",
        "detail": f"CS {int(cs)} / KDA {int(kills)}킬 {int(assists)}어시 / 보유템 {spent}g",
        "spent": spent,
    }


def player_scores(player):
    scores = player.get("scores") or {}
    return {
        "kills": safe_float(scores.get("kills"), 0),
        "deaths": safe_float(scores.get("deaths"), 0),
        "assists": safe_float(scores.get("assists"), 0),
        "cs": safe_float(scores.get("creepScore"), 0),
    }


def player_level(player):
    return safe_float(player.get("level") or player.get("championLevel"), 1)


def item_tags(item_id):
    tags = set()
    item = ITEM_BY_ID.get(item_id)
    if item:
        tags.update(item.get("tags", []))
    tags.update(EXTRA_ITEM_TAGS.get(item_id, set()))
    return tags


def allied_tag_count(players, target, tag):
    target_team = target.get("team")
    count = 0
    for player in players:
        if player.get("team") != target_team:
            continue
        if any(tag in item_tags(item.get("itemID")) for item in (player.get("items") or [])):
            count += 1
    return count


def estimate_defense_profile(player):
    champion_key = normalize_champion_key(player.get("rawChampionName") or player.get("championName"))
    archetype = CHAMPION_HINTS.get(champion_key, {}).get("archetype", "fighter")
    base = ARCHETYPE_DEFENSE_BASE.get(archetype, ARCHETYPE_DEFENSE_BASE["fighter"])
    level = max(1, player_level(player))
    armor = base["armor"] + base["armorGrowth"] * (level - 1)
    magic_resist = base["magicResist"] + base["mrGrowth"] * (level - 1)
    health = base["health"] + base["healthGrowth"] * (level - 1)
    traits = {"antiAuto": 0, "antiCrit": 0, "stasis": 0, "shield": 0, "antiBurst": 0, "cleanse": 0, "tenacity": 0}
    for item in player.get("items") or []:
        stats = ITEM_DEFENSE_STATS.get(item.get("itemID"), {})
        armor += stats.get("armor", 0)
        magic_resist += stats.get("magicResist", 0)
        health += stats.get("health", 0)
        for trait in traits:
            traits[trait] += stats.get(trait, 0)
    physical_ehp = health * (1 + max(0, armor) / 100)
    magic_ehp = health * (1 + max(0, magic_resist) / 100)
    return {
        "armor": armor,
        "magicResist": magic_resist,
        "health": health,
        "physicalEhp": physical_ehp,
        "magicEhp": magic_ehp,
        "archetype": archetype,
        **traits,
    }


def estimate_offense_profile(player):
    champion_key = normalize_champion_key(player.get("rawChampionName") or player.get("championName"))
    hint = CHAMPION_HINTS.get(champion_key, {"damage": "mixed", "burst": 1})
    scores = player_scores(player)
    level = max(1, player_level(player))
    ad = 60 + level * 4.2
    ap = 0
    bonus_burst = 0
    physical_pen = 0
    magic_pen = 0
    for item in player.get("items") or []:
        stats = ITEM_OFFENSE_STATS.get(item.get("itemID"), {})
        ad += stats.get("ad", 0)
        ap += stats.get("ap", 0)
        bonus_burst += stats.get("burst", 0) * 0.18
        physical_pen += stats.get("armorPen", 0) * 0.12 + stats.get("armorShred", 0) * 0.10
        magic_pen += stats.get("magicPen", 0) * 0.12
    burst_trait = safe_float(hint.get("burst"), 1)
    lead = max(0, scores["kills"] - scores["deaths"]) * 0.06 + scores["kills"] * 0.035 + scores["assists"] * 0.012
    multiplier = clamp(0.85 + burst_trait * 0.16 + bonus_burst + lead, 0.85, 2.25)
    damage = hint.get("damage")
    if damage == "physical":
        raw_physical = (ad * 4.2 + level * 38) * multiplier
        raw_magic = ap * 1.15
    elif damage == "magic":
        raw_physical = ad * 1.25
        raw_magic = (ap * 3.5 + level * 42) * multiplier
    else:
        raw_physical = (ad * 2.3 + level * 24) * multiplier
        raw_magic = (ap * 2.4 + level * 26) * multiplier
    return {
        "physical": raw_physical,
        "magic": raw_magic,
        "physicalPen": clamp(physical_pen, 0, 0.35),
        "magicPen": clamp(magic_pen, 0, 0.35),
        "multiplier": multiplier,
        "burstTrait": burst_trait,
    }


def mitigated_damage(raw_damage, resistance, penetration=0):
    effective_resistance = max(0, resistance * (1 - penetration))
    return raw_damage * 100 / (100 + effective_resistance)


def estimate_burst_against_target(enemy, target_defense):
    offense = estimate_offense_profile(enemy)
    physical = mitigated_damage(offense["physical"], target_defense["armor"], offense["physicalPen"])
    magic = mitigated_damage(offense["magic"], target_defense["magicResist"], offense["magicPen"])
    total = physical + magic
    health = max(1, target_defense["health"])
    return {
        "damage": total,
        "ratio": total / health,
        "physical": physical,
        "magic": magic,
    }


def build_threat(target, players):
    profile = {
        "physical": 0,
        "magic": 0,
        "healing": 0,
        "shielding": 0,
        "crit": 0,
        "tank": 0,
        "cc": 0,
        "burst": 0,
        "fedBurst": 0,
        "lead": 0,
        "avgArmor": 0,
        "avgMr": 0,
        "armorStack": 0,
        "mrStack": 0,
        "physicalEhp": 0,
        "magicEhp": 0,
        "lethalBurst": 0,
    }
    target_team = target.get("team")
    target_level = player_level(target)
    target_spent = inventory_value(target)
    target_defense = estimate_defense_profile(target)
    enemies = [p for p in players if p.get("team") and p.get("team") != target_team]
    target_position = canonical_position(target.get("position") or target.get("teamPosition"))
    lane_enemy = None
    if target_position:
        lane_candidates = [
            enemy
            for enemy in enemies
            if canonical_position(enemy.get("position") or enemy.get("teamPosition")) == target_position
        ]
        if lane_candidates:
            def lane_pressure(enemy):
                scores = player_scores(enemy)
                return (
                    player_level(enemy) * 0.25
                    + max(0, player_level(enemy) - target_level) * 0.7
                    + scores["kills"] * 0.8
                    + scores["assists"] * 0.18
                    + max(0, scores["kills"] - scores["deaths"]) * 0.45
                    + max(0, inventory_value(enemy) - target_spent) / 1500
                )

            lane_enemy = max(lane_candidates, key=lane_pressure)
    top_threat = {"score": 0, "label": ""}
    top_burst = {"damage": 0, "label": ""}
    defense_rows = []
    lane_defense = None
    lane_label = ""
    for enemy in enemies:
        key = normalize_champion_key(enemy.get("rawChampionName") or enemy.get("championName"))
        hint = CHAMPION_HINTS.get(key, {"damage": "mixed", "tank": 1, "cc": 1, "burst": 1})
        defense = estimate_defense_profile(enemy)
        defense_rows.append(defense)
        if enemy is lane_enemy:
            lane_defense = defense
            champion_label = enemy.get("championName") or key or "상대"
            lane_label = f"{champion_label} Lv{int(player_level(enemy))}"
        scores = player_scores(enemy)
        level_delta = max(0, player_level(enemy) - target_level)
        spent_delta = max(0, inventory_value(enemy) - target_spent)
        kda_pressure = scores["kills"] * 0.12 + scores["assists"] * 0.035 + max(0, scores["kills"] - scores["deaths"]) * 0.07
        farm_pressure = min(0.55, scores["cs"] / 260)
        item_pressure = min(0.85, spent_delta / 5200)
        level_pressure = min(0.65, level_delta * 0.18)
        pressure = clamp(1 + kda_pressure + farm_pressure + item_pressure + level_pressure, 0.8, 2.7)
        damage = hint.get("damage")
        if damage == "physical":
            profile["physical"] += 2.1 * pressure
        elif damage == "magic":
            profile["magic"] += 2.1 * pressure
        else:
            profile["physical"] += 1.25 * pressure
            profile["magic"] += 1.25 * pressure
        profile["healing"] += hint.get("heal", 0) * pressure
        profile["shielding"] += CHAMPION_SHIELD_HINTS.get(key, 0) * pressure
        profile["crit"] += CHAMPION_CRIT_HINTS.get(key, 0) * pressure
        profile["tank"] += hint.get("tank", 0) * (0.75 + min(0.8, inventory_value(enemy) / 8500))
        profile["cc"] += hint.get("cc", 0) * (0.85 + level_pressure)
        profile["burst"] += hint.get("burst", 0) * pressure
        if hint.get("archetype") == "assassin" and pressure >= 1.45:
            profile["fedBurst"] += hint.get("burst", 0) * pressure
        profile["lead"] += max(0, pressure - 1) * 2
        enemy_score = pressure * (hint.get("burst", 1) + hint.get("tank", 0) * 0.35 + scores["kills"] * 0.25)
        burst_estimate = estimate_burst_against_target(enemy, target_defense)
        profile["lethalBurst"] += max(0, burst_estimate["ratio"] - 0.45) * 5
        if burst_estimate["damage"] > top_burst["damage"]:
            display_name = enemy.get("championName") or key
            top_burst = {
                "damage": burst_estimate["damage"],
                "ratio": burst_estimate["ratio"],
                "label": f"{display_name} 약 {round(burst_estimate['damage'])} 피해 ({round(burst_estimate['ratio'] * 100)}%)",
            }
        if enemy_score > top_threat["score"]:
            display_name = enemy.get("championName") or key
            top_threat = {
                "score": enemy_score,
                "label": f"{display_name} Lv{int(player_level(enemy))} {int(scores['kills'])}/{int(scores['deaths'])}/{int(scores['assists'])}",
            }
        for item in enemy.get("items") or []:
            for key_name, value in ITEM_THREAT_HINTS.get(item.get("itemID"), {}).items():
                profile[key_name] += value * pressure
    if defense_rows:
        avg_armor = sum(row["armor"] for row in defense_rows) / len(defense_rows)
        avg_mr = sum(row["magicResist"] for row in defense_rows) / len(defense_rows)
        avg_physical_ehp = sum(row["physicalEhp"] for row in defense_rows) / len(defense_rows)
        avg_magic_ehp = sum(row["magicEhp"] for row in defense_rows) / len(defense_rows)
        profile["avgArmor"] = avg_armor
        profile["avgMr"] = avg_mr
        profile["physicalEhp"] = avg_physical_ehp / 1000
        profile["magicEhp"] = avg_magic_ehp / 1000
        profile["armorStack"] = max(0, (avg_armor - 82) / 9)
        profile["mrStack"] = max(0, (avg_mr - 58) / 7)
    result = {key: min(10, round(value)) for key, value in profile.items()}
    result["avgArmorValue"] = round(profile["avgArmor"])
    result["avgMrValue"] = round(profile["avgMr"])
    result["physicalEhpValue"] = round(profile["physicalEhp"] * 1000)
    result["magicEhpValue"] = round(profile["magicEhp"] * 1000)
    result["topBurst"] = top_burst["label"]
    result["topBurstDamage"] = round(top_burst["damage"])
    result["topBurstRatio"] = round(top_burst.get("ratio", 0) * 100)
    result["primary"] = top_threat["label"]
    if lane_defense:
        result["laneOpponent"] = lane_label
        result["laneArmorValue"] = round(lane_defense["armor"])
        result["laneMrValue"] = round(lane_defense["magicResist"])
        result["lanePhysicalEhpValue"] = round(lane_defense["physicalEhp"])
        result["laneMagicEhpValue"] = round(lane_defense["magicEhp"])
        result["laneArmorStack"] = min(10, round(max(0, (lane_defense["armor"] - 82) / 7)))
        result["laneMrStack"] = min(10, round(max(0, (lane_defense["magicResist"] - 58) / 6)))
    else:
        result["laneOpponent"] = ""
        result["laneArmorValue"] = 0
        result["laneMrValue"] = 0
        result["lanePhysicalEhpValue"] = 0
        result["laneMagicEhpValue"] = 0
        result["laneArmorStack"] = 0
        result["laneMrStack"] = 0
    return result


def completed_item_count(item_ids, plan_ids):
    return sum(1 for item_id in plan_ids if item_id in item_ids)


def get_build_profile(champion_key, archetype):
    return BUILD_PROFILES.get(champion_key) or DEFAULT_BUILD_PROFILES.get(archetype) or DEFAULT_BUILD_PROFILES["fighter"]


def own_damage_profile(champion_key, hint, archetype):
    damage = hint.get("damage", "mixed")
    if damage == "physical":
        return {"physical": 1.0, "magic": 0.0, "label": "물리"}
    if damage == "magic":
        return {"physical": 0.0, "magic": 1.0, "label": "마법"}
    if archetype == "marksman":
        return {"physical": 0.78, "magic": 0.22, "label": "혼합/물리 중심"}
    if archetype in {"mage", "support"}:
        return {"physical": 0.25, "magic": 0.75, "label": "혼합/마법 중심"}
    return {"physical": 0.55, "magic": 0.45, "label": "혼합"}


def profile_with_meta(base_profile, meta_sequences):
    if not meta_sequences:
        return base_profile
    meta_core = [item_id for item_id in meta_sequences[0]["core"] if item_id in ITEM_BY_ID]
    if not meta_core:
        return base_profile
    merged_core = meta_core + [item_id for item_id in base_profile.get("core", []) if item_id not in meta_core]
    merged = dict(base_profile)
    merged["core"] = merged_core
    merged["meta_source"] = meta_sequences[0].get("source")
    return merged


def choose_boot_id(profile, threat):
    boots = profile.get("boots", {})
    if threat["magic"] >= threat["physical"] + 2 or threat["cc"] >= 7:
        return boots.get("magic") or boots.get("default")
    if threat["physical"] >= threat["magic"] + 2:
        return boots.get("physical") or boots.get("default")
    return boots.get("default")


def next_component_for(item, owned_ids, gold, component_value=0):
    if item["cost"] - component_value <= gold:
        return {"id": item["id"], "name": item["name"], "cost": item["cost"], "kind": "complete"}
    components = [component for component in item.get("components", []) if component not in owned_ids]
    if not components:
        return {"id": item["id"], "name": item["name"], "cost": item["cost"], "kind": "complete"}
    component_options = []
    for component_id in components:
        meta = COMPONENT_ITEMS.get(component_id, {"name": f"#{component_id}", "cost": ITEM_COSTS.get(component_id, 0)})
        component_options.append({"id": component_id, "name": meta["name"], "cost": meta["cost"], "kind": "component"})
    affordable = [component for component in component_options if component["cost"] <= gold]
    if affordable:
        return sorted(affordable, key=lambda component: component["cost"], reverse=True)[0]
    return sorted(component_options, key=lambda component: component["cost"])[0]


def score_plan_item(item, entry, context):
    tags = set(item["tags"])
    threat = context["threat"]
    gold = context["gold_info"]["gold"]
    owned_ids = context["owned_ids"]
    archetype = context["archetype"]
    damage_profile = context["damage_profile"]
    ally_antiheal_count = context.get("ally_antiheal_count", 0)
    completed_cores = context["completed_cores"]
    score = 0
    breakdown = []

    def add(points, label):
        nonlocal score
        score += points
        prefix = "+" if points >= 0 else ""
        breakdown.append(f"{prefix}{points} {label}")

    if entry["type"] == "meta":
        stage = entry["stage"]
        meta = entry.get("meta", {})
        rank = entry.get("rank", 1)
        if stage == completed_cores:
            add(182, f"마스터+ #{rank} {stage + 1}코어 경로")
        elif stage == completed_cores + 1:
            add(132, f"마스터+ #{rank} 다음 코어")
        elif stage < completed_cores:
            add(108, f"마스터+ #{rank} 누락 코어 보정")
        else:
            add(82 - stage * 8, f"마스터+ #{rank} {stage + 1}코어 후보")
            add(-44, "아직 순서 이른 편")
        stage_stats = (meta.get("stageWinrates") or {}).get(stage + 1, {})
        winrate = stage_stats.get("winrate") if stage_stats.get("winrate") is not None else meta.get("winrate")
        if winrate is not None:
            sample_confidence = meta.get("confidence", 0)
            winrate_points = round(clamp((winrate - 0.5) * 210, -26, 52) * (0.55 + sample_confidence * 0.45))
            add(winrate_points, f"{stage + 1}코어 경로 승률 {format_percent(winrate)}")
        games = meta.get("games") or 0
        if games:
            add(round(clamp(math.log10(games + 1) * 9, 6, 31)), f"고티어 표본 {games}판")
            if games < 10:
                add(-24, "표본 매우 낮음")
            elif games < 40:
                add(-10, "표본 낮음")
        if meta.get("position") == context.get("position"):
            add(12, "포지션 일치")
    elif entry["type"] == "core":
        stage = entry["stage"]
        if stage == completed_cores:
            add(170, f"{stage + 1}코어 진행")
        elif stage == completed_cores + 1:
            add(118, f"다음 코어 후보")
        else:
            add(62 - stage * 8, f"{stage + 1}코어 후보")
            if stage > completed_cores + 1:
                add(-70, "아직 순서 이른 편")
    elif entry["type"] == "boots":
        add(92 if completed_cores == 0 else 72, "신발 타이밍")
    else:
        add(70, "상황 아이템")
        if completed_cores == 0:
            add(-55, "1코어 전 상황템 보류")
        elif completed_cores >= 2:
            add(18, "2코어 이후 상황 대응")

    if archetype in item["roles"]:
        add(24, "역할 적합")
    elif archetype == "support" and "tank" in item["roles"]:
        add(10, "서포터 탱킹 선택")
    else:
        add(-22, "역할과 거리 있음")

    component_value = sum(ITEM_COSTS.get(component_id, 0) for component_id in item.get("components", []) if component_id in owned_ids)
    if component_value:
        add(min(42, 18 + component_value // 90), f"이미 {component_value}g 진행")

    if threat["healing"] >= 7 and "antiheal" in tags:
        if ally_antiheal_count == 0:
            add(42, f"회복 위협 {threat['healing']}/10 · 팀 치감 없음")
        elif ally_antiheal_count >= 2:
            add(14, f"회복 위협 {threat['healing']}/10 · 팀 치감 {ally_antiheal_count}명")
        else:
            add(28, f"회복 위협 {threat['healing']}/10 · 팀 치감 {ally_antiheal_count}명")
    if threat.get("shielding", 0) >= 5 and "antiShield" in tags:
        add(38, f"보호막 위협 {threat['shielding']}/10")
    physical_pen_fit = damage_profile["physical"] >= 0.45 and tags.intersection({"armorPen", "armorShred"})
    magic_pen_fit = damage_profile["magic"] >= 0.45 and "magicPen" in tags
    anti_tank_fit = "antiTank" in tags and max(damage_profile["physical"], damage_profile["magic"]) >= 0.45

    if threat["tank"] >= 7 and (physical_pen_fit or magic_pen_fit or anti_tank_fit):
        add(20 if entry["type"] == "core" else 34, f"탱커 위협 {threat['tank']}/10")
    if threat.get("armorStack", 0) >= 5 and (physical_pen_fit or ("antiTank" in tags and damage_profile["physical"] >= 0.45)):
        points = 28 if entry["type"] != "core" else 18
        add(round(points * damage_profile["physical"]), f"{damage_profile['label']} 딜 + 평균 방어력 {threat.get('avgArmorValue', 0)} 추정")
    if threat.get("mrStack", 0) >= 5 and (magic_pen_fit or ("antiTank" in tags and damage_profile["magic"] >= 0.45)):
        points = 28 if entry["type"] != "core" else 18
        add(round(points * damage_profile["magic"]), f"{damage_profile['label']} 딜 + 평균 마저 {threat.get('avgMrValue', 0)} 추정")
    if threat.get("laneArmorStack", 0) >= 4 and (physical_pen_fit or ("antiTank" in tags and damage_profile["physical"] >= 0.45)):
        points = 44 if entry["type"] != "core" else 28
        add(round(points * damage_profile["physical"]), f"라인 상대 방어력 {threat.get('laneArmorValue', 0)} 추정")
    if threat.get("laneMrStack", 0) >= 4 and (magic_pen_fit or ("antiTank" in tags and damage_profile["magic"] >= 0.45)):
        points = 44 if entry["type"] != "core" else 28
        add(round(points * damage_profile["magic"]), f"라인 상대 마저 {threat.get('laneMrValue', 0)} 추정")
    if threat["physical"] >= threat["magic"] + 2 and tags.intersection({"armor", "antiAuto", "antiCrit"}):
        add(20 if completed_cores else 8, f"AD 위협 {threat['physical']}/10")
    if threat["physical"] >= threat["magic"] + 4 and "magicResist" in tags and not tags.intersection({"armor", "stasis"}):
        add(-34, "AD 위협 우세라 마저템 지연")
    if threat.get("crit", 0) >= 6 and tags.intersection({"antiCrit", "antiAuto", "armor"}):
        if "antiCrit" in tags:
            add(36, f"치명타 위협 {threat['crit']}/10")
        elif "antiAuto" in tags:
            add(24, f"치명타/평타 위협 {threat['crit']}/10")
        else:
            add(14, f"치명타 위협 {threat['crit']}/10")
    if threat["magic"] >= threat["physical"] + 2 and tags.intersection({"magicResist", "tenacity", "cleanse"}):
        add(20 if completed_cores else 8, f"AP 위협 {threat['magic']}/10")
    if threat["magic"] >= threat["physical"] + 4 and "armor" in tags and "magicResist" not in tags and "stasis" not in tags:
        add(-34, "AP 위협 우세라 방어템 지연")
    if threat["cc"] >= 7 and tags.intersection({"tenacity", "cleanse"}):
        add(24, f"CC 위협 {threat['cc']}/10")
    if threat["burst"] >= 7 and tags.intersection({"antiBurst", "stasis", "shield"}):
        add(22, f"폭딜 위협 {threat['burst']}/10")
    if threat.get("lethalBurst", 0) >= 4 and tags.intersection({"antiBurst", "stasis", "shield", "armor", "magicResist"}):
        if "stasis" in tags:
            add(42, f"예상 폭딜 {threat.get('topBurstRatio', 0)}%")
        elif tags.intersection({"antiBurst", "shield"}):
            add(34, f"예상 폭딜 {threat.get('topBurstRatio', 0)}%")
        else:
            add(20, f"예상 폭딜 {threat.get('topBurstRatio', 0)}%")
    if threat.get("fedBurst", 0) >= 6:
        if "stasis" in tags:
            add(50, f"성장한 암살자/폭딜 {threat['fedBurst']}/10")
        elif tags.intersection({"antiBurst", "shield"}):
            add(38, f"성장한 암살자/폭딜 {threat['fedBurst']}/10")
        elif tags.intersection({"armor", "magicResist"}):
            add(24, f"성장한 암살자/폭딜 {threat['fedBurst']}/10")

    remaining_cost = max(0, item["cost"] - component_value)
    next_buy = next_component_for(item, owned_ids, gold, component_value)
    missing = max(0, remaining_cost - gold)
    if next_buy["kind"] == "component":
        if next_buy["cost"] <= gold:
            add(18, f"지금 {next_buy['name']} 구매 가능")
        else:
            add(6, f"다음 하위템 {next_buy['name']}")
    elif missing == 0:
        add(28, "완성 구매 가능")
    elif missing <= 650:
        add(14, f"완성까지 {missing}g")
    elif entry["type"] != "core" and missing > 1600:
        add(-10, "완성까지 멀음")

    return {
        "item": item,
        "score": round(score),
        "missing": missing,
        "remaining_cost": remaining_cost,
        "component_value": component_value,
        "next_buy": next_buy,
        "breakdown": breakdown[:8],
    }


def build_plan_entries(profile, threat, owned_ids, meta_sequences=None):
    entries = []
    for rank, meta in enumerate((meta_sequences or [])[:3], start=1):
        stage, item_id = first_missing_core(meta["core"], owned_ids)
        if item_id in ITEM_BY_ID:
            entries.append({"id": item_id, "type": "meta", "stage": stage, "rank": rank, "meta": meta})
    for index, item_id in enumerate(profile.get("core", [])):
        if item_id in ITEM_BY_ID and item_id not in owned_ids:
            entries.append({"id": item_id, "type": "core", "stage": index})
    boot_id = choose_boot_id(profile, threat)
    has_boots = bool(owned_ids.intersection({2422, 3006, 3047, 3111, 3020, 3158}))
    if boot_id in ITEM_BY_ID and not has_boots:
        entries.append({"id": boot_id, "type": "boots", "stage": 0})
    for item_id in profile.get("situational", []):
        if item_id in ITEM_BY_ID and item_id not in owned_ids:
            entries.append({"id": item_id, "type": "situational", "stage": 99})
    return entries


def recommend(target, players, gold_info):
    key = normalize_champion_key(target.get("rawChampionName") or target.get("championName"))
    hint = CHAMPION_HINTS.get(key, {"archetype": "marksman"})
    archetype = hint.get("archetype", "marksman")
    damage_profile = own_damage_profile(key, hint, archetype)
    owned_ids = {item.get("itemID") for item in (target.get("items") or [])}
    threat = build_threat(target, players)
    position = canonical_position(target.get("position") or target.get("teamPosition"))
    meta_sequences = get_meta_sequences(key, position, archetype)
    profile = profile_with_meta(get_build_profile(key, archetype), meta_sequences)
    ally_antiheal_count = allied_tag_count(players, target, "antiheal")
    context = {
        "archetype": archetype,
        "damage_profile": damage_profile,
        "position": position,
        "threat": threat,
        "gold_info": gold_info,
        "owned_ids": owned_ids,
        "ally_antiheal_count": ally_antiheal_count,
        "completed_cores": completed_item_count(owned_ids, profile.get("core", [])),
    }
    candidates = []
    seen = set()
    for entry in build_plan_entries(profile, threat, owned_ids, meta_sequences):
        item_id = entry["id"]
        if item_id in seen:
            continue
        seen.add(item_id)
        candidates.append(score_plan_item(ITEM_BY_ID[item_id], entry, context))
    candidates.sort(key=lambda entry: entry["score"], reverse=True)
    return key, archetype, damage_profile, threat, candidates[:3], profile, context["completed_cores"], meta_sequences, ally_antiheal_count


class OverlayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LoL Item Overlay")
        self.root.geometry("470x720+70+90")
        self.root.configure(bg=COLORS["bg"])
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.94)
        self.root.overrideredirect(True)
        self.root.bind("<Escape>", lambda _event: self.root.destroy())

        self.events = queue.Queue()
        self.players = []
        self.selected_value = ""
        self.drag_start = None
        self.gold_var = tk.StringVar(value="자동")
        self.gold_note_var = tk.StringVar(value="리플레이 데이터로 계산")
        self.target_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value="연결 대기")
        self.time_var = tk.StringVar(value="--:--")

        self._build_styles()
        self._build_ui()
        self._start_polling()
        self._process_events()

    def _build_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Overlay.TCombobox", fieldbackground=COLORS["panel"], background=COLORS["panel"], foreground=COLORS["text"])

    def _build_ui(self):
        top = tk.Frame(self.root, bg=COLORS["panel_alt"], height=42)
        top.pack(fill="x")
        top.bind("<ButtonPress-1>", self._begin_drag)
        top.bind("<B1-Motion>", self._drag)

        title = tk.Label(top, text="LoL 추천 오버레이", fg=COLORS["text"], bg=COLORS["panel_alt"], font=("Malgun Gothic", 12, "bold"))
        title.pack(side="left", padx=12)
        title.bind("<ButtonPress-1>", self._begin_drag)
        title.bind("<B1-Motion>", self._drag)

        tk.Label(top, textvariable=self.time_var, fg=COLORS["gold"], bg=COLORS["panel_alt"], font=("Segoe UI", 11, "bold")).pack(side="left", padx=4)
        tk.Button(top, text="×", command=self.root.destroy, fg=COLORS["text"], bg=COLORS["red"], bd=0, font=("Segoe UI", 12, "bold"), width=3).pack(side="right", padx=6, pady=7)

        body = tk.Frame(self.root, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=10, pady=10)

        status = tk.Label(body, textvariable=self.status_var, fg=COLORS["muted"], bg=COLORS["bg"], anchor="w", font=("Malgun Gothic", 9, "bold"))
        status.pack(fill="x", pady=(0, 8))

        target_row = tk.Frame(body, bg=COLORS["bg"])
        target_row.pack(fill="x", pady=(0, 8))
        tk.Label(target_row, text="대상", fg=COLORS["muted"], bg=COLORS["bg"], font=("Malgun Gothic", 9, "bold")).pack(anchor="w")
        self.target_combo = ttk.Combobox(target_row, textvariable=self.target_var, state="readonly", style="Overlay.TCombobox")
        self.target_combo.pack(fill="x", pady=(4, 0))
        self.target_combo.bind("<<ComboboxSelected>>", self._on_target_change)

        gold_row = tk.Frame(body, bg=COLORS["bg"])
        gold_row.pack(fill="x", pady=(0, 10))
        tk.Label(gold_row, text="자동 골드", fg=COLORS["muted"], bg=COLORS["bg"], font=("Malgun Gothic", 9, "bold")).pack(side="left")
        gold_entry = tk.Entry(gold_row, textvariable=self.gold_var, fg=COLORS["text"], bg=COLORS["panel"], insertbackground=COLORS["text"], relief="flat", width=10, font=("Segoe UI", 11, "bold"), state="readonly")
        gold_entry.pack(side="left", padx=8)
        tk.Label(gold_row, textvariable=self.gold_note_var, fg=COLORS["muted"], bg=COLORS["bg"], font=("Malgun Gothic", 8, "bold")).pack(side="left")
        tk.Button(gold_row, text="항상 위", command=self._toggle_topmost, fg=COLORS["text"], bg=COLORS["panel_alt"], bd=0, padx=10, pady=4).pack(side="right")

        self.summary = tk.Label(body, text="리플레이를 재생하고 기다려 주세요.", fg=COLORS["text"], bg=COLORS["panel"], justify="left", anchor="w", wraplength=430, padx=10, pady=8, font=("Malgun Gothic", 9, "bold"))
        self.summary.pack(fill="x", pady=(0, 10))

        self.cards = []
        for _index in range(3):
            card = tk.Frame(body, bg=COLORS["panel"], highlightthickness=1, highlightbackground=COLORS["line"])
            card.pack(fill="x", pady=5)
            name = tk.Label(card, text="-", fg=COLORS["text"], bg=COLORS["panel"], anchor="w", font=("Malgun Gothic", 12, "bold"))
            name.pack(fill="x", padx=10, pady=(8, 2))
            meta = tk.Label(card, text="", fg=COLORS["gold"], bg=COLORS["panel"], anchor="w", font=("Segoe UI", 9, "bold"))
            meta.pack(fill="x", padx=10)
            reason = tk.Label(card, text="", fg=COLORS["muted"], bg=COLORS["panel"], justify="left", anchor="w", wraplength=430, font=("Malgun Gothic", 9))
            reason.pack(fill="x", padx=10, pady=(2, 8))
            self.cards.append((card, name, meta, reason))

    def _begin_drag(self, event):
        self.drag_start = (event.x_root, event.y_root, self.root.winfo_x(), self.root.winfo_y())

    def _drag(self, event):
        if not self.drag_start:
            return
        start_x, start_y, win_x, win_y = self.drag_start
        self.root.geometry(f"+{win_x + event.x_root - start_x}+{win_y + event.y_root - start_y}")

    def _toggle_topmost(self):
        current = bool(self.root.attributes("-topmost"))
        self.root.attributes("-topmost", not current)

    def _on_target_change(self, _event=None):
        self.selected_value = self.label_to_value.get(self.target_var.get(), self.selected_value)
        self._render_current()

    def _start_polling(self):
        thread = threading.Thread(target=self._poll_loop, daemon=True)
        thread.start()

    def _poll_loop(self):
        while True:
            try:
                payload = fetch_json(API_URL)
                self.events.put(("data", payload))
            except HTTPError as error:
                if error.code == 503:
                    self.events.put(("error", "리플레이 API 대기 중"))
                else:
                    self.events.put(("error", f"HTTP {error.code}"))
            except URLError:
                self.events.put(("error", "추천 서버 연결 실패"))
            except json.JSONDecodeError:
                self.events.put(("error", "데이터 해석 오류"))
            except (TimeoutError, OSError) as error:
                self.events.put(("error", f"연결 대기: {error}"))
            time.sleep(POLL_MS / 1000)

    def _process_events(self):
        try:
            while True:
                kind, payload = self.events.get_nowait()
                if kind == "data":
                    self.payload = payload
                    self._update_from_payload(payload)
                else:
                    self.status_var.set(str(payload))
        except queue.Empty:
            pass
        self.root.after(250, self._process_events)

    def _update_from_payload(self, payload):
        live = payload.get("live") or {}
        self.players = live.get("allPlayers") or []
        game_time = ((payload.get("replay") or {}).get("time") or (live.get("gameData") or {}).get("gameTime") or 0)
        self.time_var.set(format_seconds(game_time))
        if not self.players:
            self.status_var.set("LoL 리플레이 데이터를 기다리는 중")
            return

        self._update_target_options()
        self._render_current()

    def _update_target_options(self):
        self.label_to_value = {}
        labels = []
        for index, player in enumerate(self.players):
            value = player_value(player, index)
            label = player_label(player)
            self.label_to_value[label] = value
            labels.append(label)

        if self.selected_value not in self.label_to_value.values():
            self.selected_value = self.label_to_value[labels[0]]

        self.target_combo["values"] = labels
        selected_label = next((label for label, value in self.label_to_value.items() if value == self.selected_value), labels[0])
        if self.target_var.get() != selected_label:
            self.target_var.set(selected_label)

    def _render_current(self):
        if not self.players:
            return
        target = None
        for index, player in enumerate(self.players):
            if player_value(player, index) == self.selected_value:
                target = player
                break
        target = target or self.players[0]

        live = (getattr(self, "payload", {}) or {}).get("live") or {}
        gold_info = estimate_available_gold(target, live)
        self.gold_var.set(f"{gold_info['gold']}g")
        self.gold_note_var.set(gold_info["source"])

        champion_key, archetype, damage_profile, threat, recommendations, profile, completed_cores, meta_sequences, ally_antiheal_count = recommend(target, self.players, gold_info)
        owned = [item.get("displayName") or f"#{item.get('itemID')}" for item in (target.get("items") or [])]
        owned_ids = {item.get("itemID") for item in (target.get("items") or [])}
        owned_text = ", ".join(owned[:3]) if owned else "보유 아이템 없음"
        self.status_var.set(f"{target.get('championName', champion_key)} / {archetype} / {gold_info['source']} {gold_info['gold']}g")
        primary_threat = threat.get("primary") or "뚜렷한 단일 성장 위협 없음"
        meta_text = format_meta_comparison(meta_sequences, owned_ids)
        confidence = recommendation_confidence(recommendations)
        save_latest_recommendation(
            recommendation_snapshot(
                target,
                archetype,
                damage_profile,
                threat,
                recommendations,
                confidence,
                gold_info,
                completed_cores,
                profile,
                meta_sequences,
                ally_antiheal_count,
            )
        )
        if not meta_sequences and not current_build_stats():
            meta_text += " · data/master_plus_build_stats.json 필요"
        self.summary.configure(
            text=(
                f"빌드 {completed_cores}/{len(profile.get('core', []))}코어 · 내 딜 {damage_profile['label']} · AD {threat['physical']} · AP {threat['magic']} · 치명타 {threat.get('crit', 0)} · 회복 {threat['healing']} · 보호막 {threat.get('shielding', 0)} · 팀 치감 {ally_antiheal_count}명 · 탱킹 {threat['tank']} · 폭딜 {threat.get('fedBurst', 0)}\n"
                f"추천 확신: {confidence['label']} · {confidence['detail']}\n"
                f"핵심 위협: {primary_threat}\n"
                f"폭딜 추정: {threat.get('topBurst') or '뚜렷한 원콤 위협 없음'}\n"
                f"상대 내구 추정: 평균 방어 {threat.get('avgArmorValue', 0)} · 평균 마저 {threat.get('avgMrValue', 0)} · 물리EHP {threat.get('physicalEhpValue', 0)} · 마법EHP {threat.get('magicEhpValue', 0)}\n"
                f"{meta_text}\n"
                f"{owned_text}\n"
                f"골드 계산: {gold_info['detail']}"
            )
        )

        for index, widgets in enumerate(self.cards):
            _card, name_label, meta_label, reason_label = widgets
            if index >= len(recommendations):
                name_label.configure(text="-")
                meta_label.configure(text="")
                reason_label.configure(text="")
                continue
            entry = recommendations[index]
            item = entry["item"]
            next_buy = entry["next_buy"]
            if next_buy["id"] == item["id"]:
                name_label.configure(text=f"{index + 1}. 완성: {item['name']}")
            else:
                name_label.configure(text=f"{index + 1}. {next_buy['name']} → {item['name']}")
            if next_buy["kind"] == "component":
                buy_state = "구매 가능" if next_buy["cost"] <= gold_info["gold"] else f"{next_buy['cost'] - gold_info['gold']}g 부족"
                meta_label.configure(text=f"다음 {next_buy['cost']}g · 목표 {item['cost']}g · {buy_state} · {purchase_timing_label(entry, gold_info['gold'])} · 점수 {entry['score']}")
            else:
                ready = "완성 가능" if entry["missing"] == 0 else f"{entry['missing']}g 부족"
                meta_label.configure(text=f"목표 {item['cost']}g · {ready} · {purchase_timing_label(entry, gold_info['gold'])} · 점수 {entry['score']}")
            reason_label.configure(text="\n".join(entry["breakdown"]))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    OverlayApp().run()
