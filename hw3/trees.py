import numpy
import math
import pylab as plt
import perms as perm


class Tree():
    def __init__(self,d,isLeaf,val):
        self.left = None
        self.right = None
        self.data = d
        self.leaf = isLeaf
        self.val = val

def copyTree(root):
    if root != None:
        newd = root.data
        newleaf = root.leaf
        newval = root.val
        tree = Tree(newd,newleaf,newval)
        if root.left != None:
            tree.left = copyTree(root.left)
        else:
            tree.left = None
        if root.right != None:
            tree.right = copyTree(root.right)
        else:
            tree.right = None
        return tree
    else:
        return None

def populateData(root, data, depth):
    if root.leaf == True:
        root.val = findMajority(data)
        return
    feature = root.data
    leftData = getCLabel(data, feature, -1)
    rightData = getCLabel(data, feature, 1)
    if root.left != None:
        populateData(root.left, leftData, depth+1)
    if root.right != None:
        populateData(root.right, rightData, depth+1)
    return

def getVal(root, data):
    if root.leaf == False and data[root.data] == -1:
        return getVal(root.left, data)
    elif root.leaf == False and data[root.data] == 1:
        return getVal(root.right, data)
    else:
        return root.data

def getLabelValues(root, data):
    curLabel = []
    for d in data:
        curLabel.append(getVal(root, d))
    return curLabel
    
def getCEntropy(data, col, weights):
    x0 = 0
    y00 = 0
    y01 = 0
    x1 = 0
    y10 = 0
    y11 = 0
    total = 0
    for d in data:
        if d[col] == -1:
            x0 = x0 + weights[total]
            if d[0] == -1:
                y00 = y00 + weights[total]
            else:
                y01 = y01 + weights[total]
        else:
            x1 = x1 + weights[total]
            if d[0] == -1:
                y10 = y10 + weights[total]
            else:
                y11 = y11 + weights[total]
        total = total + 1
    y0 = 0
    y1 = 0
    if y00 != 0:
        y0 = y00/x0 * math.log(y00/x0)
    if y01 != 0:
        y0 = y0 + (y01/x0 * math.log(y01/x0))
    if y10 != 0:
        y1 = y10/x1 * math.log(y10/x1)
    if y11 != 0:
        y1 = y1 + (y11/x1 * math.log(y11/x1))
    entropy=0-(((x0)*(y0))+((x1)*(y1)))
    return entropy

def getCLabel(data,col,val):
    retData = []
    for d in data:
        if d[col] == val:
            retData.append(d)
    return retData

def isOnlyLabel(data):
    d0 = 0
    d1 = 0
    total = 0
    for d in data:
        if d[0] == -1:
            d0 = d0 + 1
        else:
            d1 = d1 + 1
        total = total+1
    if total == d0:
        return True
    if total == d1:
        return True
    else:
        return False

def printTree(root, depth):
    print("data: ", root.data, " Leaf: ", root.leaf, " val: ", root.val, " depth: ", depth)
    if root.left != None:
        print("LEFT: ")
        printTree(root.left,depth+1)
    else:
        print("LEFT: NONE")
    if root.right != None:
        print("RIGHT: ")
        printTree(root.right,depth+1)
    else:
        print("RIGHT: NONE")

def findMajority(data):
    d0 = 0
    d1 = 0
    for d in data:
        if d[0] == -1:
            d0 = d0 + 1
        else:
            d1 = d1 + 1
    if d1>d0:
        return 1
    else:
        return -1

def getLabelEntropy(data, weights):
    y0 = 0
    y1 = 0
    total = 0
    totalW = 0
    for d in data:
        if d[0] == -1:
            y0 = y0 + weights[total]
        else:
            y1 = y1 + weights[total]
        total = total + 1
    entropy = 0
    if y0!=0:
        entropy = y0*math.log(y0)
    if y1!=0:
        entropy = entropy + (y1*math.log(y1))
    return 0-entropy


def decisionTree(data, depth, weights, maxdepth, rootVal):
    if depth == maxdepth:
        val = findMajority(data)
        root = Tree(-1, True, val)
        return root

    maxi = rootVal
    if rootVal != -1:
        root = Tree(rootVal, False, -1)
    else:
        yentropy=getLabelEntropy(data, weights)
        ig = 0
        maxi = 1
        for i in range(1,23):
           entr = getCEntropy(data,i, weights)
           localig = yentropy - entr;
           if ig <= localig:
               ig = localig
               maxi = i
        root = Tree(maxi, False, -1)

    leftdata = getCLabel(data,maxi,-1)
    if len(leftdata) != 0:
        if isOnlyLabel(leftdata):
            if leftdata[0][0]==-1:
                root.left = Tree(-2,True,-1)
            else:
                root.left = Tree(-2,True,1)
        else:
            root.left = decisionTree(leftdata, depth+1, weights, maxdepth, -1)
    rightdata = getCLabel(data,maxi,1)
    if len(rightdata) != 0:
        if isOnlyLabel(rightdata):
            if rightdata[0][0]==-1:
                root.right = Tree(-2,True,-1)
            else:
                root.right = Tree(-2,True,1)
        else:
            root.right = decisionTree(rightdata, depth+1, weights, maxdepth, -1)
    return root

