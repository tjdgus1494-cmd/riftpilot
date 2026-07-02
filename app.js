"use strict";

const CHAMPION_HINTS = {
  Aatrox: { archetype: "fighter", damage: "physical", heal: 4, cc: 2, tank: 2 },
  Ahri: { archetype: "mage", damage: "magic", burst: 3, cc: 2 },
  Akali: { archetype: "assassin", damage: "magic", burst: 4 },
  Alistar: { archetype: "support", damage: "magic", tank: 4, cc: 5 },
  Amumu: { archetype: "tank", damage: "magic", tank: 4, cc: 4 },
  Ashe: { archetype: "marksman", damage: "physical", cc: 3 },
  Azir: { archetype: "mage", damage: "magic", burst: 2 },
  Blitzcrank: { archetype: "support", damage: "magic", tank: 3, cc: 4 },
  Brand: { archetype: "mage", damage: "magic", burst: 4 },
  Caitlyn: { archetype: "marksman", damage: "physical", burst: 2 },
  Darius: { archetype: "fighter", damage: "physical", heal: 2, tank: 2 },
  Draven: { archetype: "marksman", damage: "physical", burst: 4 },
  Ekko: { archetype: "assassin", damage: "magic", burst: 4 },
  Ezreal: { archetype: "marksman", damage: "physical", burst: 2 },
  Fiora: { archetype: "fighter", damage: "physical", heal: 3, burst: 2 },
  Galio: { archetype: "tank", damage: "magic", tank: 3, cc: 4 },
  Garen: { archetype: "fighter", damage: "physical", tank: 3 },
  Graves: { archetype: "marksman", damage: "physical", burst: 3 },
  Hwei: { archetype: "mage", damage: "magic", burst: 4, cc: 2 },
  Irelia: { archetype: "fighter", damage: "physical", heal: 2, burst: 3 },
  Janna: { archetype: "support", damage: "magic", cc: 3 },
  Jax: { archetype: "fighter", damage: "physical", tank: 2, burst: 2 },
  Jhin: { archetype: "marksman", damage: "physical", burst: 3, cc: 2 },
  Jinx: { archetype: "marksman", damage: "physical" },
  KaiSa: { archetype: "marksman", damage: "mixed", burst: 3 },
  Karma: { archetype: "support", damage: "magic", cc: 2 },
  Kassadin: { archetype: "assassin", damage: "magic", burst: 4 },
  Katarina: { archetype: "assassin", damage: "magic", heal: 2, burst: 5 },
  Kayle: { archetype: "mage", damage: "mixed", burst: 2 },
  KhaZix: { archetype: "assassin", damage: "physical", burst: 5 },
  LeeSin: { archetype: "fighter", damage: "physical", burst: 3 },
  Leona: { archetype: "support", damage: "magic", tank: 4, cc: 5 },
  Lillia: { archetype: "mage", damage: "magic", cc: 2 },
  Lulu: { archetype: "support", damage: "magic", cc: 2 },
  Lucian: { archetype: "marksman", damage: "physical", burst: 3 },
  Lux: { archetype: "mage", damage: "magic", burst: 4, cc: 2 },
  Malphite: { archetype: "tank", damage: "magic", tank: 4, cc: 3 },
  MasterYi: { archetype: "fighter", damage: "physical", heal: 2, burst: 3 },
  MissFortune: { archetype: "marksman", damage: "physical", burst: 3 },
  Milio: { archetype: "support", damage: "magic" },
  Mordekaiser: { archetype: "fighter", damage: "magic", heal: 2, tank: 3 },
  Morgana: { archetype: "mage", damage: "magic", cc: 3 },
  Nami: { archetype: "support", damage: "magic", cc: 3 },
  Nautilus: { archetype: "support", damage: "magic", tank: 4, cc: 5 },
  Nidalee: { archetype: "mage", damage: "magic", heal: 2, burst: 3 },
  Orianna: { archetype: "mage", damage: "magic", burst: 3 },
  Ornn: { archetype: "tank", damage: "magic", tank: 5, cc: 4 },
  Pyke: { archetype: "support", damage: "physical", burst: 4, cc: 3 },
  Qiyana: { archetype: "assassin", damage: "physical", burst: 5, cc: 2 },
  Rakan: { archetype: "support", damage: "magic", cc: 4 },
  Rammus: { archetype: "tank", damage: "magic", tank: 5, cc: 4 },
  Rell: { archetype: "support", damage: "magic", tank: 4, cc: 5 },
  Renekton: { archetype: "fighter", damage: "physical", heal: 2, tank: 2 },
  Riven: { archetype: "fighter", damage: "physical", burst: 3, cc: 2 },
  Samira: { archetype: "marksman", damage: "physical", heal: 2, burst: 4 },
  Senna: { archetype: "support", damage: "physical", heal: 2 },
  Seraphine: { archetype: "support", damage: "magic", cc: 3 },
  Sett: { archetype: "fighter", damage: "physical", tank: 3, cc: 2 },
  Shen: { archetype: "tank", damage: "mixed", tank: 4, cc: 3 },
  Sion: { archetype: "tank", damage: "physical", tank: 5, cc: 3 },
  Sivir: { archetype: "marksman", damage: "physical" },
  Sylas: { archetype: "fighter", damage: "magic", heal: 4, burst: 3 },
  Syndra: { archetype: "mage", damage: "magic", burst: 5, cc: 2 },
  TahmKench: { archetype: "tank", damage: "magic", tank: 5, cc: 2 },
  Talon: { archetype: "assassin", damage: "physical", burst: 5 },
  Thresh: { archetype: "support", damage: "magic", tank: 2, cc: 4 },
  Tristana: { archetype: "marksman", damage: "physical", burst: 3 },
  Tryndamere: { archetype: "fighter", damage: "physical", heal: 2, burst: 3 },
  TwistedFate: { archetype: "mage", damage: "magic", cc: 2 },
  Varus: { archetype: "marksman", damage: "mixed", burst: 3, cc: 2 },
  Vayne: { archetype: "marksman", damage: "physical", burst: 3 },
  Veigar: { archetype: "mage", damage: "magic", burst: 5, cc: 2 },
  Viego: { archetype: "fighter", damage: "physical", heal: 2, burst: 3 },
  Vi: { archetype: "fighter", damage: "physical", burst: 3, cc: 3 },
  Viktor: { archetype: "mage", damage: "magic", burst: 4 },
  Vladimir: { archetype: "mage", damage: "magic", heal: 5, burst: 3 },
  Yasuo: { archetype: "fighter", damage: "physical", burst: 3 },
  Yone: { archetype: "fighter", damage: "mixed", burst: 4 },
  Yunara: { archetype: "marksman", damage: "physical", burst: 2 },
  Yuumi: { archetype: "support", damage: "magic", heal: 4 },
  Zed: { archetype: "assassin", damage: "physical", burst: 5 },
  Ziggs: { archetype: "mage", damage: "magic", burst: 3 },
  Zilean: { archetype: "support", damage: "magic", cc: 2 },
  Zoe: { archetype: "mage", damage: "magic", burst: 5 },
  Zyra: { archetype: "mage", damage: "magic", cc: 3 }
};

