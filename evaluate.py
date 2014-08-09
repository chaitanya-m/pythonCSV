import csv, sys, re
from decimal import Decimal

inputData=[]

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
    global inputData

    print "\nData stored was:"
    for row in inputData:
        print row

    print "\nValues evaluate to:"
    for row in inputData:
        for cellValue in row:
            cell = evaluateCell(cellValue)
            print cell
            

def evaluateCell(cellValue):

    # Assumption: we expect there not to be more than one match- that would be an invalid cellValue
    # Find if the cellValue corresponds to an expression, extract expression-operand pair
    match = (
        (expression.match(cellValue), operand) for expression, operand in validExpressions.iteritems()
    )

    # Extract groups. 
    match = (
        (args.groups(), operand) for args, operand in match if args is not None
    )

    for args, operand in match:
        return operand(*args)

    # Not in our list of valid expressions
    return "ERR"


def add(augend, addend):
    return Decimal(augend) + Decimal(addend)

def multiply(multiplicand, multiplier):
    return Decimal(multiplicand) * Decimal(multiplier)

def subtract(minuend, subtrahend):
    return Decimal(minuend) - Decimal(subtrahend)

def zero():
    return Decimal(0)

def divide(dividend, divisor):
    if Decimal(divisor) == 0:
        return "#ERR-Division by zero"
    else:
        return Decimal(dividend) / Decimal(divisor)


validExpressions={}
validExpressions[re.compile('(\d+) (\d+) \+')] = add
validExpressions[re.compile('(\d+) (\d+) \-')] = subtract
validExpressions[re.compile('(\d+) (\d+) \*')] = multiply
validExpressions[re.compile('(\d+) (\d+) \/')] = divide
validExpressions[re.compile('^$')] = zero

#Assumption: cell range is [a-z][\d+]

if __name__ == '__main__':
    main()
#Apparently this is a Pythonic idiom- StackOverflow.
#Code in functions is compiled to bytecode.
#This means local variables are stored in fixed-size arrays, not dictionaries.
#This makes lookups faster!