def getValidLabel(root, trainRow):
    d = root.data
    if d > 0:
        if trainRow[d] == -1:
            return getValidLabel(root.left, trainRow)
        else:
            return getValidLabel(root.right, trainRow)
    else:
        return root.val

def findAccuracy(testData, trees, alphas):
    testTotal = 0
    acc = 0
    for testVal in testData:
        total = 0
        space = len(alphas)
        for j in range(0,space):
            total = total + alphas[j]*getValidLabel(trees[j],testVal)
        if total > 0:
            if testVal[0] == 1:
                acc=acc+1
        else:
            if testVal[0] == -1:
                acc=acc+1
        testTotal = testTotal + 1
    #print("ACC: ", acc, " TOTAL: ", testTotal)
    return acc/testTotal

def getNumNodes(root):
    if root.leaf == True or root == None:
        return 0
    else:
        val = 1
        if root.left != None:
            val = val + getNumNodes(root.left)

        if root.right != None:
            val = val + getNumNodes(root.right)

        return val


trainedLabel=[]
def computeError(root, trainData, weights):
    err = 0
    total = 0
    errtotal = 0
    for d in trainData:
        label = getValidLabel(root, d)
        if label != d[0]:
            err = err + weights[total];
            errtotal = errtotal + 1
        total = total + 1
        trainedLabel.append(label)
    return (err)

filename = 'heart_train.data'
dump = open(filename, 'rt')
d=numpy.loadtxt(dump,delimiter=',', dtype=numpy.int)
for values in d:
    for i in range(0,23):
        if values[i] == 0:
            values[i] = -1

filename = 'heart_test.data'
testdump = open(filename, 'rt')
testData=numpy.loadtxt(testdump,delimiter=',', dtype=numpy.int)
for values in d:
    for i in range(0,23):
        if values[i] == 0:
            values[i] = -1

weights = []
trees = []
alphas = []
dataCount = len(d)
for i in range(0, dataCount):
    weights.append(1/dataCount)

maxdepth = 3
trainAccList = []
testAccList = []
oneTrees = []
coordinate_alphas = []
# use d for coordinate descent
# get 1 rooted trees (22 of them)
for i in range(1,23):
    root = decisionTree(d, 1, weights, 2, i)
    oneTrees.append(root)
    coordinate_alphas.append(1/5)

twoTrees = []
for i in range(0,len(oneTrees)):
    root = copyTree(oneTrees[i])
    for j in range(0, len(oneTrees)):
        if i!=j:
            root.left = copyTree(oneTrees[j])
            twoTrees.append(root)
    
    root = copyTree(oneTrees[i])
    for j in range(0, len(oneTrees)):
        if i!=j:
            root.right = copyTree(oneTrees[j])
            twoTrees.append(root)

threeTrees = []
for i in range(0, len(oneTrees)):
    root = copyTree(oneTrees[i])
    for j in range(0, len(twoTrees)):
        if i!=j:
            root.left = copyTree(twoTrees[j])
            threeTrees.append(root)

    root = copyTree(oneTrees[i])
    for j in range(0, len(twoTrees)):
        if i!=j:
            root.left = copyTree(twoTrees[j])
            threeTrees.append(root)

for i in range(0, len(oneTrees)):
    root = copyTree(oneTrees[i])
    for j in range(0, len(oneTrees)):
        if i!=j:
            root.left = copyTree(oneTrees[j])
            for k in range(0, len(oneTrees)):
                if j!=k:
                    root.right = copyTree(oneTrees[k])
                    threeTrees.append(root)

    root = copyTree(oneTrees[i])
    for j in range(0, len(oneTrees)):
        if i!=j:
            root.right = copyTree(oneTrees[j])
            for k in range(0, len(oneTrees)):
                if j!=k:
                    root.left = copyTree(oneTrees[k])
                    threeTrees.append(root)

treei = 0
print("Populating 3 attribute trees")
for tree in threeTrees:
    treei= treei+1
    populateData(tree, d, 1)

print(len(threeTrees))
for j in range(0,10):
    # use threeTrees list to find the min error
    error = float("inf")
    index = 0
    i = 0
    for tree in threeTrees:
        e = computeError(tree, d, weights)
        if e < error:
            error = e
            index = i

        i=i+1

    error = computeError(threeTrees[index], d, weights)
    trees.append(threeTrees[index])
    #if j == 0:
    #    for i in range(0, dataCount):
    #        weights[i] = 1/dataCount
    #print("Error: ", error)
    # calculate alpha
    alpha = 0.5 * (math.log((1-error)/error))
    print("aplha round: ", j, " :",alpha)
    if j < 3:
        printTree(threeTrees[index], 1)

    alphas.append(alpha)
    # update weights
    trainedVal = getLabelValues(threeTrees[index], d)
    for i in range(0,dataCount):
        if trainedVal[i] != d[i][0]:
            trainval = 1
        else:
            trainval = -1
        weights[i] = (((math.exp(trainval*alpha)))*weights[i])/(2*(math.sqrt(error*(1-error))))

    trainAcc = findAccuracy(d, trees, alphas)
    testAcc = findAccuracy(testData, trees, alphas)
    print("Train Acc: ", trainAcc)
    print("Test Acc: ", testAcc)
    trainAccList.append(trainAcc)
    testAccList.append(testAcc)

