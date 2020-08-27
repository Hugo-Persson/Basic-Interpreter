""" words = "adb  2 3   5".split(" ")

filteredList = [word for word in words if word!= " " and word != ""]
print (filteredList) """


""" def function():
    print("Hey")
def func():
    print("func")
{"a":function}.get("b",func)() """

""" mathEq = "5+5*4/2 "

print(eval(mathEq))

additionArray = '5+5*2+5-2'.split("-")

print(additionArray)
 """

""" array = '"hello world"'.split('"')
isString = '"' in '"hello world"'
print(array) """

""" arr = "c[3333][3]".split("[")
print(arr[1][:-1]) """


""" arr = [5]
arr[5] = 5
print( arr[5]) """

dimensionFind = [0,1,0] #[0][1][0]





""" arr = [[[],["hi"]]]

arrVal = arr

for i in dimensionFind:
    arrVal= arrVal[i]

 """

""" arr = []
arrValue = arr
for i in range(0,2):
    arrValue.append([])
    arrValue=arrValue[0]

print(arrValue) """

""" a=[]
b=[]
b.append(a)
c=[]
c.append(b)
print(c) """

""" a=[]
b=[]
for i in range(0,0): #becomes end index + 1 depth so this is two dimensional
    a.append(b)
    b=a
    a=[]
print(b) """

""" arr = []
arrValue = arr
for i in range(0,2):
    arrValue.append([])
    arrValue=arrValue[0]

print(arrValue) """


a=[["hey"]]
b=a[0]
c=b[0]
b[0]="Yah"
print(a)