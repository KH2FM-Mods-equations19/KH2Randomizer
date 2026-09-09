import random
from Class.openkhmod import AttackEntriesOrganizer, ATKPObject

WEAK_MAX_DIFFERENCE = 0.3
WEAK_MIN_DIFFERENCE = 0.0
MILD_MAX_DIFFERENCE = 0.5
MILD_MIN_DIFFERENCE = 0.0
MEDIUM_MAX_DIFFERENCE = 0.8
MEDIUM_MIN_DIFFERENCE = 0.2
STRONG_MAX_DIFFERENCE = 1.2
STRONG_MIN_DIFFERENCE = 0.5
HEAVY_MAX_DIFFERENCE = 2.0
HEAVY_MIN_DIFFERENCE = 0.8
OVERPOWERED_MAX_DIFFERENCE = 3.0
OVERPOWERED_MIN_DIFFERENCE = 1.2
NIGHTMARE_MAX_DIFFERENCE = 5.0
NIGHTMARE_MIN_DIFFERENCE = 2.4
CHAOS_MAX_DIFFERENCE = 8.0
CHAOS_MIN_DIFFERENCE = 0.0

LIST_OF_COMPANION_IDS = [
	1698,
	151,
	152,
	155,
	1698,
	151,
	152,
	155,
	153,
	154,
	1163,
	1164,
	1165,
	1525,
	139,
	146,
	156,
	157,
	158,
	159,
	1160,
	1188,
	1161,
	1162,
	224,
	895,
	225,
	563,
	564,
	565,
	273,
	274,
	1176,
	1177,
	1178,
	861,
	941,
	862,
	863,
	864,
	864,
	1179,
	1180,
	1526,
	214,
	215,
	216,
	217,
	218,
	1174,
	1175,
	1193,
	365,
	366,
	367,
	368,
	369,
	371,
	384,
	387,
	385,
	372,
	373,
	1169,
	622,
	219,
	220,
	223,
	221,
	222,
	1166,
	570,
	575,
	361,
	1527,
	1528,
	1529,
	627,
	1181,
	494,
	495,
	646,
	647,
	648,
	515,
	649,
	1171,
	1172,
	1173,
	1494,
	1495,
	1496,
	1497,
	1498,
	1499,
	1500,
	1501,
	1502,
	1503,
	1504,
	1505,
	1506,
	1507,
	1508,
	1509,
	1510,
	1511,
	1512,
	1513,
	1514,
	1515,
	1516,
	1531,
	1532,
	193,
	194,
	195,
	196,
	1272,
	1576,
	153,
	154,
	1716,
	1717,
	1718,
	1165,
	1643,
	1942,
	85,
	86,
	87,
	95,
	1253,
	1258,
	1188,
	1292,
	1293,
	1294,
	1295,
	1296,
	1297,
	1315,
	1006,
	1183,
	1644,
	1689,
	1265,
	988,
	996,
	999,
	1555,
	1579,
	1477,
	1478,
	1373,
	1628,
	1629,
	1631,
	1135,
	1574,
	1225,
	860,
	1573,
	855,
	1227,
	1733,
	1261,
	1441,
	1444,
	1445,
	883,
	1210,
]
KNOCBACK_LIST = [8, 9, 10, 11, 12, 17, 18]