j = range(0,10)
plt.plot(j, trainAccList, 'r-', j, testAccList, 'bs')
plt.show()

# calculate final accuracy on training data with boosting
# accuracy = findAccuracy(d, alphas, trees)
# calculate accuracy on test data with boosting

def findCoordinateAccuracy(testData, oneTrees, coordinate_alphas):
    testTotal = 0
    acc = 0
    for testVal in testData:
        total = 0
        space = len(coordinate_alphas)
        for j in range(0,space):
            total = total + coordinate_alphas[j]*getVal(oneTrees[j],testVal)
        if total > 0:
            if testVal[0] == 1:
                acc=acc+1
        else:
            if testVal[0] == -1:
                acc=acc+1
        testTotal = testTotal + 1
    #print("ACC: ", acc, " TOTAL: ", testTotal)
    return acc/testTotal

weights = []
trees = []
alphas = []
dataCount = len(d)
for i in range(0, dataCount):
    weights.append(1/dataCount)

maxdepth = 2
oneTrees = []
coordinate_alphas = []
for i in range(1,23):
    root = decisionTree(d, 1, weights, maxdepth, i)
    oneTrees.append(root)
    coordinate_alphas.append(1/5)

print("Adaboost on trees with 1 attribute")
for j in range(0,20):
    error = float("inf")
    index = 0
    i = 0
    for tree in oneTrees:
        e = computeError(tree, d, weights)
        if e < error:
            error = e
            index = i

        i=i+1

    trees.append(root)
    #if j == 0:
    #    for i in range(0, dataCount):
    #        weights[i] = 1/dataCount
    error = computeError(root, d, weights)
    #print("Error: ", error)
    # calculate alpha
    alpha = 0.5 * (math.log((1-error)/error))
    print("aplha round: ", j, " :",alpha)
    alphas.append(alpha)
    # update weights
    trainedVal = getLabelValues(root, d)
    for i in range(0,dataCount):
        if trainedLabel[i] != d[i][0]:
            trainval = 1
        else:
            trainval = -1
        weights[i] = (((math.exp(trainval*alpha)))*weights[i])/(2*(math.sqrt(error*(1-error))))
    #print(weights)

# use d for coordinate descent
# get 1 rooted trees (22 of them)
print("initial coordinate alphas: \n",coordinate_alphas)
expVal = 0
for values in d:
    total = 0
    for i in range(0,22):
       total = total + coordinate_alphas[i]*getVal(oneTrees[i], values)

    total = (-values[0]) * total
    expVal = expVal + math.exp(total)

print("Exponential Loss before descent: ", expVal)
# for 10 iterations:
for it in range(0, 1):
    # for all 22 features
    for featureId in range(0,22):
        # getlabel corresponding to alpha from data
        labels = getLabelValues(oneTrees[featureId], d)
        # for all datapoints if h(label) == label, add exponent to equals
        # else add to unequals and update alpha to 1/2ln(equals/unequals)
        equals = 0
        unequals = 0
        labelCount = len(labels)
        new_alpha = 0
        for i in range(0, labelCount):
            if labels[i] == d[i][0]:
                value = 0
                for j in range(0,22):
                    if j != featureId:
                        value = value + coordinate_alphas[j]*getVal(oneTrees[j], d[i])
                equals = equals + math.exp(-d[i][0] * (value))
            else:
                value = 0
                for j in range(0,22):
                    if j != featureId:
                        value = value + coordinate_alphas[j]*getVal(oneTrees[j], d[i])
                unequals = unequals + math.exp(-d[i][0] * value)

        if equals != 0 and unequals != 0:
            new_alpha = 0.5 * math.log(equals/unequals)
            coordinate_alphas[featureId] = new_alpha

expVal = 0
for values in d:
    total = 0
    for i in range(0,22):
       total = total + coordinate_alphas[i]*getVal(oneTrees[i], values)

    total = (-values[0]) * total
    expVal = expVal + math.exp(total)

print("Exponential Loss after coordinate descent: ", expVal)
testCoordAcc = findCoordinateAccuracy(testData, oneTrees, coordinate_alphas)
print("Coordinate Descent Accuracy on TestData: ", testCoordAcc)
testAdaboostAcc = findAccuracy(testData, trees, alphas)
print("Test Accuracy with Adaboost: ", testAdaboostAcc)
print("Final set of coordinate alphas:\n")
print(coordinate_alphas)
print("Final set of adaboost alphas:\n")
print(alphas)