const COMPONENTS = {
  1001: { id: 1001, name: "장화", cost: 300 },
  1026: { id: 1026, name: "방출의 마법봉", cost: 850 },
  1031: { id: 1031, name: "쇠사슬 조끼", cost: 800 },
  1033: { id: 1033, name: "마법무효화의 망토", cost: 450 },
  1036: { id: 1036, name: "롱소드", cost: 350 },
  1037: { id: 1037, name: "곡괭이", cost: 875 },
  1038: { id: 1038, name: "B. F. 대검", cost: 1300 },
  1042: { id: 1042, name: "단검", cost: 300 },
  1043: { id: 1043, name: "곡궁", cost: 700 },
  1052: { id: 1052, name: "증폭의 고서", cost: 400 },
  1053: { id: 1053, name: "흡혈의 낫", cost: 900 },
  1057: { id: 1057, name: "음전자 망토", cost: 900 },
  1058: { id: 1058, name: "쓸데없이 큰 지팡이", cost: 1250 },
  1011: { id: 1011, name: "거인의 허리띠", cost: 900 },
  1018: { id: 1018, name: "민첩성의 망토", cost: 600 },
  2022: { id: 2022, name: "빛나는 티끌", cost: 250 },
  2420: { id: 2420, name: "초시계", cost: 750 },
  3067: { id: 3067, name: "점화석", cost: 800 },
  3070: { id: 3070, name: "여신의 눈물", cost: 400 },
  3133: { id: 3133, name: "콜필드의 전투 망치", cost: 1100 },
  3134: { id: 3134, name: "톱날 단검", cost: 1000 },
  3140: { id: 3140, name: "수은 장식띠", cost: 1300 },
  4630: { id: 4630, name: "역병의 보석", cost: 1100 },
  6660: { id: 6660, name: "바미의 불씨", cost: 900 },
  6670: { id: 6670, name: "절정의 화살", cost: 1300 }
};

const ITEM_CANDIDATES = [
  {
    id: 3006,
    name: "광전사의 군화",
    cost: 1100,
    roles: ["marksman", "fighter"],
    tags: ["boots", "attackSpeed", "tempo"],
    components: [1001, 1042],
    priority: 42
  },
  {
    id: 3047,
    name: "판금 장화",
    cost: 1200,
    roles: ["marksman", "fighter", "tank", "support"],
    tags: ["boots", "armor", "antiAuto", "defense"],
    components: [1001, 1031],
    priority: 42
  },
  {
    id: 3111,
    name: "헤르메스의 발걸음",
    cost: 1200,
    roles: ["mage", "assassin", "fighter", "tank", "support"],
    tags: ["boots", "magicResist", "tenacity", "defense"],
    components: [1001, 1033],
    priority: 42
  },
  {
    id: 3020,
    name: "마법사의 신발",
    cost: 1100,
    roles: ["mage", "assassin"],
    tags: ["boots", "magicPen", "tempo"],
    components: [1001],
    priority: 38
  },
  {
    id: 3158,
    name: "명석함의 아이오니아 장화",
    cost: 900,
    roles: ["mage", "fighter", "support", "assassin"],
    tags: ["boots", "haste", "utility"],
    components: [1001],
    priority: 36
  },
  {
    id: 3031,
    name: "무한의 대검",
    cost: 3450,
    roles: ["marksman"],
    tags: ["attackDamage", "crit", "burst", "scaling"],
    components: [1038, 1018],
    priority: 80
  },
  {
    id: 6672,
    name: "크라켄 학살자",
    cost: 3100,
    roles: ["marksman", "fighter"],
    tags: ["attackDamage", "attackSpeed", "antiTank", "duel", "tempo"],
    components: [6670, 1043],
    priority: 78
  },
  {
    id: 3033,
    name: "필멸자의 운명",
    cost: 3000,
    roles: ["marksman", "fighter"],
    tags: ["attackDamage", "crit", "antiheal", "armorPen"],
    components: [1037, 1018],
    priority: 62
  },
  {
    id: 3036,
    name: "도미닉 경의 인사",
    cost: 3000,
    roles: ["marksman"],
    tags: ["attackDamage", "crit", "armorPen", "antiTank"],
    components: [1037, 1018],
    priority: 65
  },
  {
    id: 3072,
    name: "피바라기",
    cost: 3400,
    roles: ["marksman", "fighter"],
    tags: ["attackDamage", "lifesteal", "shield", "defense"],
    components: [1038, 1053],
    priority: 58
  },
  {
    id: 3026,
    name: "수호 천사",
    cost: 3200,
    roles: ["marksman", "assassin", "fighter"],
    tags: ["attackDamage", "armor", "antiBurst", "defense"],
    components: [1038, 1031],
    priority: 54
  },
  {
    id: 3089,
    name: "라바돈의 죽음모자",
    cost: 3600,
    roles: ["mage", "assassin"],
    tags: ["abilityPower", "burst", "scaling"],
    components: [1058, 1058],
    priority: 80
  },
  {
    id: 3135,
    name: "공허의 지팡이",
    cost: 3000,
    roles: ["mage"],
    tags: ["abilityPower", "magicPen", "antiTank"],
    components: [4630, 1026],
    priority: 66
  },
  {
    id: 3165,
    name: "모렐로노미콘",
    cost: 2200,
    roles: ["mage", "support"],
    tags: ["abilityPower", "antiheal", "haste"],
    components: [1052, 2022],
    priority: 58
  },
  {
    id: 3157,
    name: "존야의 모래시계",
    cost: 3250,
    roles: ["mage", "assassin", "support"],
    tags: ["abilityPower", "armor", "antiBurst", "stasis", "defense"],
    components: [2420, 1031, 1026],
    priority: 64
  },
  {
    id: 6653,
    name: "리안드리의 고통",
    cost: 3000,
    roles: ["mage"],
    tags: ["abilityPower", "health", "antiTank", "burn"],
    components: [1052, 1011],
    priority: 67
  },
  {
    id: 3102,
    name: "밴시의 장막",
    cost: 3000,
    roles: ["mage"],
    tags: ["abilityPower", "magicResist", "antiBurst", "defense"],
    components: [1057, 1026],
    priority: 56
  },
  {
    id: 3071,
    name: "칠흑의 양날 도끼",
    cost: 3000,
    roles: ["fighter", "assassin"],
    tags: ["attackDamage", "health", "haste", "armorShred", "antiTank"],
    components: [3133, 1011],
    priority: 73
  },
  {
    id: 3053,
    name: "스테락의 도전",
    cost: 3200,
    roles: ["fighter", "tank"],
    tags: ["attackDamage", "health", "shield", "antiBurst", "defense"],
    components: [1037, 1011],
    priority: 63
  },
  {
    id: 6333,
    name: "죽음의 무도",
    cost: 3200,
    roles: ["fighter", "assassin"],
    tags: ["attackDamage", "armor", "antiBurst", "haste"],
    components: [3133, 1031],
    priority: 60
  },
  {
    id: 3156,
    name: "맬모셔스의 아귀",
    cost: 3100,
    roles: ["fighter", "assassin", "marksman"],
    tags: ["attackDamage", "magicResist", "shield", "antiBurst"],
    components: [3133, 1057],
    priority: 58
  },
  {
    id: 3075,
    name: "가시 갑옷",
    cost: 2700,
    roles: ["tank", "support", "fighter"],
    tags: ["armor", "antiheal", "antiAuto", "defense"],
    components: [1031, 1031],
    priority: 67
  },
  {
    id: 3068,
    name: "태양불꽃 방패",
    cost: 2700,
    roles: ["tank", "fighter"],
    tags: ["health", "armor", "waveclear", "damage"],
    components: [6660, 1031],
    priority: 62
  },
  {
    id: 4401,
    name: "대자연의 힘",
    cost: 2800,
    roles: ["tank", "fighter", "support"],
    tags: ["magicResist", "health", "speed", "defense"],
    components: [1057, 1011],
    priority: 64
  },
  {
    id: 3143,
    name: "란두인의 예언",
    cost: 2700,
    roles: ["tank", "fighter", "support"],
    tags: ["armor", "health", "antiCrit", "antiAuto", "defense"],
    components: [1031, 1011],
    priority: 61
  },
  {
    id: 3110,
    name: "얼어붙은 심장",
    cost: 2500,
    roles: ["tank", "support", "fighter"],
    tags: ["armor", "haste", "antiAuto", "defense"],
    components: [1031, 3067],
    priority: 58
  },
  {
    id: 3065,
    name: "정령의 형상",
    cost: 2900,
    roles: ["tank", "fighter"],
    tags: ["magicResist", "health", "healingAmp", "defense"],
    components: [1057, 3067],
    priority: 57
  },
  {
    id: 6665,
    name: "작쇼",
    cost: 3200,
    roles: ["tank", "fighter"],
    tags: ["armor", "magicResist", "health", "scaling", "defense"],
    components: [1031, 1057, 1011],
    priority: 69
  },
  {
    id: 3190,
    name: "강철의 솔라리 펜던트",
    cost: 2200,
    roles: ["support", "tank"],
    tags: ["armor", "magicResist", "shield", "utility", "teamfight"],
    components: [1031, 1033],
    priority: 64
  },
  {
    id: 3107,
    name: "구원",
    cost: 2300,
    roles: ["support"],
    tags: ["healShield", "utility", "teamfight"],
    components: [3067],
    priority: 62
  },
  {
    id: 6617,
    name: "월석 재생기",
    cost: 2200,
    roles: ["support"],
    tags: ["healShield", "abilityPower", "teamfight"],
    components: [1052, 3067],
    priority: 63
  },
  {
    id: 3222,
    name: "미카엘의 축복",
    cost: 2300,
    roles: ["support"],
    tags: ["magicResist", "cleanse", "healShield", "utility"],
    components: [1033, 3067],
    priority: 58
  },
  {
    id: 3504,
    name: "불타는 향로",
    cost: 2200,
    roles: ["support"],
    tags: ["healShield", "attackSpeed", "utility"],
    components: [1052, 2022],
    priority: 56
  }
];

