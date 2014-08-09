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
    return "ERR"


def add(augend, addend):
    return Decimal(augend) + Decimal(addend)

def multiply(multiplicand, multiplier):
    return Decimal(multiplicand) * Decimal(multiplier)

def subtract(minuend, subtrahend):
    return Decimal(minuend) - Decimal(subtrahend)

def divide(dividend, divisor):
    if Decimal(divisor) == 0:
        return "#ERR-Division by zero"
    else:
        return Decimal(dividend) / Decimal(divisor)

def emptyToZero():
    return Decimal(0)

def getValue(*args):

    if args[0] == '':
        return Decimal(args[1])
    else:                               #if it's a cell address, return the value # Assumption: for now, we assume it is known, we don't deal with dependencies 
        letterIndex = ord(args[0]) - ord('a')
        numberIndex = int(args[1])-1

        print "---------"        
        print letterIndex
        print "+++++++++"
        return inputData[letterIndex][numberIndex]
#    elif m.match(operand):              
            #print 'zzzzz %d' %(ord(m.groups(1)) - ord('a'))
#            result = m.match(operand)
#            print result.group(1)
#        else:
#            return '#ERR: Invalid operand'
                                        #We should never get here if the getValue regex and regexes in this function are correct.

validExpressions={}
validExpressions[re.compile('^(\d+) (\d+) \+$')] = add
validExpressions[re.compile('^(\d+) (\d+) \-$')] = subtract
validExpressions[re.compile('^(\d+) (\d+) \*$')] = multiply
validExpressions[re.compile('^(\d+) (\d+) \/$')] = divide
validExpressions[re.compile('^$')] = emptyToZero
validExpressions[re.compile('^([a-z]?)(\d+)$')] = getValue




                                        # Assumption: empty cells should be assigned a value of zero
                                        # Assumption: cell range is [a-z][\d+]

if __name__ == '__main__':
    main()
                                        #Apparently this is a Pythonic idiom- StackOverflow.
                                        #Code in functions is compiled to bytecode.
                                        #This means local variables are stored in fixed-size arrays, not dictionaries.  
                                        #This makes lookups faster!

