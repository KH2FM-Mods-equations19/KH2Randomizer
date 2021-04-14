from dataclasses import dataclass, field
import random, zipfile, yaml, io

from Class.locationClass import KH2Location, KH2ItemStat, KH2LevelUp, KH2FormLevel, KH2Bonus, KH2Treasure, KH2StartingItem, KH2ItemStat
from Class.itemClass import KH2Item
from Class.modYml import modYml

from List.configDict import locationType, itemType
from List.experienceValues import soraExp, formExp
from List.LvupStats import Stats
from List.LocationList import Locations
from List.ItemList import Items
from List.hashTextEntries import hashTextEntries

def noop(self, *args, **kw):
    pass


@dataclass
class KH2Randomizer():
    seedName: str
    _validLocationList: list[KH2Location] = field(default_factory=list)
    _allLocationList: list[KH2Location] = field(default_factory=list)
    _validItemList: list[KH2Item] = field(default_factory=list)

    _validLocationListGoofy: list[KH2Location] = field(default_factory=list)
    _allLocationListGoofy: list[KH2Location] = field(default_factory=list)
    _validItemListGoofy: list[KH2Item] = field(default_factory=list)

    _validLocationListDonald: list[KH2Location] = field(default_factory=list)
    _allLocationListDonald: list[KH2Location] = field(default_factory=list)
    _validItemListDonald: list[KH2Item] = field(default_factory=list)

    def __post_init__(self):
        random.seed(self.seedName)
    

    def populateLocations(self, excludeWorlds):
        self._allLocationList = Locations.getTreasureList() + Locations.getSoraLevelList() + Locations.getSoraBonusList() + Locations.getFormLevelList() + Locations.getSoraWeaponList() + Locations.getSoraStartingItemList()

        self._validLocationList = [location for location in self._allLocationList if not set(location.LocationTypes).intersection(excludeWorlds)]

        self._allLocationListGoofy = Locations.getGoofyWeaponList() + Locations.getGoofyStartingItemList() + Locations.getGoofyBonusList()

        self._validLocationListGoofy = [location for location in self._allLocationListGoofy if not set(location.LocationTypes).intersection(excludeWorlds)]

        self._allLocationListDonald = Locations.getDonaldWeaponList() + Locations.getDonaldStartingItemList() + Locations.getDonaldBonusList()

        self._validLocationListDonald = [location for location in self._allLocationListDonald if not set(location.LocationTypes).intersection(excludeWorlds)]

    def populateItems(self, promiseCharm = False):
        self._validItemList = Items.getItemList() + Items.getSupportAbilityList() + Items.getActionAbilityList()
        self._validItemListGoofy = Items.getGoofyAbilityList()
        self._validItemListDonald = Items.getDonaldAbilityList()

        if promiseCharm:
            self._validItemList.append(KH2Item(524, "Promise Charm",itemType.PROMISE_CHARM))

    def validateCount(self):
        return len(self._validItemList) < len(self._validLocationList)

    def goMode(self):
        locations = [location for location in self._validLocationList if set(location.LocationTypes).intersection([locationType.Free])]
        print(locations)
        proofs = [item for item in self._validItemList if item.ItemType in [itemType.PROOF, itemType.PROOF_OF_CONNECTION, itemType.PROOF_OF_PEACE]]
        print(proofs)
        for index, location in enumerate(locations):
            location.setReward(proofs[index].Id)
            self._validLocationList.remove(location)
            location.InvalidChecks.append(itemType.JUNK)
            self._validItemList.remove(proofs[index])


    def setKeybladeAbilities(self, keybladeAbilities = ["Support"], keybladeMinStat = 0, keybladeMaxStat = 7):
        keybladeList = [location for location in self._validLocationList if isinstance(location, KH2ItemStat)]
        abilityList = [item for item in self._validItemList if (item.ItemType == itemType.SUPPORT_ABILITY and "Support" in keybladeAbilities) or (item.ItemType == itemType.ACTION_ABILITY and "Action" in keybladeAbilities)]

        for keyblade in keybladeList:
            randomAbility = random.choice(abilityList)
            keyblade.setReward(randomAbility.Id)
            keyblade.setStats(keybladeMinStat, keybladeMaxStat)
            abilityList.remove(randomAbility)
            self._validItemList.remove(randomAbility)

        shieldList = [location for location in self._validLocationListGoofy if isinstance(location, KH2ItemStat)]
        for shield in shieldList:
            random.shuffle(self._validItemListGoofy)
            shield.setReward(self._validItemListGoofy.pop().Id)

        staffList = [location for location in self._validLocationListDonald if isinstance(location, KH2ItemStat)]
        for staff in staffList:
            random.shuffle(self._validItemListDonald)
            staff.setReward(self._validItemListDonald.pop().Id)

    def setRewards(self, levelChoice="ExcludeFrom50"):
        locations = [location for location in self._validLocationList if not isinstance(location, KH2ItemStat)]
        for item in self._validItemList:
            while True:
                randomLocation = random.choice(locations)
                if not item.ItemType in randomLocation.InvalidChecks:
                    randomLocation.setReward(item.Id)
                    locations.remove(randomLocation)
                    break
        
        junkLocations = locations + [location for location in self._allLocationList if (not location in self._validLocationList and not set(location.LocationTypes).intersection([levelChoice]) and not set(location.InvalidChecks).intersection([itemType.JUNK]))]


        for location in junkLocations:
            location.setReward(random.choice(Items.getJunkList()).Id)

        goofyLocations = [location for location in self._validLocationListGoofy if not isinstance(location, KH2ItemStat)]
        for item in self._validItemListGoofy:
            randomLocation = random.choice(goofyLocations)
            randomLocation.setReward(item.Id)
            if not randomLocation.DoubleReward:
                self._validLocationListGoofy.remove(randomLocation)
                goofyLocations.remove(randomLocation)
                continue
            if not randomLocation.BonusItem2 == 0:
                self._validLocationListGoofy.remove(randomLocation)
                goofyLocations.remove(randomLocation)
                continue

        donaldLocations = [location for location in self._validLocationListDonald if not isinstance(location, KH2ItemStat)]
        for item in self._validItemListDonald:
            randomLocation = random.choice(donaldLocations)
            randomLocation.setReward(item.Id)
            if not randomLocation.DoubleReward:
                self._validLocationListDonald.remove(randomLocation)
                donaldLocations.remove(randomLocation)
                continue
            if not randomLocation.BonusItem2 == 0:
                self._validLocationListDonald.remove(randomLocation)
                donaldLocations.remove(randomLocation)
                continue            
            

    def setLevels(self, soraExpMult, formExpMult):
        statsList = Stats.getLevelStats()
        apList = Stats.getAp()
        soraLevels = [location for location in self._allLocationList if isinstance(location, KH2LevelUp)]
        for index, level in enumerate(soraLevels):
            level.Exp = round(soraExp[level.Level] / soraExpMult)
            if level.Level > 1:
                random.shuffle(statsList)
                level.setStat(soraLevels[index-1], statsList.pop())
                if level.getReward() == 0:
                    random.shuffle(apList)
                    level.setAp(soraLevels[index-1], apList.pop())



        formLevels = [location for location in self._allLocationList if isinstance(location, KH2FormLevel)]
        for level in formLevels:
            level.Exp = round(formExp[level.FormId][level.FormLevel] / float(formExpMult[str(level.FormId)]))

    def setBonusStats(self):
        statsList = Stats.getBonusStats()
        locations = [location for location in self._allLocationList if isinstance(location, KH2Bonus) and location.HasStat]
        for location in locations:
            random.shuffle(statsList)
            location.setStat(statsList.pop())

    def generateZip(self, enemyOptions={"boss":"Disabled"}):
        trsrList = [location for location in self._allLocationList if isinstance(location, KH2Treasure)]
        lvupList = [location for location in self._allLocationList if isinstance(location, KH2LevelUp)]
        bonsList = [location for location in self._allLocationList if isinstance(location, KH2Bonus)] + [location for location in self._allLocationListDonald if isinstance(location, KH2Bonus)] + [location for location in self._allLocationListGoofy if isinstance(location, KH2Bonus)]
        fmlvList = [location for location in self._allLocationList if isinstance(location, KH2FormLevel)]
        itemList = [location for location in self._allLocationList if isinstance(location, KH2ItemStat)] + [location for location in self._allLocationListDonald if isinstance(location, KH2ItemStat)] + [location for location in self._allLocationListGoofy if isinstance(location, KH2ItemStat)]
        plrpList = []
        [plrpList.append(location) for location in self._allLocationList if isinstance(location, KH2StartingItem) and not location in plrpList]
        [plrpList.append(location) for location in self._allLocationListDonald if isinstance(location, KH2StartingItem) and not location in plrpList]
        [plrpList.append(location) for location in self._allLocationListGoofy if isinstance(location, KH2StartingItem) and not location in plrpList]

        mod = modYml.getDefaultMod()

        formattedTrsr = {}
        for trsr in trsrList:
            formattedTrsr[trsr.Id] = {'ItemId':trsr.ItemId}

        formattedLvup = {}
        for lvup in lvupList:
            if not lvup.Character in formattedLvup.keys():
                formattedLvup[lvup.Character] = {}
            formattedLvup[lvup.Character][lvup.Level] = {
                "Exp": lvup.Exp,
                "Strength": lvup.Strength,
                "Magic": lvup.Magic,
                "Defense": lvup.Defense,
                "Ap": lvup.Ap,
                "SwordAbility": lvup.SwordAbility,
                "ShieldAbility": lvup.ShieldAbility,
                "StaffAbility": lvup.StaffAbility,
                "Padding": 0,
                "Character": lvup.Character,
                "Level": lvup.Level
            }

        formattedBons = {}
        for bons in bonsList:
            if not bons.RewardId in formattedBons.keys():
                formattedBons[bons.RewardId] = {}
            formattedBons[bons.RewardId][bons.getCharacterName()] = {
                "RewardId": bons.RewardId,
                "CharacterId": bons.CharacterId,
                "HpIncrease": bons.HpIncrease,
                "MpIncrease": bons.MpIncrease,
                "DriveGaugeUpgrade": bons.DriveGaugeUpgrade,
                "ItemSlotUpgrade": bons.ItemSlotUpgrade,
                "AccessorySlotUpgrade": bons.AccessorySlotUpgrade,
                "ArmorSlotUpgrade": bons.ArmorSlotUpgrade,
                "BonusItem1": bons.BonusItem1,
                "BonusItem2": bons.BonusItem2,
                "Unknown0c": 0
            }

        formattedFmlv = {}
        for fmlv in fmlvList:
            if not fmlv.getFormName() in formattedFmlv.keys():
                formattedFmlv[fmlv.getFormName()] = []
            formattedFmlv[fmlv.getFormName()].append({
                "Ability": fmlv.Ability,
                "Experience": fmlv.Experience,
                "FormId": fmlv.FormId,
                "FormLevel": fmlv.FormLevel,
                "GrowthAbilityLevel": fmlv.GrowthAbilityLevel,
            })

        formattedItem = {"Stats": []}
        for item in itemList:
            formattedItem["Stats"].append({
                "Id": item.Id,
                "Attack": item.Attack,
                "Magic": item.Magic,
                "Defense": item.Defense,
                "Ability": item.Ability,
                "AbilityPoints": item.AbilityPoints,
                "Unknown08": item.Unknown08,
                "FireResistance": item.FireResistance,
                "IceResistance": item.IceResistance,
                "LightningResistance": item.LightningResistance,
                "DarkResistance": item.DarkResistance,
                "Unknown0d": item.Unknown0d,
                "GeneralResistance": item.GeneralResistance,
                "Unknown": item.Unknown
            })

        formattedPlrp = []
        for plrp in plrpList:
            formattedPlrp.append({
                "Character": plrp.Character,
                "Difficulty": plrp.Difficulty,
                "Hp": plrp.Hp,
                "Mp": plrp.Mp,
                "Ap": plrp.Ap,
                "Unknown06": plrp.Unknown06,
                "Unknown08": plrp.Unknown08,
                "Unknown0a": plrp.Unknown0a,
                "Objects": plrp.Objects
            })

        sys = [{"id": 17198, "en":""}]
        for i in range(7):
            sys[0]["en"] += random.choice(hashTextEntries)
            if i < 6:
                sys[0]["en"] += " "


        

        data = io.BytesIO()
        with zipfile.ZipFile(data, "w") as outZip:
            yaml.emitter.Emitter.process_tag = noop

            

            outZip.writestr("TrsrList.yml", yaml.dump(formattedTrsr, line_break="\r\n"))
            outZip.writestr("BonsList.yml", yaml.dump(formattedBons, line_break="\r\n"))
            outZip.writestr("LvupList.yml", yaml.dump(formattedLvup, line_break="\r\n"))
            outZip.writestr("FmlvList.yml", yaml.dump(formattedFmlv, line_break="\r\n"))
            outZip.writestr("ItemList.yml", yaml.dump(formattedItem, line_break="\r\n"))
            outZip.writestr("PlrpList.yml", yaml.dump(formattedPlrp, line_break="\r\n"))
            outZip.writestr("sys.yml", yaml.dump(sys, line_break=""))

            enemySpoilers = None
            if not enemyOptions["boss"] == "Disabled":
                if enemyOptions.get("boss", False) or enemyOptions.get("enemy", False):
                    from khbr.randomizer import Randomizer as khbr
                    enemySpoilers = khbr().generateToZip("kh2", enemyOptions, mod, outZip)

            outZip.writestr("mod.yml", yaml.dump(mod, line_break="\r\n"))
            outZip.close()
        data.seek(0)
        return data


        

        










    
if __name__ == '__main__':
    randomizer = KH2Randomizer()
    randomizer.populateLocations([locationType.LoD, "ExcludeFrom50"])
    randomizer.populateItems()
    if randomizer.validateCount():
        randomizer.setKeybladeAbilities()
        randomizer.setRewards()
        randomizer.setLevels(soraExpMult = 1.5, formExpMult = {1:6, 2:3, 3:3, 4:3, 5:3})
        randomizer.setBonusStats()
        zip = randomizer.generateZip().getbuffer()
        open("randoSeed.zip", "wb").write(zip)