const ENEMY_PROFILES = {
  balanced: { physical: 5, magic: 5, healing: 2, tank: 3, cc: 3, burst: 3 },
  physical: { physical: 8, magic: 3, healing: 2, tank: 3, cc: 3, burst: 4 },
  magic: { physical: 3, magic: 8, healing: 2, tank: 3, cc: 3, burst: 4 },
  healing: { physical: 5, magic: 5, healing: 8, tank: 4, cc: 3, burst: 3 },
  tank: { physical: 5, magic: 5, healing: 3, tank: 8, cc: 3, burst: 2 },
  cc: { physical: 5, magic: 5, healing: 2, tank: 3, cc: 8, burst: 3 }
};

const SAMPLE_LIVE_DATA = {
  activePlayer: {
    summonerName: "Demo Player",
    championStats: {},
    currentGold: 2200
  },
  allPlayers: [
    {
      summonerName: "Demo Player",
      championName: "KaiSa",
      team: "ORDER",
      items: [
        { itemID: 1001, displayName: "장화" },
        { itemID: 1037, displayName: "곡괭이" }
      ]
    },
    { summonerName: "Enemy Top", championName: "Darius", team: "CHAOS", items: [{ itemID: 3071, displayName: "칠흑의 양날 도끼" }] },
    { summonerName: "Enemy Jungle", championName: "Lillia", team: "CHAOS", items: [{ itemID: 6653, displayName: "리안드리의 고통" }] },
    { summonerName: "Enemy Mid", championName: "Ahri", team: "CHAOS", items: [{ itemID: 1058, displayName: "쓸데없이 큰 지팡이" }] },
    { summonerName: "Enemy Bot", championName: "Samira", team: "CHAOS", items: [{ itemID: 1053, displayName: "흡혈의 낫" }] },
    { summonerName: "Enemy Support", championName: "Yuumi", team: "CHAOS", items: [{ itemID: 6617, displayName: "월석 재생기" }] }
  ]
};

const REPLAY_TIMELINE = [
  {
    minute: 4,
    label: "첫 귀환 직전",
    data: {
      activePlayer: { summonerName: "Replay Player", currentGold: 900 },
      allPlayers: [
        { summonerName: "Replay Player", championName: "KaiSa", team: "ORDER", items: [{ itemID: 1036, displayName: "롱소드" }] },
        { summonerName: "Enemy Top", championName: "Darius", team: "CHAOS", items: [{ itemID: 1036, displayName: "롱소드" }] },
        { summonerName: "Enemy Jungle", championName: "Lillia", team: "CHAOS", items: [{ itemID: 1052, displayName: "증폭의 고서" }] },
        { summonerName: "Enemy Mid", championName: "Ahri", team: "CHAOS", items: [{ itemID: 1052, displayName: "증폭의 고서" }] },
        { summonerName: "Enemy Bot", championName: "Samira", team: "CHAOS", items: [{ itemID: 1036, displayName: "롱소드" }] },
        { summonerName: "Enemy Support", championName: "Yuumi", team: "CHAOS", items: [] }
      ]
    }
  },
  {
    minute: 9.5,
    label: "라인전 회복 압박",
    data: {
      activePlayer: { summonerName: "Replay Player", currentGold: 1450 },
      allPlayers: [
        { summonerName: "Replay Player", championName: "KaiSa", team: "ORDER", items: [{ itemID: 1001, displayName: "장화" }, { itemID: 1037, displayName: "곡괭이" }] },
        { summonerName: "Enemy Top", championName: "Darius", team: "CHAOS", items: [{ itemID: 3067, displayName: "점화석" }] },
        { summonerName: "Enemy Jungle", championName: "Lillia", team: "CHAOS", items: [{ itemID: 1026, displayName: "방출의 마법봉" }] },
        { summonerName: "Enemy Mid", championName: "Ahri", team: "CHAOS", items: [{ itemID: 1058, displayName: "쓸데없이 큰 지팡이" }] },
        { summonerName: "Enemy Bot", championName: "Samira", team: "CHAOS", items: [{ itemID: 1053, displayName: "흡혈의 낫" }] },
        { summonerName: "Enemy Support", championName: "Yuumi", team: "CHAOS", items: [{ itemID: 2022, displayName: "빛나는 티끌" }] }
      ]
    }
  },
  {
    minute: 17,
    label: "앞라인 성장",
    data: {
      activePlayer: { summonerName: "Replay Player", currentGold: 2300 },
      allPlayers: [
        { summonerName: "Replay Player", championName: "KaiSa", team: "ORDER", items: [{ itemID: 3006, displayName: "광전사의 군화" }, { itemID: 6670, displayName: "절정의 화살" }, { itemID: 1037, displayName: "곡괭이" }] },
        { summonerName: "Enemy Top", championName: "Darius", team: "CHAOS", items: [{ itemID: 3071, displayName: "칠흑의 양날 도끼" }, { itemID: 1031, displayName: "쇠사슬 조끼" }] },
        { summonerName: "Enemy Jungle", championName: "Rammus", team: "CHAOS", items: [{ itemID: 6660, displayName: "바미의 불씨" }, { itemID: 1031, displayName: "쇠사슬 조끼" }] },
        { summonerName: "Enemy Mid", championName: "Ahri", team: "CHAOS", items: [{ itemID: 3102, displayName: "밴시의 장막" }] },
        { summonerName: "Enemy Bot", championName: "Samira", team: "CHAOS", items: [{ itemID: 1053, displayName: "흡혈의 낫" }, { itemID: 1018, displayName: "민첩성의 망토" }] },
        { summonerName: "Enemy Support", championName: "Yuumi", team: "CHAOS", items: [{ itemID: 6617, displayName: "월석 재생기" }] }
      ]
    }
  },
  {
    minute: 26,
    label: "후반 한타 준비",
    data: {
      activePlayer: { summonerName: "Replay Player", currentGold: 3200 },
      allPlayers: [
        { summonerName: "Replay Player", championName: "KaiSa", team: "ORDER", items: [{ itemID: 3006, displayName: "광전사의 군화" }, { itemID: 6672, displayName: "크라켄 학살자" }, { itemID: 3033, displayName: "필멸자의 운명" }, { itemID: 1018, displayName: "민첩성의 망토" }] },
        { summonerName: "Enemy Top", championName: "Darius", team: "CHAOS", items: [{ itemID: 3071, displayName: "칠흑의 양날 도끼" }, { itemID: 3053, displayName: "스테락의 도전" }] },
        { summonerName: "Enemy Jungle", championName: "Rammus", team: "CHAOS", items: [{ itemID: 3075, displayName: "가시 갑옷" }, { itemID: 3143, displayName: "란두인의 예언" }] },
        { summonerName: "Enemy Mid", championName: "Ahri", team: "CHAOS", items: [{ itemID: 3089, displayName: "라바돈의 죽음모자" }, { itemID: 3102, displayName: "밴시의 장막" }] },
        { summonerName: "Enemy Bot", championName: "Samira", team: "CHAOS", items: [{ itemID: 3072, displayName: "피바라기" }, { itemID: 3031, displayName: "무한의 대검" }] },
        { summonerName: "Enemy Support", championName: "Yuumi", team: "CHAOS", items: [{ itemID: 6617, displayName: "월석 재생기" }, { itemID: 3107, displayName: "구원" }] }
      ]
    }
  }
];

