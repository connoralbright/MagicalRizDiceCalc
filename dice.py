from itertools import groupby


d4 = [1,2,3,4]
d6 = [1,2,3,4,5,6]
d6T = [0,0,0,0,0,6]
d20 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

def main():

    a = riz(diceListX = [d6, d6, d6, d6, d6T, d6T, d6T, d6T,d4, d4], modifierX = 0, rollsX = [], dataX = [])
    b = riz(diceListX = [d6, d6, d6, d6, d6, d6], modifierX = 0, rollsX = [], dataX = [])
    r = results(0,0,0,0)

    rollA = buildRollTable(a)
    rollB = buildRollTable(b)

    for a_index, a_count in enumerate(rollA):
        a_value = a_index + a.modifier
        if a_count > 0:
            for b_index, b_count in enumerate(rollB):
                if b_count > 0:
                    b_value = b_index + b.modifier
                    numberOfRolls = a_count * b_count
                    r.count += 1
                    if a_value > b_value:
                        r.roll1WinCount += 1
                    elif b_value > a_value:
                        r.roll2WinCount += 1
                    else:
                        r.tieCount +=1  
    aDice = dice(a.diceList, a.modifier).diceToString()
    bDice = dice(b.diceList, b.modifier).diceToString()

    print(aDice + ' > ' + bDice + ':', str(round(r.roll1WinCount/r.count*100, 2)) + '%')
    print(r)



class dice():

    diceList = []
    modifier = 0
    def __init__(self,diceList, modifier):
        self.diceList = diceList
        self.modifer = modifier


    def dieToString(self, die):
        if die == d4:
            return 'd4'
        if die == d6:
            return 'd6'
        if die == d6T:
            return 'd6T'
        if die == d20:
            return 'd20'
        
    
    def diceToString(self):
        countedDice = [ [len(list(group)),self.dieToString( key)] for key, group in groupby(self.diceList)]
        s = ''
        for i,j in enumerate(countedDice):
            count = j[0]
            die = j[1]
            if count >1:
                s += str(count)
            s += str(die)
            if i < ( len(countedDice)-1):
                s += '+'
        if self.modifer != 0:
            if (self.modifer > 0):
                s +=  '+'
            s += str(self.modifer) 

            
        return s




class riz:
    diceList    = []
    modifier    = 0
    rolls       = []
    data   = []
    def __init__(self, diceListX, modifierX, rollsX, dataX):
        self.diceList   = diceListX
        self.modifier   = modifierX
        self.rolls      = rollsX
        if dataX == []:
            self.data   = [0]*(diceListSize(self.diceList)+1)
        else:
            self.data = dataX

class results:
    count = 0
    roll1WinCount = 0
    roll2WinCount = 0
    tieCount = 0
    def __init__(self, count, roll1WinCount, roll2WinCount, tieCount):
        self.count              = count
        self.roll1WinCount      = roll1WinCount
        self.roll2WinCount      = roll2WinCount
        self.tieCount           = tieCount
    def __str__(self):
        s = ''
        s += 'Count: '              + str(self.count) + '\n'
        s += 'roll1WinCount: '      + str(self.roll1WinCount) + '\n'
        s += 'roll2WinCount: '      + str(self.roll2WinCount) + '\n'
        s += 'tieCount: '           + str(self.tieCount) + '\n'
        return s

def diceListSize(diceList):
    length = 0
    for die in diceList:
        length += max(die)
    return length


            
def buildRollTable(sideA):

    if len(sideA.diceList) > 0:

        for i in sideA.diceList[0]:
            newSizeA = riz(sideA.diceList, sideA.modifier,sideA.rolls, sideA.data)
            newSizeA.diceList = newSizeA.diceList[1:]
            newSizeA.rolls = sideA.rolls + [i]
            
            if len(newSizeA.diceList) > 0:
                buildRollTable( newSizeA)
            else:
                rollSum = sum(newSizeA.rolls)
                sideA.data[rollSum] += 1
    return sideA.data




if __name__ == '__main__':
    main()