ALL_DAMAGE_PRESETS = {
	"DISABLED": [],
	"WEAK": [WEAK_MAX_DIFFERENCE, WEAK_MIN_DIFFERENCE],
	"MILD": [MILD_MAX_DIFFERENCE, MILD_MIN_DIFFERENCE],
	"MEDIUM": [MEDIUM_MAX_DIFFERENCE, MEDIUM_MIN_DIFFERENCE],
	"STRONG": [STRONG_MAX_DIFFERENCE, STRONG_MIN_DIFFERENCE],
	"HEAVY": [HEAVY_MAX_DIFFERENCE, HEAVY_MIN_DIFFERENCE],
	"OVERPOWERED": [OVERPOWERED_MAX_DIFFERENCE, OVERPOWERED_MIN_DIFFERENCE],
	"NIGHTMARE": [NIGHTMARE_MAX_DIFFERENCE, NIGHTMARE_MIN_DIFFERENCE],
	"CHAOS": [CHAOS_MAX_DIFFERENCE, CHAOS_MIN_DIFFERENCE],
}
ALL_KNOCKBACK_AMOUNT_PRESETS = {
	"DISABLED": [],
	"WEAK": [WEAK_MAX_DIFFERENCE, WEAK_MIN_DIFFERENCE],
	"MILD": [MILD_MAX_DIFFERENCE, MILD_MIN_DIFFERENCE],
	"MEDIUM": [MEDIUM_MAX_DIFFERENCE, MEDIUM_MIN_DIFFERENCE],
	"STRONG": [STRONG_MAX_DIFFERENCE, STRONG_MIN_DIFFERENCE],
	"HEAVY": [HEAVY_MAX_DIFFERENCE, HEAVY_MIN_DIFFERENCE],
	"OVERPOWERED": [OVERPOWERED_MAX_DIFFERENCE, OVERPOWERED_MIN_DIFFERENCE],
	"NIGHTMARE": [NIGHTMARE_MAX_DIFFERENCE, NIGHTMARE_MIN_DIFFERENCE],
	"CHAOS": [CHAOS_MAX_DIFFERENCE, CHAOS_MIN_DIFFERENCE],
}
ALL_REVENGE_VALUE_PRESETS = {
	"DISABLED": [],
	"WEAK": [1, 0],
	"MILD": [2, 0],
	"MEDIUM": [2, 1],
	"STRONG": [3, 1],
	"HEAVY": [4, 2],
	"OVERPOWERED": [8, 3],
	"NIGHTMARE": [11, 5],
	"CHAOS": [24, 0],
}
ALL_MULTI_HIT_PRESETS = {
	"DISABLED": [],
	"WEAK": [5, 8, 16],
	"MILD": [8, 8, 16],
	"MEDIUM": [12, 6, 14],
	"STRONG": [25, 6, 12],
	"HEAVY": [35, 5, 9],
	"OVERPOWERED": [40, 4, 8],
	"NIGHTMARE": [60, 2, 8],
	"CHAOS": [90, 1, 36],
}
ALL_HPDRAIN_PRESETS = {
	"DISABLED": [],
	"WEAK": [10, 1, 2],
	"MILD": [16, 1, 3],
	"MEDIUM": [24, 1, 6],
	"STRONG": [30, 3, 9],
	"HEAVY": [40, 4, 12],
	"OVERPOWERED": [50, 7, 18],
	"NIGHTMARE": [80, 10, 26],
	"CHAOS": [100, 1, 40],
}
ALL_DRIVEGAIN_PRESETS = {
	"DISABLED": [],
	"WEAK": [WEAK_MAX_DIFFERENCE, WEAK_MIN_DIFFERENCE],
	"MILD": [MILD_MAX_DIFFERENCE, MILD_MIN_DIFFERENCE],
	"MEDIUM": [MEDIUM_MAX_DIFFERENCE, MEDIUM_MIN_DIFFERENCE],
	"STRONG": [STRONG_MAX_DIFFERENCE, STRONG_MIN_DIFFERENCE],
	"HEAVY": [HEAVY_MAX_DIFFERENCE, HEAVY_MIN_DIFFERENCE],
	"OVERPOWERED": [OVERPOWERED_MAX_DIFFERENCE, OVERPOWERED_MIN_DIFFERENCE],
	"NIGHTMARE": [NIGHTMARE_MAX_DIFFERENCE, NIGHTMARE_MIN_DIFFERENCE],
	"CHAOS": [CHAOS_MAX_DIFFERENCE, CHAOS_MIN_DIFFERENCE],
}

