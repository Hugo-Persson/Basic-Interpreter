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

    #param = " ".join(param)#incase a string got splitted up when I split up all spaces earlier (fix big problem, a string will add spaces )
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
    obj["filteredWords"].pop(0)

    varId = None
    arrDepth = 1
    if("," in obj["filteredWords"][0]):
        arr = obj["filteredWords"][0].split(",") # for a a line like ARRAY c,3 the array should look like [c,3]
        varId=arr[0]
        arrDepth = int(arr[1])
    else:
        varId=obj["filteredWords"][0]
    if(len(varId)>1):
        print("ERROR: Arr var name too long")
        return
    return {"command":"ARRINIT","varId":varId,"arrDepth":arrDepth,"lineNum":obj["lineNum"]} 

def printToken(obj):
    words = obj["filteredWords"]
    words.pop(0)
    return{"lineNum":obj["lineNum"],"command":"PRINT","value":tokenizeValue(words)}

def gotoToken(obj):
    obj["filteredWords"].pop(0)

    val = tokenizeValue(obj["filteredWords"])
    if(val["type"]!="INT"):
        print("ERROR: goto value not int")
    return{"lineNum":obj["lineNum"],"command":"GOTO","value":val}

def variableAssignment(obj):
    if(obj["filteredWords"][0]=="LET"):
        obj["filteredWords"].pop(0)
    line = " ".join(obj["filteredWords"])
    if("=" in line):
        arr = line.split("=") #should look like [x,34]
        if(len(arr[0])>1): #Checking if the varible name is greater than 1 the only time this is allowed is when it is an array
            if("[" in arr[0]):
                
                #indexDepthArr = [int(x[:-1] for x in arr[0].split("["))]
                #indexDepthArr = list(min(map(lambda x: int(x[:-1]),arr[0].split("["))))
                indexes = arr[0].split("[")
                varId = indexes.pop(0) 

                indexDepthArr = list(map((lambda x:int(x[:-1])),indexes))
                
                return {"varId":varId, "command":"VARASSIGN","array":True,"arrDepth":indexDepthArr,"lineNum":obj["lineNum"],"value":tokenizeValue(arr[1])}
            print("ERROR: variable name too long, line 68")
        else:
            return {"lineNum":obj["lineNum"],"command":"VARASSIGN","array":False,"varId":arr.pop(0),"value":tokenizeValue(arr)}
    

def getExecutionArray():
    executionArray = []
    for line in lines: 
        line = line.replace("\n","")
        lineCopy = line
        lineCopy.replace(" ","")
        
        if(len(lineCopy)==0): #deals with empty lines
            continue
        
        words = line.split(" ")
        
        executionObj = {}
        filteredWords = [word for word in words if word!=" " and word !=""]
        lineNum = -1
        if(filteredWords[0].isnumeric()):
            lineNum=filteredWords.pop(0)
            
        if(filteredWords[0]=="REM"):
            return
        
        token = {
            "ARRAY":arrayToken,
            "PRINT":printToken,
            "LET":variableAssignment,
            "GOTO": gotoToken

        }.get(filteredWords[0],variableAssignment)({"filteredWords":filteredWords,"lineNum":lineNum})
        executionArray.append(token)
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

runInterpreter(executionArray,lineDeclaredList,0)
        




