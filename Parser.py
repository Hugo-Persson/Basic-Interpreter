from interpreter import runInterpreter


def getLines():
    f = open("code.bas","r");
    return f.readlines()
lines = getLines();

#Clean white rows
def isFloat(val):
    arr = val.split(".")
    for i in arr:
        if(not i.isnumeric()):
            return False
    return True

def tokenizeValue(param): #will take a value like 4+4 or "hello world " or "hello" + var and create a token
    #Param is either math equation or a value

    isString = '"' in param
    
    token = {}

    if(isString):
        # a string
        stringValue = param.replace('"',"")
        token={"type":"STRING","value":stringValue}

    elif(param.isnumeric()):
        token={"type":"INT","value":param}
    elif(isFloat(param)):
        token={"type":"FLOAT","value":param}
    else:
        if(len(param)>1):
            print("ERROR, variable name too long")
        else:
            token={"type":"VAR","varId":param}
        #probably a var or error
    return token

def arrayToken(obj):
    return {}   

def printToken(obj):
    words = obj["filteredWords"]
    words.pop(0)
    valueText = " ".join(words) #incase a string got splitted up when I split up all spaces earlier
    return{"lineNum":obj["lineNum"],"command":"PRINT","value":tokenizeValue(valueText)}

def gotoToken(obj):


    return

def variableAssignment(obj):
    if(obj["filteredWords"][0]=="LET"):
        obj["filteredWords"].pop(0)
    print (obj)
    noSpaceString = "".join(obj["filteredWords"])
    print(noSpaceString)
    if("=" in noSpaceString):
        arr = noSpaceString.split("=") #should look like [x,34]
        if(len(arr[0])>1):
            print("ERROR: variable name too long")
        else:
            return {"lineNum":obj["lineNum"],"command":"VARASSIGN","varId":arr[0],"value":tokenizeValue(arr[1])}
    

def getExecutionArray():
    executionArray = []
    for line in lines: 
        line = line.replace("\n","")
        lineCopy = line
        lineCopy.replace(" ","")
        
        print("LEN",len(lineCopy))
        if(len(lineCopy)==0):
            print("FOUND line")
            continue
        
        words = line.split(" ")
        
        executionObj = {}
        filteredWords = [word for word in words if word!=" " and word !=""]
        print("Filtered Words", filteredWords)
        lineNum = -1
        if(filteredWords[0].isnumeric()):
            lineNum=filteredWords.pop(0)
            
        if(filteredWords[0]=="REM"):
            return
        
        token = {
            "ARRAY":arrayToken,
            "PRINT":printToken,
            "LET":variableAssignment

        }.get(filteredWords[0],variableAssignment)({"filteredWords":filteredWords,"lineNum":lineNum})
        executionArray.append(token)
        print ("TOKEN",token)
    return executionArray

def getLineDeclaredExecutionList(executionArray):
    lineDeclaredList = {}
    index = 0
    for i in executionArray:
        if(float( i["lineNum"])>-1):
            lineDeclaredList[i["lineNum"]]=index
            index+=1
    return lineDeclaredList



executionArray = getExecutionArray()
lineDeclaredList = getLineDeclaredExecutionList(executionArray)

runInterpreter(executionArray,lineDeclaredList)
        
""" "ARRAY":{"lineNum":lineNum,"command":"VARASSIGN","value":{"type":"ARR","value":"[]"}},
            "PRINT": {"lineNum":lineNum,"command":"PRINT",}
             """