const state = {
  mode: "demo",
  watchMode: false,
  ddragon: null,
  itemData: {},
  championData: {},
  liveData: null,
  liveError: null,
  actualReplay: null,
  actualReplayError: null,
  actualReplayPollTimer: null,
  replayIndex: 0,
  replayPlaying: false,
  replayTimer: null,
  pollTimer: null,
  toastTimer: null
};

const els = {};

document.addEventListener("DOMContentLoaded", init);

function init() {
  initializeViewMode();
  bindElements();
  populateChampionSelect();
  configureReplayControls();
  bindEvents();
  if (state.watchMode) {
    setMode("replayLive");
  } else {
    render();
  }
  loadDataDragon();
}

function initializeViewMode() {
  const params = new URLSearchParams(window.location.search);
  state.watchMode = params.get("view") === "watch";
  document.body.classList.toggle("watch-mode", state.watchMode);
}

function bindElements() {
  [
    "patchLine",
    "modeDemo",
    "modeLive",
    "modeReplay",
    "modeReplayLive",
    "refreshButton",
    "watchModeButton",
    "connectionBadge",
    "championSelect",
    "archetypeSelect",
    "goldInput",
    "enemyProfileSelect",
    "snowballToggle",
    "behindToggle",
    "replayPanel",
    "replayTime",
    "replaySlider",
    "replayPrev",
    "replayPlay",
    "replayNext",
    "replayLabel",
    "actualReplayPanel",
    "actualReplayState",
    "actualReplayTime",
    "actualReplaySpeed",
    "actualReplayTarget",
    "actualReplayBack",
    "actualReplayPlay",
    "actualReplayForward",
    "actualReplayNote",
    "ownedItems",
    "physicalMeter",
    "magicMeter",
    "healMeter",
    "tankMeter",
    "contextLine",
    "goldBadge",
    "recommendations",
    "analysisList",
    "nextBuys",
    "toast"
  ].forEach((id) => {
    els[id] = document.getElementById(id);
  });
}

function populateChampionSelect() {
  const champions = Object.keys(CHAMPION_HINTS).sort((a, b) => a.localeCompare(b));
  els.championSelect.innerHTML = champions
    .map((key) => `<option value="${escapeHtml(key)}">${escapeHtml(formatChampionName(key))}</option>`)
    .join("");
  els.championSelect.value = "KaiSa";
  els.archetypeSelect.value = CHAMPION_HINTS.KaiSa.archetype;
}

function bindEvents() {
  els.watchModeButton.textContent = state.watchMode ? "일반모드" : "영상모드";
  els.modeDemo.addEventListener("click", () => setMode("demo"));
  els.modeLive.addEventListener("click", () => setMode("live"));
  els.modeReplay.addEventListener("click", () => setMode("replay"));
  els.modeReplayLive.addEventListener("click", () => setMode("replayLive"));
  els.watchModeButton.addEventListener("click", toggleWatchMode);
  els.refreshButton.addEventListener("click", () => {
    if (state.mode === "live") {
      fetchLiveData(true);
    } else if (state.mode === "replayLive") {
      fetchActualReplay(true);
    } else if (state.mode === "replay") {
      setReplayIndex(state.replayIndex);
      showToast("현재 리플레이 장면으로 다시 계산했습니다.");
    } else {
      render();
      showToast("데모 조건으로 다시 계산했습니다.");
    }
  });

  els.replaySlider.addEventListener("input", () => {
    stopReplay();
    setReplayIndex(Number(els.replaySlider.value));
  });
  els.replayPrev.addEventListener("click", () => {
    stopReplay();
    setReplayIndex(state.replayIndex - 1);
  });
  els.replayNext.addEventListener("click", () => {
    stopReplay();
    setReplayIndex(state.replayIndex + 1);
  });
  els.replayPlay.addEventListener("click", () => {
    if (state.replayPlaying) {
      stopReplay();
    } else {
      startReplay();
    }
  });
  els.actualReplayBack.addEventListener("click", () => seekActualReplay(-10));
  els.actualReplayForward.addEventListener("click", () => seekActualReplay(10));
  els.actualReplayPlay.addEventListener("click", toggleActualReplayPlay);
  els.actualReplayTarget.addEventListener("change", () => {
    if (state.actualReplay?.live) {
      syncControlsFromLive(state.actualReplay.live);
    }
    render();
  });

  els.championSelect.addEventListener("change", () => {
    const hint = CHAMPION_HINTS[els.championSelect.value];
    if (hint) els.archetypeSelect.value = hint.archetype;
    render();
  });

  [
    els.archetypeSelect,
    els.goldInput,
    els.enemyProfileSelect,
    els.snowballToggle,
    els.behindToggle
  ].forEach((el) => {
    el.addEventListener("input", render);
    el.addEventListener("change", render);
  });
}

function toggleWatchMode() {
  const url = new URL(window.location.href);
  url.searchParams.set("v", "7");
  if (state.watchMode) {
    url.searchParams.delete("view");
  } else {
    url.searchParams.set("view", "watch");
  }
  window.location.href = url.toString();
}

function configureReplayControls() {
  els.replaySlider.max = String(REPLAY_TIMELINE.length - 1);
  els.replaySlider.value = String(state.replayIndex);
  updateReplayControls();
}

function setMode(mode) {
  state.mode = mode;
  els.modeDemo.classList.toggle("is-active", mode === "demo");
  els.modeLive.classList.toggle("is-active", mode === "live");
  els.modeReplay.classList.toggle("is-active", mode === "replay");
  els.modeReplayLive.classList.toggle("is-active", mode === "replayLive");

  window.clearInterval(state.pollTimer);
  state.pollTimer = null;
  window.clearInterval(state.actualReplayPollTimer);
  state.actualReplayPollTimer = null;

  if (mode === "live") {
    stopReplay();
    state.actualReplay = null;
    state.actualReplayError = null;
    fetchLiveData(true);
    state.pollTimer = window.setInterval(() => fetchLiveData(false), 4500);
  } else if (mode === "replay") {
    state.actualReplay = null;
    state.actualReplayError = null;
    state.liveError = null;
    setReplayIndex(state.replayIndex);
  } else if (mode === "replayLive") {
    stopReplay();
    state.liveError = null;
    fetchActualReplay(true);
    state.actualReplayPollTimer = window.setInterval(() => fetchActualReplay(false), 1200);
  } else {
    stopReplay();
    state.liveError = null;
    state.actualReplay = null;
    state.actualReplayError = null;
    render();
  }
  updateReplayControls();
  updateActualReplayControls();
}

function startReplay() {
  if (state.replayIndex >= REPLAY_TIMELINE.length - 1) {
    setReplayIndex(0);
  }
  state.replayPlaying = true;
  window.clearInterval(state.replayTimer);
  state.replayTimer = window.setInterval(() => {
    if (state.replayIndex >= REPLAY_TIMELINE.length - 1) {
      stopReplay();
      return;
    }
    const nextIndex = state.replayIndex + 1;
    setReplayIndex(nextIndex);
    if (nextIndex >= REPLAY_TIMELINE.length - 1) {
      stopReplay();
    }
  }, 1900);
  updateReplayControls();
}