#Randomizing element in all IDs can be painful against certain enemies like gargoyles.
#These IDs can be excluded from having element randomized if enabled.
SORA_BASE_ATTACK_IDS = [
	126,
	127,
	128,
	147,
	131,
	132,
	129,
	130,
	133,
	134,
	926,
	935,
	937,
	936,
	944,
	945,
	962,
	947,
	946,
	949,
	948,
	950,
	951,
	952,
	953,
	954,
	955,
	957,
	956,
	958,
	959,
	961,
	960,
	589,
	590,
	591,
	1003,
	1004,
	1052,
	1431,
	1937,
	1938,
	1959,
	1963,
	1964,
	1698,
	699,
	701,
	888,
	889,
	1586,
	1587,
	716,
	740,
	741,
	1590,
	893,
	713,
	714,
	1585,
	886,
	715,
]

#Workaround for weird bug that doesn't let sora kill bosses for some reason
SORA_IDS = [
	126,
	127,
	128,
	147,
	131,
	132,
	129,
	130,
	133,
	134,
	926,
	170,
	406,
	854,
	876,
	911,
	912,
	915,
	916,
	917,
	927,
	963,
	967,
	1007,
	1898,
	1899,
	1131,
	1581,
	1582,
	1583,
	1869,
	1882,
	1896,
	1897,
	1900,
	1901,
	1903,
	171,
	172,
	175,
	176,
	177,
	178,
	179,
	180,
	187,
	189,
	190,
	191,
	192,
	526,
	527,
	197,
	198,
	199,
	200,
	201,
	202,
	203,
	204,
	237,
	238,
	528,
	529,
	227,
	228,
	1857,
	1858,
	1859,
	1860,
	1861,
	1862,
	1866,
	1867,
	1870,
	1871,
	1872,
	1877,
	1878,
	1879,
	1883,
	1884,
	1885,
	1886,
	1887,
	1888,
	1889,
	1890,
	1891,
	1892,
	1893,
	1894,
	1895,
	249,
	250,
	251,
	574,
	576,
	578,
	667,
	668,
	669,
	248,
	502,
	859,
	658,
	976,
	1059,
	1060,
	1366,
	1061,
	1063,
	1062,
	1076,
	1077,
	1100,
	1101,
	1257,
	1252,
	1368,
	1254,
	1369,
	1255,
	1370,
	1356,
	1256,
	1065,
	1066,
	1096,
	1097,
	1098,
	1078,
	1078,
	1099,
	1274,
	1273,
	1286,
	1287,
	1276,
	1275,
	1277,
	1278,
	1281,
	1282,
	1285,
	1284,
	1450,
	1449,
	1388,
	1389,
	1455,
	1390,
	1391,
	1392,
	1393,
	1394,
	1396,
	1395,
	1398,
	1397,
	1399,
	1400,
	1404,
	1403,
	1422,
	1423,
	1424,
	1425,
	1426,
	1427,
	1412,
	1413,
	1405,
	1406,
	1407,
	1408,
	1409,
	1410,
	1411,
	1401,
	1402,
	1456,
	1457,
	1458,
	1737,
	1414,
	1415,
	1416,
	1417,
	1418,
	1419,
	1420,
	1421,
	1428,
	1429,
	1607,
	1608,
	30,
	31,
	457,
	531,
	459,
	532,
	533,
	456,
	475,
	476,
	530,
	458,
	534,
	460,
	542,
	543,
	544,
	474,
	538,
	477,
	478,
	549,
	550,
	551,
	552,
	545,
	479,
	480,
	546,
	547,
	548,
	553,
	554,
	555,
	556,
	699,
	701,
	888,
	889,
	1586,
	1587,
	716,
	740,
	741,
	1590,
	893,
	713,
	714,
	1585,
	886,
	715,
	935,
	937,
	936,
	944,
	945,
	962,
	947,
	946,
	949,
	948,
	950,
	951,
	952,
	953,
	954,
	955,
	957,
	956,
	958,
	959,
	961,
	960,
	125,
	589,
	590,
	591,
	1003,
	1004,
	1052,
	1431,
	1937,
	1938,
	1959,
	1963,
	1964,
	1698,
	1086,
]
LIMITFORM_LIMIT_IDS = [
	1857,
	1858,
	1859,
	1860,
	1861,
	1862,
	1866,
	1867,
	1878,
	1879,
	1883,
	1884,
	1885,
	1886,
	1887,
	1888,
	1889,
	1890,
	1891,
	1892,
	1893,
	1894,
	1895,
]
NON_DRIVE_SORA_IDS = [
	926,
	126,
	127,
	128,
	147,
	131,
	132,
	890,
	909,
	968,
	975,
	129,
	130,
	133,
	134,
	170,
	406,
	854,
	876,
	911,
	912,
	915,
	916,
	917,
	927,
	963,
	967,
	1007,
	1898,
	1899,
	1131,
	1581,
	1582,
	1583,
	1869,
	1882,
	1896,
	1897,
	1900,
	1901,
	1903,
]
NON_DRIVE_SORA_MAGIC_SUBIDS = [
	0,
	1,
	2,
	256,
	258,
	512,
	513,
	514,
	515,
	768,
	769,
	770,
	771,
	1024,
	1025,
	1280,
	1284,
]
SORA_MAGIC_IDS = [
	249,
	250,
	251,
	574,
	576,
	578,
	667,
	668,
	669,
	248,
	502,
	658,
]
class atkpRandomizerClass:
	def __init__(self, kill_boss, companion_damage):
		self.companion_kill_boss = kill_boss
		self.companion_deal_damage = companion_damage
		self.DAMAGE_PRESETS = []
		self.KNOCKBACK_AMOUNT_PRESETS = []
		self.REVENGE_VALUE_PRESETS = []
		self.MULTI_HIT_PRESETS = []
		self.HPDRAIN_PRESETS = []
		self.DRIVEGAIN_PRESETS = []
	
	def randomize_atkp_data(self, list_data, atkp_organizer: AttackEntriesOrganizer, damage_preset: str, element, revenge_value_preset, multi_hit_preset, knockback_amount_preset, exclude_base_attack, HpDrain_preset, drivegain_preset):
		attack_entries = []
		final_attack_entries = []
		self.DAMAGE_PRESETS = ALL_DAMAGE_PRESETS[damage_preset]
		self.KNOCKBACK_AMOUNT_PRESETS = ALL_KNOCKBACK_AMOUNT_PRESETS[knockback_amount_preset]
		self.REVENGE_VALUE_PRESETS = ALL_REVENGE_VALUE_PRESETS[revenge_value_preset]
		self.MULTI_HIT_PRESETS = ALL_MULTI_HIT_PRESETS[multi_hit_preset]
		self.HPDRAIN_PRESETS = ALL_HPDRAIN_PRESETS[HpDrain_preset]
		self.DRIVEGAIN_PRESETS = ALL_DRIVEGAIN_PRESETS[drivegain_preset]

		for attack_entry in list_data:
			attack_entries.append(atkp_organizer.attack_entry_constructor(attack_entry))
		for attack_entry in attack_entries:
			attack_entry: ATKPObject
			#Exclude Guard so it still works like normal
			if attack_entry.Id == 161:
				continue
			#Workaround
			if SORA_IDS.__contains__(attack_entry.Id):
				attack_entry.Flags = "KillBoss"
			if len(self.DRIVEGAIN_PRESETS) != 0:
				if NON_DRIVE_SORA_IDS.__contains__(attack_entry.Id):
					attack_entry.DriveDrain = min(max(int(round(self.randomize_value(attack_entry.DriveDrain, self.DRIVEGAIN_PRESETS[0], self.DRIVEGAIN_PRESETS[1]))), 0), 254)
				if SORA_MAGIC_IDS.__contains__(attack_entry.Id) and NON_DRIVE_SORA_MAGIC_SUBIDS.__contains__(attack_entry.Id):
					attack_entry.DriveDrain = min(max(int(round(self.randomize_value(attack_entry.DriveDrain, self.DRIVEGAIN_PRESETS[0], self.DRIVEGAIN_PRESETS[1]))), 0), 254)
			
			#Fix limit form limits not healing
			if LIMITFORM_LIMIT_IDS.__contains__(attack_entry.Id):
				attack_entry.HpDrain = random.randint(2, 15)
			if len(self.DAMAGE_PRESETS) != 0:
				attack_entry.Power = max(min(int(round(self.randomize_value(attack_entry.Power, self.DAMAGE_PRESETS[0], self.DAMAGE_PRESETS[1]))), 65535), 0)
			if element:
				if exclude_base_attack:
					if not SORA_BASE_ATTACK_IDS.__contains__(attack_entry.Id):
						attack_entry.Element = self.randomize_elements()
				else: 
					attack_entry.Element = self.randomize_elements()
			if self.companion_deal_damage:
				if LIST_OF_COMPANION_IDS.__contains__(attack_entry.Id):
					attack_entry.EnemyReaction = self.randomize_companion_knockback_type()
			if self.companion_kill_boss != 0:
				if LIST_OF_COMPANION_IDS.__contains__(attack_entry.Id):
					attack_entry.Flags = self.companion_kill_boss
			if len(self.KNOCKBACK_AMOUNT_PRESETS) != 0:
				attack_entry.KnockbackStrength1 = max(min(int(round(self.randomize_value(attack_entry.KnockbackStrength1, self.KNOCKBACK_AMOUNT_PRESETS[0], self.KNOCKBACK_AMOUNT_PRESETS[1]))), 32767), -32767)
				attack_entry.KnockbackStrength2 = max(min(int(round(self.randomize_value(attack_entry.KnockbackStrength2, self.KNOCKBACK_AMOUNT_PRESETS[0], self.KNOCKBACK_AMOUNT_PRESETS[1]))), 32767), -32767)
			if len(self.REVENGE_VALUE_PRESETS) != 0:
				attack_entry.RevengeDamage = min(max(attack_entry.RevengeDamage + (self.randomize_revenge_value(self.REVENGE_VALUE_PRESETS[0], self.REVENGE_VALUE_PRESETS[1])), 0), 255)
			if len(self.MULTI_HIT_PRESETS) != 0:
				attack_entry.Interval = max(self.randomize_multi_hit(self.MULTI_HIT_PRESETS[0], self.MULTI_HIT_PRESETS[1], self.MULTI_HIT_PRESETS[2]), 0)
			if len(self.HPDRAIN_PRESETS) != 0:
				attack_entry.HpDrain = min(max(int(round(attack_entry.HpDrain + self.randomize_hpdrain(self.HPDRAIN_PRESETS[0], self.HPDRAIN_PRESETS[1], self.HPDRAIN_PRESETS[2]))), 0), 254)
			
			attack_entry.validate()
			final_attack_entries.append(attack_entry)
		
		return final_attack_entries

	def randomize_value(self, value, max_difference, min_difference):
		if value == 0:
			return 0
		increase_value = self.positive_or_negative()
		if increase_value:
			multiplier = 1.0 + random.uniform(min_difference, max_difference)
			return value * multiplier
		else:
			divisor = 1.0 + random.uniform(min_difference, max_difference)
			return value / divisor
	
	def randomize_elements(self):
		return random.randint(0, 5)
	
	def randomize_on_hit(self):
		return random.randint(0, 12)
	
	def randomize_companion_knockback_type(self):
		index = random.randint(0, 2)
		return KNOCBACK_LIST[index]

	def randomize_multi_hit(self, chance, minFrames, maxFrames):
		if random.randint(1, 100) > chance:
			return -1
		return random.randint(minFrames, maxFrames)
	
	# Because a lot of moves have either 0 revenge value or a high amount, randomization
	# is handled by first determining if any change will happen, then by a flat value.
	# This is to avoid 0 values being multiplied uselessly or moves with revenge value
	# to get ridiculously high. Generally, revenge value is not randomized at high
	# differences because the game would be kind of unplayable. (unless Chaos enabled)
	def randomize_revenge_value(self, maxValue, minValue):
		increase_value = self.positive_or_negative()
		num = random.randint(minValue, maxValue)
		if not increase_value:
			return -num
		return num

	def randomize_hpdrain(self, chance, minValue, maxValue):
		increase_value = self.positive_or_negative()
		if random.randint(1, 100) > chance:
			return 0
		if not increase_value:
			return -random.randint(minValue, maxValue)
		else: return random.randint(minValue, maxValue)

	def positive_or_negative(self):
		if random.randint(1, 100) > 50: return True
		return False
	