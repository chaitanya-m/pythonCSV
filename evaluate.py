#Assumption: There are no circular dependencies that indefinitely prevent evaluation of an expression.
# e.g. b2 = b1, b1 = b2.
#So we shall assume that every cell will evaluate to a constant expression, given sufficient iterations
#What might be a more efficient way of solving this? We have a system of equations that could be of any order...
#consider the case where a1 = b1 b1 b1 b1 b1 b1 * + * * * , i.e.  (b1^2 + b1 ) * b1^3
#For now I shall implement a brute force approach wherein I iteratively evaluate the matrix until all values are 
#either constants or #ERRs. A better and more complete solution would lie in building a dependency graph, 
#checking that there are no circular dependencies, then evaluating upwards from the leaves.

import csv, sys, re
from decimal import Decimal

inputData=[]
outputData=[]

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
    global inputData, outputData

    print "\nData stored was:"
    for row in inputData:
        print row

    for row in inputData:
        outputRow=[]
        for cellValue in row:
            cell = evaluateCell(cellValue)
            print cell
            outputRow.append(str(cell))
        outputData.append(outputRow)

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



def add(*args):
    augend = args[1]                    # For readability, though inefficient. args[0] and args[2] are the cell letter prefixes.
    addend = args[3]
    if args[0] == '' and args[2] == '':
        return Decimal(augend) + Decimal(addend)
    else:
        return str(getValue(args[0], args[1])) + ' ' + str(getValue(args[2], args[3])) + ' +'

def subtract(*args):
    minuend = args[1]
    subtrahend = args[3]
    if args[0] == '' and args[2] == '':
        return Decimal(minuend) - Decimal(subtrahend)
    else:
        return str(getValue(args[0], args[1])) + ' ' + str(getValue(args[2], args[3])) + ' -'

def multiply(*args):
    multiplicand = args[1]                   
    multiplier = args[3]
    if args[0] == '' and args[2] == '':
        return Decimal(multiplicand) * Decimal(multiplier)
    else:
        return str(getValue(args[0], args[1])) + ' ' + str(getValue(args[2], args[3])) + ' *'

def divide(*args):
    dividend = args[1]
    divisor = args[3]
    if args[0] == '' and args[2] == '':
        if Decimal(divisor) == 0:
            return "#ERR-Division by zero"
        else:
            return Decimal(dividend) / Decimal(divisor)
    else:
        return str(getValue(args[0], args[1])) + ' ' + str(getValue(args[2], args[3])) + ' /'

def getValue(*args):
    if args[0] == '' and args [1] == '':  
        return Decimal(0)
    elif args[0] == '':
        return Decimal(args[1])
    else:                               #if it's a cell address, return the value # Assumption: for now, we assume it is known, we don't deal with dependencies 
        letterIndex = ord(args[0]) - ord('a')
        numberIndex = int(args[1])-1
        print "letterIndex %d numberIndex %d" %(letterIndex, numberIndex)
        if inputData[numberIndex][letterIndex] == '':
            return 0              
        return inputData[numberIndex][letterIndex]              # rows, columns


validExpressions={}
validExpressions[re.compile('^([a-z]?)(\d+) ([a-z]?)(\d+) \+$')] = add
validExpressions[re.compile('^([a-z]?)(\d+) ([a-z]?)(\d+) \-$')] = subtract
validExpressions[re.compile('^([a-z]?)(\d+) ([a-z]?)(\d+) \*$')] = multiply
validExpressions[re.compile('^([a-z]?)(\d+) ([a-z]?)(\d+) \/$')] = divide
validExpressions[re.compile('^([a-z]?)(\d*)$')] = getValue



                                        # Assumption: empty cells should be assigned a value of zero
                                        # Assumption: cell range is [a-z][\d+]

if __name__ == '__main__':
    main()
                                        #Apparently this is a Pythonic idiom- StackOverflow.
                                        #Code in functions is compiled to bytecode.
                                        #This means local variables are stored in fixed-size arrays, not dictionaries.  
                                        #This makes lookups faster!

