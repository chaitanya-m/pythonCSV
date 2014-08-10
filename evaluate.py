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
                print cellValue
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
    if args[4] == '+':
        return add(*args)
    elif args[4] == '-':
        return subtract(*args)
    elif args[4] == '*':
        return multiply(*args)
    elif args[4] == '/':
        return divide(*args)
    else:
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
    else:
                             #if it's a cell address, return the value # Assumption: for now, we assume it is known, we don't deal with dependencies
        global expressionsEvaluated
        expressionsEvaluated = False
        letterIndex = ord(args[0]) - ord('a')
        numberIndex = int(args[1])-1
        if inputData[numberIndex][letterIndex] == '':
            return 0              
        return inputData[numberIndex][letterIndex]              # rows, columns

def postFixStackSolve(*args):
    #Our regex for this could be improved to save some computation here. At the moment, it finds the last binary operation... we need the first one.
    #For now, we will re-search for the first binary subexpression in args[0] or args[6], whichever one is not None(upon matching the first one, the regex won't match again... mutual exclusion)
    print "====================================="
    if args[0] is not None:
        return args[0]
    elif args[6] is not None:
        return args[6]
    else:
        return "#ERR"
    print "====================================="

binaryOperationRE = re.compile('^([a-z]?)(\d+) ([a-z]?)(\d+) ([\+|\-|\*|\/])$')
validExpressions={}
validExpressions[binaryOperationRE] = binaryOperation
validExpressions[re.compile('^([a-z]?)(\d*)$')] = getValue
validExpressions[re.compile('(^.+( ([a-z]?)(\d+) ([a-z]?)(\d+) [\+|\-|\*|\/])+.*$)|(^.*(([a-z]?)(\d+) ([a-z]?)(\d+) [\+|\-|\*|\/])+ .+$)')] = postFixStackSolve
#To keep the regex simple, we simply test for the presence of a binary postfix sub-expression with any tokens that precede or succeed it.
#If the tokens are invalid, we will reach a state with either an invalid binary expression or no match to any of our operators
#The token that must precede or succeed cannot be a whitespace... that would eventually lead to #ERR.
#We will evaluate our first match using the evaluateCell method (name must be changed)


#validExpressions[re.compile('^(([a-z]?)(\d+))+ [\+|\-|\*|\/]* (([a-z]?)(\d+) ([a-z]?)(\d+) [\+|\-|\*|\/])+ (([a-z]?)(\d+))* [\+|\-|\*|\/]*$')] = postFixStackSolve
#validExpressions[re.compile('^((([a-z]?)(\d+))+ [\+ |\- |\* |\/ ]*)+(([a-z]?)(\d+) ([a-z]?)(\d+) [\+|\-|\*|\/]+)+ ((([a-z]?)(\d+) )*[\+ |\- |\* |\/ ]*)*$')] = postFixStackSolve

#[\+|\-|\*|\/]+

#^((([a-z]?)(\d+))+ [\+|\-|\*|\/]* (([a-z]?)(\d+) ([a-z]?)(\d+) [\+|\-|\*|\/]+)+)

#.*$|^((([a-z]?)(\d+) ([a-z]?)(\d+) [\+|\-|\*|\/]+)+ (([a-z]?)(\d+))+ [\+|\-|\*|\/]*.*)$')] = postFixStackSolve

#(([a-z]?)(\d+))+ [\+|\-|\*|\/]* 
#(([a-z]?)(\d+))* [\+|\-|\*|\/]*$')] 

# This regex expects the first token to be a valid atomic expression.
# The next token can be a valid atomic expression or an operator
# At least one sequence of two valid atomic expressions and one operator must exist for the postfix to be valid and reduce to a binary postfix primitive
# Finally, we may have any number of atomic expressions and operators... the expression might be found to be invalid at some point in the evaluation process
# It also shouldn't match simple binary expressions- that is left to the other functions. This implies atleast one more atomic expression, either before or after it. 
# (Just an extra operator is obviously invalid).

                                        # Assumption: empty cells should be assigned a value of zero
                                        # Assumption: cell range is [a-z][\d+]

if __name__ == '__main__':
    main()
                                        #Apparently this is a Pythonic idiom- StackOverflow.
                                        #Code in functions is compiled to bytecode.
                                        #This means local variables are stored in fixed-size arrays, not dictionaries.  
                                        #This makes lookups faster!