function stopReplay() {
  window.clearInterval(state.replayTimer);
  state.replayTimer = null;
  state.replayPlaying = false;
  updateReplayControls();
}

function setReplayIndex(index) {
  state.replayIndex = clamp(Math.round(index), 0, REPLAY_TIMELINE.length - 1);
  syncControlsFromLive(REPLAY_TIMELINE[state.replayIndex].data);
  updateReplayControls();
  render();
}

function updateReplayControls() {
  if (!els.replayPanel) return;
  const frame = REPLAY_TIMELINE[state.replayIndex];
  els.replayPanel.hidden = state.mode !== "replay";
  els.replaySlider.value = String(state.replayIndex);
  els.replayTime.textContent = formatMinute(frame.minute);
  els.replayLabel.textContent = frame.label;
  els.replayPrev.disabled = state.replayIndex === 0;
  els.replayNext.disabled = state.replayIndex === REPLAY_TIMELINE.length - 1;
  els.replayPlay.textContent = state.replayPlaying ? "정지" : "재생";
}

function updateActualReplayControls() {
  if (!els.actualReplayPanel) return;
  const payload = state.actualReplay;
  const playback = payload?.replay;
  els.actualReplayPanel.hidden = state.mode !== "replayLive";

  if (state.mode !== "replayLive") return;

  if (playback) {
    els.actualReplayState.className = `badge ${playback.paused ? "warn" : "good"}`;
    els.actualReplayState.textContent = playback.paused ? "정지" : "재생";
    els.actualReplayTime.textContent = formatSeconds(playback.time || 0);
    els.actualReplaySpeed.textContent = `속도 x${Number(playback.speed || 1).toFixed(1)}`;
    els.actualReplayPlay.disabled = false;
    els.actualReplayBack.disabled = false;
    els.actualReplayForward.disabled = false;
    els.actualReplayNote.textContent = payload.live
      ? "실제 리플레이의 현재 골드/아이템 기준으로 추천 중입니다."
      : "리플레이 재생 상태는 연결됐지만 아이템 데이터는 아직 감지되지 않았습니다.";
    return;
  }

  if (payload?.live) {
    els.actualReplayState.className = "badge good";
    els.actualReplayState.textContent = "데이터";
    els.actualReplayTime.textContent = formatSeconds(payload.live.gameData?.gameTime || 0);
    els.actualReplaySpeed.textContent = "제어 없음";
    els.actualReplayPlay.disabled = true;
    els.actualReplayBack.disabled = true;
    els.actualReplayForward.disabled = true;
    els.actualReplayNote.textContent = payload.live.activePlayer?.error
      ? "플레이어/아이템 데이터 기준으로 추천 중입니다. 골드는 좌측 입력값을 사용합니다."
      : "Replay API 제어는 감지되지 않았지만, 실제 플레이어/아이템 데이터 기준으로 추천 중입니다.";
    return;
  }

  els.actualReplayState.className = "badge danger";
  els.actualReplayState.textContent = "미연결";
  els.actualReplayTime.textContent = "--:--";
  els.actualReplaySpeed.textContent = "속도 --";
  els.actualReplayPlay.disabled = true;
  els.actualReplayBack.disabled = true;
  els.actualReplayForward.disabled = true;
  els.actualReplayNote.textContent = state.actualReplayError
    ? "LoL 클라이언트에서 리플레이를 재생한 뒤 새로고침하세요."
    : "LoL 클라이언트에서 리플레이를 재생한 뒤 연결하세요.";
}

async function loadDataDragon() {
  try {
    const response = await fetch("/api/ddragon?locale=ko_KR");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    if (!payload.ok) throw new Error(payload.detail || "Data Dragon error");
    state.ddragon = payload;
    state.itemData = payload.items.data || {};
    state.championData = payload.champions.data || {};
    els.patchLine.textContent = `Data Dragon ${payload.version} / ko_KR`;
    render();
  } catch (error) {
    els.patchLine.textContent = "내장 아이템 데이터 사용 중";
    showToast("Data Dragon 연결 실패. 내장 데이터로 계속합니다.");
  }
}

