import sys, csv

inputData=[]

def main():
    getInputData()
    evaluateExpressions()    

def getInputData():
    with open(sys.argv[1], 'rb') as csvfile:
        global inputData 
        dataReader = csv.reader(csvfile, delimiter=',')
        print "\nData read was:"
        for row in dataReader:
            inputData.append(row)
            print ', '.join(row)            

def evaluateExpressions():
    global inputData

    print "\nData stored was:"
    for row in inputData:
        print row

    for row in inputData:
        for element in row:
            print element



if __name__ == '__main__':
    main()
#Apparently this is a Pythonic idiom- StackOverflow.
#Code in functions is compiled to bytecode.
#This means local variables are stord in fixed-size arrays, not dicts.
#This makes lookups faster!

