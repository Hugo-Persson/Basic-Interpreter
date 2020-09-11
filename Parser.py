from interpreter import runInterpreter
import re;

codeIndex = 0

def codeError(message):
    print(message + "at line "+str(codeIndex))
    exit()


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


def getTokenValue(param): #creates a small chunk, it handles values like string and int
    
    isString =  re.search(r"\"|\'",param)
    
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


def tokenizeValue(param): #will take a value like 4+4 or "hello world " or "hello" + var and create a token
    print("PARAM",param)
    strs = []
    variables =[]

    # Find variables by checking for alfabetic character that is not inside string
    inString = False
    stringSign = None
    for char in param:

        if inString:
            if char==stringSign:
                inString=False
            
        else: 
            if char=="'" or char =='"':
                inString=True
                stringSign=char
            #save index so I can later split look at the none string parts

    param = param.replace("AND","&&")
    param = param.replace("OR","||")
    param = param.replace("NOT","!")
    return {"type":"value","strs":strs,"variables":variables}

    

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
        codeError("ERROR: Arr var name too long, exiting application")
    return {"command":"ARRINIT","varId":varId,"arrDepth":arrDepth,"lineNum":obj["lineNum"]} 



def printToken(obj):
    words = obj["filteredWords"]
    words.pop(0)
    return{"lineNum":obj["lineNum"],"command":"PRINT","value":tokenizeValue(words)}

def gotoToken(obj):
    obj["filteredWords"].pop(0)

    val = tokenizeValue(obj["filteredWords"])
    if(val["type"]!="INT"):
        print("ERROR: goto value not int, exiting application")
        exit()
        
    return{"lineNum":obj["lineNum"],"command":"GOTO","value":val}

def variableAssignment(obj):
    regexPattern = re.compile(r"(?<!=)=(?!=)")

    if(obj["filteredWords"][0]=="LET"):
        obj["filteredWords"].pop(0)
    line = " ".join(obj["filteredWords"])
    if(re.search(regexPattern,line)):
        arr = re.split(regexPattern,line) #should look like [x,34]
        if(len(arr[0])>1): #Checking if the varible name is greater than 1 the only time this is allowed is when it is an array
            if("[" in arr[0]):
                
                #indexDepthArr = [int(x[:-1] for x in arr[0].split("["))]
                #indexDepthArr = list(min(map(lambda x: int(x[:-1]),arr[0].split("["))))
                indexes = arr[0].split("[")
                varId = indexes.pop(0) 

                indexDepthArr = list(map((lambda x:int(x[:-1])),indexes))
                
                return {"varId":varId, "command":"VARASSIGN","array":True,"arrDepth":indexDepthArr,"lineNum":obj["lineNum"],"value":tokenizeValue(arr[1])}
            print("ERROR: variable name too long, line 68, exiting application")
            exit()
        else:
            
            return {"lineNum":obj["lineNum"],"command":"VARASSIGN","array":False,"varId":arr.pop(0),"value":tokenizeValue(arr[0])}
    else:
        print("ERROR: Unknow command exiting ")
        exit()


def forToken(obj):
    obj["filteredWords"].pop(0)
    joinedLine = " ".join(obj["filteredWords"])
    chunks = joinedLine.split("TO")
    variableToken = variableAssignment({"filteredWords":chunks[0].split(" "),"lineNum":-1})

    return{"command":"FOR", "variable":variableToken,"TO":int(chunks[1]),"execObjs":[],"STEP":1}

def nextToken(obj):
    return{"command":"NEXT","varId":int(obj["filteredWords"][1])}
def getExecutionObj(line):
    line = line.replace("\n","")
    lineCopy = line
    lineCopy.replace(" ","")
    


    if(len(lineCopy)==0): #deals with empty lines
        return None;
    
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
        "GOTO": gotoToken,
        "IF": ifStatement,
        "FOR":forToken,
        "NEXT":nextToken

    }.get(filteredWords[0],variableAssignment)({"filteredWords":filteredWords,"lineNum":lineNum})
    return token;

def ifStatement(obj):
    obj["filteredWords"].pop(0);
    concattedString = " ".join(obj["filteredWords"])
    if("ELSE" in concattedString):
        return ifElseStatement(obj)
    chunks = concattedString.split("THEN")
    logicalStatement = tokenizeValue(chunks[0])
    execObj = getExecutionObj(chunks[1])
    return {"command":"IF","lineNum":obj["lineNum"],"logicalStatement":logicalStatement,"execObj":execObj}

def ifElseStatement(obj):
    
    concattedString = " ".join(obj["filteredWords"])
    chunks = re.split("THEN | ELSE",concattedString)
    logicalStatement = tokenizeValue(chunks[0])
    ifExecObj = getExecutionObj(chunks[1])
    elseExecObj = getExecutionObj(chunks[2])
    return {"command":"ELSE","lineNum":obj["lineNum"],"logicalStatement":logicalStatement,"ifExecObj":ifExecObj,"elseExecObj":elseExecObj}

def getExecutionArray():
    inForLoop=False
    forToken = []
    executionArray = []
    for line in lines: 
        token = getExecutionObj(line)
        
        if(token==None):
            continue;
        if(token["command"]=="FOR"):
            inForLoop=True
            forToken.append(token)
            continue
        if(token["command"]=="NEXT"):
            for token in forToken:
                if(token["variable"]["varId"]==token["varId"]):
                    forToken.remove(token)
                    executionArray.append(token)
                    continue
        if inForLoop:
            forToken[len(forToken)-1]["execObjs"].append(token)
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
        