async function fetchLiveData(showResult) {
  try {
    const response = await fetch("/api/live", { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok || !payload.ok) throw new Error(payload.detail || payload.message || "live unavailable");
    state.liveData = payload.data;
    state.liveError = null;
    syncControlsFromLive(payload.data);
    render();
    if (showResult) showToast("라이브 데이터를 불러왔습니다.");
  } catch (error) {
    state.liveError = error.message;
    state.liveData = null;
    render();
    if (showResult) showToast("라이브 게임을 찾지 못했습니다. 데모 계산을 유지합니다.");
  }
}

async function fetchActualReplay(showResult) {
  try {
    const response = await fetch("/api/replay", { cache: "no-store" });
    const payload = await response.json();
    if (!response.ok || !payload.ok) throw new Error(payload.detail || payload.message || "replay unavailable");
    state.actualReplay = payload;
    state.actualReplayError = null;
    if (payload.live) {
      populateActualReplayTargets(payload.live);
      syncControlsFromLive(payload.live);
    }
    render();
    if (showResult) {
      showToast(payload.live ? "실제 리플레이 데이터와 추천 정보를 연결했습니다." : "리플레이 재생 상태를 연결했습니다.");
    }
  } catch (error) {
    state.actualReplay = null;
    state.actualReplayError = error.message;
    render();
    if (showResult) showToast("실제 리플레이를 찾지 못했습니다.");
  }
}

async function controlActualReplay(body, successMessage) {
  if (!state.actualReplay?.replay) {
    showToast("연결된 실제 리플레이가 없습니다.");
    return;
  }

  try {
    const response = await fetch("/api/replay/playback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const payload = await response.json();
    if (!response.ok || !payload.ok) throw new Error(payload.detail || payload.message || "control failed");
    await fetchActualReplay(false);
    showToast(successMessage);
  } catch (error) {
    showToast("리플레이 제어에 실패했습니다.");
  }
}

function toggleActualReplayPlay() {
  const playback = state.actualReplay?.replay;
  if (!playback) {
    showToast("LoL 리플레이 재생 화면을 먼저 열어주세요.");
    return;
  }
  controlActualReplay({ paused: !playback.paused }, playback.paused ? "리플레이를 재생했습니다." : "리플레이를 정지했습니다.");
}

function seekActualReplay(offsetSeconds) {
  const playback = state.actualReplay?.replay;
  if (!playback) {
    showToast("LoL 리플레이 재생 화면을 먼저 열어주세요.");
    return;
  }
  const currentTime = Number(playback.time || 0);
  const maxTime = Number(playback.length || currentTime + offsetSeconds);
  const nextTime = clamp(currentTime + offsetSeconds, 0, Math.max(currentTime, maxTime));
  controlActualReplay({ time: nextTime }, `${offsetSeconds > 0 ? "+" : ""}${offsetSeconds}초 이동했습니다.`);
}

function syncControlsFromLive(data) {
  const context = state.mode === "replayLive"
    ? parseLiveContext(data, els.actualReplayTarget.value)
    : parseLiveContext(data);
  if (context.championKey && CHAMPION_HINTS[context.championKey]) {
    els.championSelect.value = context.championKey;
  }
  els.archetypeSelect.value = context.archetype;
  els.goldInput.value = context.gold;
}

function populateActualReplayTargets(data) {
  const players = Array.isArray(data.allPlayers) ? data.allPlayers : [];
  const previous = els.actualReplayTarget.value;
  if (!players.length) {
    els.actualReplayTarget.innerHTML = `<option value="">감지된 플레이어 없음</option>`;
    return;
  }

  els.actualReplayTarget.innerHTML = players
    .map((player, index) => {
      const value = playerOptionValue(player, index);
      const label = `${player.team === "ORDER" ? "블루" : "레드"} ${player.position || "-"} / ${player.championName || "?"} / ${player.summonerName || player.riotId || "플레이어"}`;
      return `<option value="${escapeAttribute(value)}">${escapeHtml(label)}</option>`;
    })
    .join("");

  const values = players.map((player, index) => playerOptionValue(player, index));
  els.actualReplayTarget.value = values.includes(previous) ? previous : values[0];
}

function render() {
  const context = getCurrentContext();
  const threat = context.manualThreat || buildThreatProfile(context);
  const recommendations = getRecommendations(context, threat);

  updateStatus(context);
  renderMeters(threat);
  renderOwnedItems(context);
  renderRecommendations(recommendations, context);
  renderAnalysis(context, threat, recommendations);
  renderNextBuys(recommendations, context);
  updateActualReplayControls();
}

function getCurrentContext() {
  if (state.mode === "live" && state.liveData) {
    return parseLiveContext(state.liveData);
  }
  if (state.mode === "replayLive" && state.actualReplay?.live) {
    return parseActualReplayContext(state.actualReplay);
  }
  if (state.mode === "replayLive") {
    return {
      ...parseDemoContext(),
      source: "replayLiveFallback"
    };
  }
  if (state.mode === "replay") {
    return parseReplayContext();
  }
  return parseDemoContext();
}

function parseDemoContext() {
  const championKey = els.championSelect.value || "KaiSa";
  const hint = CHAMPION_HINTS[championKey] || CHAMPION_HINTS.KaiSa;
  const profile = { ...ENEMY_PROFILES[els.enemyProfileSelect.value || "balanced"] };
  if (els.snowballToggle.checked) {
    profile.burst = Math.max(1, profile.burst - 1);
    profile.tank = profile.tank + 1;
  }
  if (els.behindToggle.checked) {
    profile.physical = profile.physical + 1;
    profile.magic = profile.magic + 1;
    profile.burst = profile.burst + 2;
  }

  return {
    source: "demo",
    championKey,
    championName: formatChampionName(championKey),
    archetype: els.archetypeSelect.value || hint.archetype,
    gold: Number(els.goldInput.value || 0),
    ownedIds: [1001, 1037],
    ownedItems: [itemById(1001), itemById(1037)],
    enemies: SAMPLE_LIVE_DATA.allPlayers.filter((player) => player.team === "CHAOS"),
    manualThreat: profile
  };
}

function parseReplayContext() {
  const frame = REPLAY_TIMELINE[state.replayIndex];
  const context = parseLiveContext(frame.data);
  return {
    ...context,
    source: "replay",
    replayLabel: frame.label,
    replayMinute: frame.minute
  };
}

function parseActualReplayContext(payload) {
  const context = parseLiveContext(payload.live, els.actualReplayTarget.value);
  return {
    ...context,
    source: "replayLive",
    replayPlayback: payload.replay,
    replayGame: payload.game,
    replayTime: payload.replay?.time || payload.live?.gameData?.gameTime || 0
  };
}

function parseLiveContext(data, preferredPlayerValue = "") {
  const active = data.activePlayer || {};
  const players = Array.isArray(data.allPlayers) ? data.allPlayers : [];
  const activeName = active.summonerName || active.riotId || active.riotIdGameName || "";
  let player = preferredPlayerValue
    ? players.find((candidate, index) => playerOptionValue(candidate, index) === preferredPlayerValue)
    : null;
  if (!player) player = players.find((candidate) => samePlayer(candidate, activeName));
  if (!player && players.length) player = players[0];

  const championName = player?.championName || active.championName || els.championSelect.value || "KaiSa";
  const championKey = normalizeChampionKey(player?.rawChampionName || championName);
  const hint = CHAMPION_HINTS[championKey] || { archetype: els.archetypeSelect.value || "marksman" };
  const enemies = player
    ? players.filter((candidate) => candidate.team && candidate.team !== player.team)
    : [];
  const ownedItems = Array.isArray(player?.items)
    ? player.items.map((item) => itemById(item.itemID, item.displayName)).filter(Boolean)
    : [];
  const activeGold = Number(active.currentGold);
  const hasActiveGold = Number.isFinite(activeGold);

  return {
    source: "live",
    championKey,
    championName: formatChampionName(championKey),
    archetype: hint.archetype || els.archetypeSelect.value || "marksman",
    gold: Math.max(0, Math.floor(hasActiveGold ? activeGold : Number(els.goldInput.value || 0))),
    goldSource: hasActiveGold ? "live" : "manual",
    ownedIds: ownedItems.map((item) => item.id),
    ownedItems,
    enemies
  };
}

function samePlayer(candidate, activeName) {
  if (!candidate || !activeName) return false;
  const values = [
    candidate.summonerName,
    candidate.riotId,
    candidate.riotIdGameName,
    candidate.rawChampionName
  ].filter(Boolean);
  return values.some((value) => String(value).toLowerCase() === String(activeName).toLowerCase());
}

function playerOptionValue(player, index) {
  return player?.summonerName || player?.riotId || `${player?.team || "TEAM"}:${player?.championName || "Champion"}:${index}`;
}

function buildThreatProfile(context) {
  const profile = { physical: 0, magic: 0, healing: 0, tank: 0, cc: 0, burst: 0 };
  const enemies = context.enemies.length ? context.enemies : SAMPLE_LIVE_DATA.allPlayers.filter((p) => p.team === "CHAOS");

  enemies.forEach((enemy) => {
    const key = normalizeChampionKey(enemy.rawChampionName || enemy.championName);
    const hint = CHAMPION_HINTS[key] || { damage: "mixed", tank: 1, cc: 1, burst: 1 };
    if (hint.damage === "physical") profile.physical += 2.1;
    if (hint.damage === "magic") profile.magic += 2.1;
    if (hint.damage === "mixed") {
      profile.physical += 1.25;
      profile.magic += 1.25;
    }
    profile.healing += hint.heal || 0;
    profile.tank += hint.tank || 0;
    profile.cc += hint.cc || 0;
    profile.burst += hint.burst || 0;

    (enemy.items || []).forEach((item) => addItemThreat(profile, item.itemID));
  });

  Object.keys(profile).forEach((key) => {
    profile[key] = Math.min(10, Math.round(profile[key]));
  });
  return profile;
}

function addItemThreat(profile, itemId) {
  const item = state.itemData[String(itemId)];
  if (!item) return;
  const stats = item.stats || {};
  if (stats.FlatPhysicalDamageMod) profile.physical += Math.min(1.6, stats.FlatPhysicalDamageMod / 45);
  if (stats.FlatMagicDamageMod) profile.magic += Math.min(1.6, stats.FlatMagicDamageMod / 70);
  if (stats.FlatArmorMod) profile.tank += Math.min(1.4, stats.FlatArmorMod / 45);
  if (stats.FlatSpellBlockMod) profile.tank += Math.min(1.2, stats.FlatSpellBlockMod / 45);
  if (stats.FlatHPPoolMod) profile.tank += Math.min(1.2, stats.FlatHPPoolMod / 450);
  if (stats.PercentAttackSpeedMod) profile.physical += 0.8;
}

function getRecommendations(context, threat) {
  const ownedSet = new Set(context.ownedIds);
  const hasBoots = context.ownedIds.some((id) => {
    const candidate = ITEM_CANDIDATES.find((item) => item.id === id);
    const ddragon = state.itemData[String(id)];
    return candidate?.tags.includes("boots") || ddragon?.tags?.includes("Boots");
  });

  return ITEM_CANDIDATES
    .filter((item) => !ownedSet.has(item.id))
    .filter((item) => !(hasBoots && item.tags.includes("boots")))
    .map((item) => scoreCandidate(enrichItem(item), context, threat))
    .filter((result) => result.score > 35)
    .sort((a, b) => b.score - a.score)
    .slice(0, 6);
}

function scoreCandidate(item, context, threat) {
  let score = item.priority || 50;
  const reasons = [];

  if (item.roles.includes(context.archetype)) {
    score += 26;
    reasons.push(`${archetypeLabel(context.archetype)} 핵심 능력치와 맞습니다.`);
  } else if (item.roles.includes("tank") && context.archetype === "support") {
    score += 10;
  } else {
    score -= 18;
  }

  const tags = new Set(item.tags);
  const physicalHeavy = threat.physical >= threat.magic + 2;
  const magicHeavy = threat.magic >= threat.physical + 2;

  if (threat.healing >= 6 && tags.has("antiheal")) {
    score += 34;
    reasons.push("상대 회복/흡혈을 끊는 가치가 큽니다.");
  }
  if (threat.tank >= 7 && (tags.has("antiTank") || tags.has("armorPen") || tags.has("magicPen") || tags.has("armorShred"))) {
    score += 30;
    reasons.push("상대 앞라인이 단단해서 관통/대탱커 옵션이 필요합니다.");
  }
  if (physicalHeavy && (tags.has("armor") || tags.has("antiAuto") || tags.has("antiCrit"))) {
    score += 25;
    reasons.push("AD 압박이 높아 방어력 효율이 좋습니다.");
  }
  if (magicHeavy && (tags.has("magicResist") || tags.has("tenacity") || tags.has("cleanse"))) {
    score += 25;
    reasons.push("AP 압박이 높아 마법 저항/강인함 가치가 올라갑니다.");
  }
  if (threat.cc >= 7 && (tags.has("tenacity") || tags.has("cleanse"))) {
    score += 24;
    reasons.push("군중제어가 많아 CC 대응 옵션이 좋습니다.");
  }
  if (threat.burst >= 7 && (tags.has("antiBurst") || tags.has("stasis") || tags.has("shield"))) {
    score += 22;
    reasons.push("순간 폭딜을 버티는 선택지가 필요합니다.");
  }

  if (context.archetype === "marksman") {
    if (tags.has("crit")) score += 10;
    if (tags.has("attackSpeed")) score += 8;
    if (tags.has("attackDamage")) score += 8;
  }
  if (context.archetype === "mage") {
    if (tags.has("abilityPower")) score += 13;
    if (tags.has("magicPen")) score += threat.tank >= 5 ? 12 : 6;
    if (tags.has("haste")) score += 5;
  }
  if (context.archetype === "fighter") {
    if (tags.has("health")) score += 8;
    if (tags.has("attackDamage")) score += 10;
    if (tags.has("haste")) score += 6;
  }
  if (context.archetype === "tank") {
    if (tags.has("health")) score += 8;
    if (tags.has("armor") || tags.has("magicResist")) score += 10;
  }
  if (context.archetype === "support") {
    if (tags.has("utility") || tags.has("healShield") || tags.has("teamfight")) score += 14;
  }
  if (context.archetype === "assassin") {
    if (tags.has("burst")) score += 10;
    if (tags.has("attackDamage") || tags.has("abilityPower")) score += 8;
  }

  if (els.snowballToggle.checked && (tags.has("burst") || tags.has("scaling") || tags.has("tempo"))) {
    score += 8;
    reasons.push("앞선 상황에서 굴릴 수 있는 화력 선택입니다.");
  }
  if (els.behindToggle.checked && (tags.has("defense") || tags.has("antiBurst"))) {
    score += 12;
    reasons.push("불리한 상황에서 사망 리스크를 줄입니다.");
  }

  const componentValue = getOwnedComponentValue(item, context.ownedIds);
  const remainingCost = Math.max(0, item.cost - componentValue);
  const missingGold = Math.max(0, remainingCost - context.gold);
  if (componentValue > 0) {
    score += 16;
    reasons.push("이미 가진 하위 아이템과 자연스럽게 이어집니다.");
  }
  if (missingGold === 0) {
    score += 14;
    reasons.push("현재 골드로 완성할 수 있습니다.");
  } else if (missingGold <= 500) {
    score += 8;
    reasons.push(`${missingGold}g만 더 모으면 완성 가능합니다.`);
  } else if (remainingCost > 3200 && context.gold < 1200) {
    score -= 8;
  }

  if (!reasons.length) reasons.push("현재 역할과 게임 흐름에서 무난한 선택입니다.");

  return {
    item,
    score: Math.round(score),
    remainingCost,
    missingGold,
    reasons: reasons.slice(0, 4)
  };
}

function getOwnedComponentValue(item, ownedIds) {
  const ownedSet = new Set(ownedIds);
  return (item.components || []).reduce((sum, componentId) => {
    if (!ownedSet.has(componentId)) return sum;
    const component = itemById(componentId);
    return sum + (component?.cost || 0);
  }, 0);
}

function renderStatusBadge(className, text) {
  els.connectionBadge.className = `badge ${className}`;
  els.connectionBadge.textContent = text;
}

function updateStatus(context) {
  els.goldBadge.textContent = `${context.gold}g`;
  if (context.source === "replayLive") {
    renderStatusBadge("good", "실제리플");
    const timeText = formatSeconds(context.replayTime || context.replayPlayback?.time || 0);
    const goldNote = context.goldSource === "manual" ? " / 골드 수동 입력" : "";
    els.contextLine.textContent = `${timeText} 실제 리플레이 / ${context.championName}${goldNote}`;
  } else if (state.mode === "replayLive") {
    renderStatusBadge(state.actualReplay?.replay ? "warn" : "danger", state.actualReplay?.replay ? "리플연결" : "미연결");
    els.contextLine.textContent = state.actualReplay?.replay
      ? "리플레이는 연결됐지만 아이템 데이터가 없어 데모 조건으로 표시"
      : "LoL 클라이언트 리플레이를 찾지 못했습니다";
  } else if (context.source === "replay") {
    renderStatusBadge("warn", "리플레이");
    els.contextLine.textContent = `${formatMinute(context.replayMinute)} ${context.replayLabel} / ${context.championName}`;
  } else if (state.mode === "live" && state.liveData) {
    renderStatusBadge("good", "라이브");
    els.contextLine.textContent = `${context.championName} / ${archetypeLabel(context.archetype)} / 실제 게임 데이터`;
  } else if (state.mode === "live" && state.liveError) {
    renderStatusBadge("danger", "미연결");
    els.contextLine.textContent = "라이브 API 연결 실패, 데모 조건으로 표시";
  } else {
    renderStatusBadge("neutral", "데모");
    els.contextLine.textContent = `${context.championName} / ${archetypeLabel(context.archetype)} / 데모 조건`;
  }
}

function renderMeters(threat) {
  els.physicalMeter.style.width = `${clamp(threat.physical * 10, 0, 100)}%`;
  els.magicMeter.style.width = `${clamp(threat.magic * 10, 0, 100)}%`;
  els.healMeter.style.width = `${clamp(threat.healing * 10, 0, 100)}%`;
  els.tankMeter.style.width = `${clamp(threat.tank * 10, 0, 100)}%`;
}

function renderOwnedItems(context) {
  if (!context.ownedItems.length) {
    els.ownedItems.innerHTML = `<div class="empty-state">보유 아이템 없음</div>`;
    return;
  }

  els.ownedItems.innerHTML = context.ownedItems
    .slice(0, 7)
    .map((item) => `
      <div class="owned-row">
        ${iconHtml(item, "owned-icon")}
        <div>
          <strong>${escapeHtml(item.name)}</strong>
          <span>${item.cost ? `${item.cost}g` : "가격 정보 없음"}</span>
        </div>
        <span>#${item.id}</span>
      </div>
    `)
    .join("");
}

function renderRecommendations(recommendations, context) {
  if (!recommendations.length) {
    els.recommendations.innerHTML = `<div class="empty-state">추천 후보가 부족합니다.</div>`;
    return;
  }

  const visibleRecommendations = state.watchMode ? recommendations.slice(0, 3) : recommendations;
  els.recommendations.innerHTML = visibleRecommendations
    .map((entry, index) => {
      const ready = entry.missingGold === 0;
      const item = entry.item;
      return `
        <article class="item-card ${index === 0 ? "top-pick" : ""}">
          <div class="item-main">
            ${iconHtml(item, "item-icon")}
            <div>
              <div class="item-name">${escapeHtml(item.name)}</div>
              <div class="item-meta">
                <span class="mini-badge">${item.cost}g</span>
                <span class="mini-badge ${ready ? "ready" : "wait"}">${ready ? "구매 가능" : `${entry.missingGold}g 부족`}</span>
              </div>
            </div>
          </div>
          <ul class="reason-list">
            ${entry.reasons.map((reason) => `<li>${escapeHtml(reason)}</li>`).join("")}
          </ul>
          <div class="score-line">
            <span>추천 점수</span>
            <strong>${entry.score}</strong>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderAnalysis(context, threat, recommendations) {
  const notes = [];
  const top = recommendations[0];
  if (threat.healing >= 6) notes.push("상대 회복 수치가 높습니다. 치유 감소 아이템을 늦추지 않는 편이 좋습니다.");
  if (threat.physical >= threat.magic + 2) notes.push("상대 피해가 AD 쪽으로 기울었습니다. 방어력/평타 대응 아이템 가치가 상승합니다.");
  if (threat.magic >= threat.physical + 2) notes.push("상대 피해가 AP 쪽으로 기울었습니다. 마법 저항 또는 주문 방어 옵션을 고려하세요.");
  if (threat.tank >= 7) notes.push("앞라인이 단단합니다. 관통, 지속 피해, 방어력 감소 효과가 좋은 타이밍입니다.");
  if (threat.cc >= 7) notes.push("CC가 많은 조합입니다. 강인함이나 정화형 유틸리티가 싸움 시간을 늘려줍니다.");
  if (top) notes.push(`현재 1순위는 ${top.item.name}입니다. ${top.reasons[0]}`);
  if (!notes.length) notes.push("큰 위협이 한쪽으로 쏠리지 않았습니다. 역할 핵심 아이템을 빠르게 완성하는 흐름이 좋습니다.");

  els.analysisList.innerHTML = notes.slice(0, 5).map((note) => `<li>${escapeHtml(note)}</li>`).join("");
}

function renderNextBuys(recommendations, context) {
  const rows = [];
  recommendations.slice(0, 4).forEach((entry) => {
    const component = nextComponentFor(entry.item, context.ownedIds, context.gold);
    if (component) {
      rows.push({ item: component, note: `${entry.item.name} 하위템`, cost: component.cost });
    } else {
      rows.push({ item: entry.item, note: entry.missingGold === 0 ? "완성 가능" : `${entry.missingGold}g 더 필요`, cost: entry.item.cost });
    }
  });

  if (!rows.length) {
    els.nextBuys.innerHTML = `<div class="empty-state">다음 구매 후보 없음</div>`;
    return;
  }

  els.nextBuys.innerHTML = rows.map((row) => `
    <div class="buy-row">
      ${iconHtml(row.item, "buy-icon")}
      <div>
        <strong>${escapeHtml(row.item.name)}</strong>
        <span>${escapeHtml(row.note)}</span>
      </div>
      <span>${row.cost}g</span>
    </div>
  `).join("");
}

function nextComponentFor(item, ownedIds, gold) {
  const ownedSet = new Set(ownedIds);
  const options = (item.components || [])
    .filter((id) => !ownedSet.has(id))
    .map((id) => itemById(id))
    .filter(Boolean)
    .sort((a, b) => {
      const aReady = a.cost <= gold ? 1 : 0;
      const bReady = b.cost <= gold ? 1 : 0;
      return bReady - aReady || b.cost - a.cost;
    });
  return options[0] || null;
}

function enrichItem(item) {
  const ddragon = state.itemData[String(item.id)];
  if (!ddragon) return { ...item };
  return {
    ...item,
    name: ddragon.name || item.name,
    cost: ddragon.gold?.total || item.cost,
    image: imageUrl(ddragon.image?.full),
    description: ddragon.plaintext || ""
  };
}

function itemById(id, fallbackName) {
  const candidate = ITEM_CANDIDATES.find((item) => item.id === Number(id)) || COMPONENTS[Number(id)];
  const ddragon = state.itemData[String(id)];
  if (candidate) {
    return enrichItem({ tags: [], roles: [], components: [], priority: 0, ...candidate });
  }
  if (ddragon) {
    return {
      id: Number(id),
      name: ddragon.name || fallbackName || `아이템 ${id}`,
      cost: ddragon.gold?.total || 0,
      image: imageUrl(ddragon.image?.full),
      tags: ddragon.tags || [],
      roles: [],
      components: []
    };
  }
  if (!id) return null;
  return {
    id: Number(id),
    name: fallbackName || `아이템 ${id}`,
    cost: 0,
    tags: [],
    roles: [],
    components: []
  };
}

function imageUrl(imageName) {
  if (!imageName || !state.ddragon?.version) return "";
  return `https://ddragon.leagueoflegends.com/cdn/${state.ddragon.version}/img/item/${imageName}`;
}

function iconHtml(item, className) {
  if (item.image) {
    return `<span class="${className}"><img src="${escapeAttribute(item.image)}" alt=""></span>`;
  }
  const letters = item.name.replace(/[^A-Za-z가-힣0-9]/g, "").slice(0, 2) || "IT";
  return `<span class="${className}" aria-hidden="true">${escapeHtml(letters)}</span>`;
}

function normalizeChampionKey(name) {
  const cleaned = String(name || "")
    .replace(/^game_character_displayname_/i, "")
    .replace(/^game_character_skin_displayname_/i, "");
  const raw = cleaned.replace(/[^A-Za-z]/g, "");
  const special = {
    Chogath: "Chogath",
    DrMundo: "DrMundo",
    JarvanIV: "JarvanIV",
    Kaisa: "KaiSa",
    Khazix: "KhaZix",
    KSante: "KSante",
    LeeSin: "LeeSin",
    MasterYi: "MasterYi",
    MissFortune: "MissFortune",
    MonkeyKing: "Wukong",
    NunuWillump: "Nunu",
    Reksai: "RekSai",
    TahmKench: "TahmKench",
    TwistedFate: "TwistedFate",
    Velkoz: "Velkoz",
    XinZhao: "XinZhao"
  };
  if (CHAMPION_HINTS[raw]) return raw;
  if (special[raw]) return special[raw];
  const found = Object.keys(CHAMPION_HINTS).find((key) => key.toLowerCase() === raw.toLowerCase());
  return found || raw || "KaiSa";
}

function formatChampionName(key) {
  const ddragon = state.championData[key];
  if (ddragon?.name) return ddragon.name;
  return String(key)
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace("Kai Sa", "Kai'Sa")
    .replace("Kha Zix", "Kha'Zix");
}

function archetypeLabel(value) {
  return {
    marksman: "원거리 딜러",
    mage: "마법사",
    assassin: "암살자",
    fighter: "브루저",
    tank: "탱커",
    support: "서포터"
  }[value] || value;
}

function formatMinute(minute) {
  const safeMinute = Math.max(0, Number(minute) || 0);
  const whole = Math.floor(safeMinute);
  const seconds = Math.round((safeMinute - whole) * 60);
  return `${String(whole).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function formatSeconds(totalSeconds) {
  const safeSeconds = Math.max(0, Math.floor(Number(totalSeconds) || 0));
  const minutes = Math.floor(safeSeconds / 60);
  const seconds = safeSeconds % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function showToast(message) {
  els.toast.textContent = message;
  els.toast.classList.add("show");
  window.clearTimeout(state.toastTimer);
  state.toastTimer = window.setTimeout(() => els.toast.classList.remove("show"), 2400);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}
