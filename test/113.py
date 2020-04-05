class LevelDef:
    def __init__(self, aName = "???"):
        self.name = aName;
        self.plusNumber = 1;
        self.minusNumber = 1;
        self.ghostEntries = list();
        self.diamondDropAmount = 1;
        self.ghostsDefeatedForDiamondDrop = 1;
        self.totalSeconds = 60;
        self.enemyAmount = 1;

global LIST;
LIST = list();
        
        
#This is the way to add levels:

lv = LevelDef("1: positivos");
lv.plusNumber = 1;
lv.minusNumber = 1;
lv.ghostEntries = [1,2,3,4,5];
lv.diamondDropAmount = 4;
lv.ghostsDefeatedForDiamondDrop = 1;
lv.totalSeconds = 120;#60 * 3;
lv.enemyAmount = 1;
LIST.append(lv);

#TODO: Add more levels here:

lv = LevelDef("2: negativos");
lv.plusNumber = 1;
lv.minusNumber = 1;
lv.ghostEntries = [-1,-2,-3,-4,-5];
lv.diamondDropAmount = 4;
lv.ghostsDefeatedForDiamondDrop = 1;
lv.totalSeconds = 120;#60 * 3;
lv.enemyAmount = 1;
LIST.append(lv);

lv = LevelDef("3: negativos y positivos");
lv.plusNumber = 1;
lv.minusNumber = 1;
lv.ghostEntries = [1,-2,3,-4,5];
lv.diamondDropAmount = 2;
lv.ghostsDefeatedForDiamondDrop = 1;
lv.totalSeconds = 120;#60 * 3;
lv.enemyAmount = 2;
LIST.append(lv);

lv = LevelDef("4: yendo hacia negativos por accidente");
lv.plusNumber = 1;
lv.minusNumber = 4;
lv.ghostEntries = [3,9,7,3,11];
lv.diamondDropAmount = 2;
lv.ghostsDefeatedForDiamondDrop = 1;
lv.totalSeconds = 120;#60 * 3;
lv.enemyAmount = 1;
LIST.append(lv);

lv = LevelDef("5: manejo de paridades y desparidades");
lv.plusNumber = 3;
lv.minusNumber = 2;
lv.ghostEntries = [-3,-7,8,12,17,6];
lv.diamondDropAmount = 2;
lv.ghostsDefeatedForDiamondDrop = 1;
lv.totalSeconds = 120;#60 * 3;
lv.enemyAmount = 2;
LIST.append(lv);


lv = LevelDef("6: manejo de paridades y desparidades mas dificil");
lv.plusNumber = 5;
lv.minusNumber = 3;
lv.ghostEntries = [-4,-8,11,15,-17,8];
lv.diamondDropAmount = 3;
lv.ghostsDefeatedForDiamondDrop = 1;
lv.totalSeconds = 120;#60 * 3;
lv.enemyAmount = 2;
LIST.append(lv);



lv = LevelDef("7: pares y medio complicado");
lv.plusNumber = 6;
lv.minusNumber = 4;
lv.ghostEntries = [2,-3,11,-15,-13,5,16];
lv.diamondDropAmount = 3;
lv.ghostsDefeatedForDiamondDrop = 1;
lv.totalSeconds = 120;#60 * 3;
lv.enemyAmount = 2;
LIST.append(lv);



lv = LevelDef("8: ultimo piso, todo mal, muchos fantasmas, numeros altos, poco tiempo, restos, todo");
lv.plusNumber = 4;
lv.minusNumber = 8;
lv.ghostEntries = [43,-55,37,-57,-43,35,67,79,81];
lv.diamondDropAmount = 4;
lv.ghostsDefeatedForDiamondDrop = 1;
lv.totalSeconds = 120;#60 * 3;
lv.enemyAmount = 2;
LIST.append(lv);