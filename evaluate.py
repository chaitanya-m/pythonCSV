import csv, sys, re
from decimal import Decimal

inputData=[]

#validExpressions={}
#validExpressions[
addition = re.compile('(\d+) (\d+) \+')

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
        for cell in row:
            cellValue = evaluateExpression(cell)
            print cellValue

def evaluateExpression(expression):

    match = addition.match(expression)
    if match is not None:
        return add( Decimal(match.group(1)), Decimal(match.group(2)) )

def add(summand1, summand2):
    return summand1 + summand2


if __name__ == '__main__':
    main()
#Apparently this is a Pythonic idiom- StackOverflow.
#Code in functions is compiled to bytecode.
#This means local variables are stored in fixed-size arrays, not dictionaries.
#This makes lookups faster!

