import csv, sys, re
from decimal import Decimal

inputData=[]
outputData=[]
expressionsEvaluated = False

def main():
    getInputData()
    processSpreadsheet()    


def getInputData():
    with open(sys.argv[1], 'rb') as csvfile:
        global inputData 
        dataReader = csv.reader(csvfile, delimiter=',')
        print "\nData read was:"
        for row in dataReader:
            inputData.append(row)
            print ', '.join(row)            


def processSpreadsheet():
    global inputData, outputData, expressionsEvaluated

    print "\nData stored was:"
    for row in inputData:
        print row

    while expressionsEvaluated == False:
        expressionsEvaluated = True
        outputData=[]
        for row in inputData:
            outputRow=[]
            for cellValue in row:
                if re.search(' [\+|\-|\*\|\/]', str(cellValue)) is not None:
                    expressionsEvaluated = False
                cell = evaluateCell(cellValue)
                outputRow.append(str(cell))
            outputData.append(outputRow)
        inputData = outputData

    print "\nValues evaluate to:"
    for row in outputData:
        print ', '.join(row)


def evaluateCell(cellValue):
                                        # Assumption: we expect there not to be more than one match- that would be an invalid cellValue
                                        # Find if the cellValue corresponds to an expression, extract expression-operator pair
    match = (
        (expression.match(cellValue), operator) for expression, operator in validExpressions.iteritems()
    )

                                        # Extract groups. 
    match = (
        (args.groups(), operator) for args, operator in match if args is not None
    )

    for args, operator in match:
        return operator(*args)

                                        # Not in our list of valid expressions
    return "#ERR"


#These operators can be abstracted away for more elegant code. 
def binaryOperation(*args):

    if args[5] == '+':
        return add(*args)
    elif args[5] == '-':
        return subtract(*args)
    elif args[5] == '*':
        return multiply(*args)
    elif args[5] == '/':
        return divide(*args)
    else:
        return "#ERR"

def add(*args):
    augend = args[2]                    # For readability, though inefficient. args[0] and args[2] are the cell letter prefixes.
    addend = args[4]
    if args[1] == '' and args[3] == '':
        return Decimal(augend) + Decimal(addend)
    else:
        return str(getValue(args[1], args[2])) + ' ' + str(getValue(args[3], args[4])) + ' +'

def subtract(*args):
    minuend = args[2]
    subtrahend = args[4]
    if args[1] == '' and args[3] == '':
        return Decimal(minuend) - Decimal(subtrahend)
    else:
        return str(getValue(args[1], args[2])) + ' ' + str(getValue(args[3], args[4])) + ' -'

def multiply(*args):
    multiplicand = args[2]                   
    multiplier = args[4]
    if args[1] == '' and args[3] == '':
        return Decimal(multiplicand) * Decimal(multiplier)
    else:
        return str(getValue(args[1], args[2])) + ' ' + str(getValue(args[3], args[4])) + ' *'

def divide(*args):
    dividend = args[2]
    divisor = args[4]
    if args[1] == '' and args[3] == '':
        if Decimal(divisor) == 0:
            return "#ERR-Division by zero"
        else:
            return Decimal(dividend) / Decimal(divisor)
    else:
        return str(getValue(args[1], args[2])) + ' ' + str(getValue(args[3], args[4])) + ' /'

def getValue(*args):
    if args[0] == '' and args [1] == '':  
        return Decimal(0)
    elif args[0] == '':
        return Decimal(args[1])
    else:
                             #if it's a cell address, return the value # Assumption: for now, we assume it is known, we don't deal with dependencies
        letterIndex = ord(args[0]) - ord('a')
        numberIndex = int(args[1])-1
        if inputData[numberIndex][letterIndex] == '':
            return 0              
        return inputData[numberIndex][letterIndex]              # rows, columns

def postFixStackSolve(*args):
    #Our regex for this could be improved to save some computation here. At the moment, it finds the last binary operation... we need the first one.
    #For now, we will re-search for the first binary subexpression in args[0] or args[6], whichever one is not None(upon matching the first one, the regex won't match again... mutual exclusion)
    if args[0] is not None:
        binarySubexpression = binaryOperationRE.search(str(args[0]))
        binaryArgs = binarySubexpression.groups()
        evalVal = re.sub(binaryOperationRE, str(binaryOperation(*binaryArgs)), str(args[0]))
        return evalVal

    elif args[6] is not None:
        binarySubexpression = binaryOperationRE.search(str(args[6]))
        binaryArgs = binarySubexpression.groups()
        evalVal = re.sub(binaryOperationRE, str(binaryOperation(*binaryArgs)), str(args[6]))
        return evalVal

    else:
        return "#ERR"

binaryOperationRE = re.compile('(([a-z]?)(\-*\d+) ([a-z]?)(\-*\d+) ([\+|\-|\*|\/]))')
binaryOperationREStrict = re.compile('^(([a-z]?)(\-*\d+) ([a-z]?)(\-*\d+) ([\+|\-|\*|\/]))$')
validExpressions={}
validExpressions[binaryOperationREStrict] = binaryOperation
validExpressions[re.compile('^([a-z]?)(\-*\d*(\.\d+)?)$')] = getValue
validExpressions[re.compile('(^.+( ([a-z]?)(\-*\d+) ([a-z]?)(\-*\d+) [\+|\-|\*|\/])+.*$)|(^.*(([a-z]?)(\-*\d+) ([a-z]?)(\-*\d+) [\+|\-|\*|\/])+ .+$)')] = postFixStackSolve

if __name__ == '__main__':
    main()

