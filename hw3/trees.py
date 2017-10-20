import numpy
import math
import pylab as plt

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
        return root.val

def getLabelValues(root, data):
    curLabel = []
    for d in data:
        curLabel.append(getVal(root, d))
    return curLabel

def getCLabel(data,col,val):
    retData = []
    for d in data:
        if d[col] == val:
            retData.append(d)
    return retData

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

#def getNumNodes(root):
#    if root.leaf == True or root == None:
#        return 0
#    else:
#        val = 1
#        if root.left != None:
#            val = val + getNumNodes(root.left)
#
#        if root.right != None:
#            val = val + getNumNodes(root.right)
#
#        return val


def computeError(root, trainData, weights):
    err = 0
    total = 0
    for d in trainData:
        label = getValidLabel(root, d)
        if label != d[0]:
            err = err + weights[total];
        total = total + 1

    return (err)

filename = 'heart_train.data'
dump = open(filename, 'rt')
d=numpy.loadtxt(dump,delimiter=',', dtype=numpy.int)
numFeatures=23
for values in d:
    for i in range(0,numFeatures):
        if values[i] == 0:
            values[i] = -1

filename2 = 'heart_test.data'
testdump = open(filename2, 'rt')
testData=numpy.loadtxt(testdump,delimiter=',', dtype=numpy.int)
for values in testData:
    for i in range(0,numFeatures):
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
# use d for coordinate descent
# get 1 rooted trees (22 of them)
for i in range(1,numFeatures):
    #root = decisionTree(d, 1, weights, 2, i)
    root = Tree(i,False,-1)
    root.left = Tree(-1, True, -1)
    root.right = Tree(-1, True, 1)
    oneTrees.append(root)
    root = Tree(i,False,-1)
    root.left = Tree(-1, True, 1)
    root.right = Tree(-1, True, -1)
    oneTrees.append(root)
    root = Tree(i,False,-1)
    root.left = Tree(-1, True, -1)
    root.right = Tree(-1, True, -1)
    oneTrees.append(root)
    root = Tree(i,False,-1)
    root.left = Tree(-1, True, 1)
    root.right = Tree(-1, True, 1)
    oneTrees.append(root)

twoTrees = []
for i in range(0,numFeatures-1):
    for j in range(0, len(oneTrees)):
        root = Tree(i, False, -1)
        root.right = Tree(-1, True, -1)
        root.left = copyTree(oneTrees[j])
        twoTrees.append(root)
        root = Tree(i, False, -1)
        root.right = Tree(-1, True, 1)
        root.left = copyTree(oneTrees[j])
        twoTrees.append(root)
    
    for j in range(0, len(oneTrees)):
        root = Tree(i, False, -1)
        root.left = Tree(-1, True, -1)
        root.right = copyTree(oneTrees[j])
        twoTrees.append(root)
        root = Tree(i, False, -1)
        root.left = Tree(-1, True, 1)
        root.right = copyTree(oneTrees[j])
        twoTrees.append(root)

threeTrees = []
for i in range(0, numFeatures-1):
    for j in range(0, len(twoTrees)):
        root = Tree(i, False, -1)
        root.right = Tree(-1, True, 1)
        root.left = copyTree(twoTrees[j])
        threeTrees.append(root)
        root = Tree(i, False, -1)
        root.right = Tree(-1, True, -1)
        root.left = copyTree(twoTrees[j])
        threeTrees.append(root)

    for j in range(0, len(twoTrees)):
        root = Tree(i, False, -1)
        root.left = Tree(-1, True, 1)
        root.right = copyTree(twoTrees[j])
        threeTrees.append(root)
        root = Tree(i, False, -1)
        root.left = Tree(-1, True, -1)
        root.right = copyTree(twoTrees[j])
        threeTrees.append(root)

for i in range(0, numFeatures-1):
    for j in range(0, len(oneTrees)):
        for k in range(0, len(oneTrees)):
            root = Tree(i, False, -1)
            root.left = copyTree(oneTrees[j])
            root.right = copyTree(oneTrees[k])
            threeTrees.append(root)

#print("Populating 3 attribute trees")
#for tree in threeTrees:
  #  populateData(tree, d, 1)

print("3 internal node trees: ",len(threeTrees))
ita = 10
for j in range(0,ita):
    # use threeTrees list to find the min error
    error = 1
    index = 0
    i = 0
    for tree in threeTrees:
        e = computeError(tree, d, weights)
        if e <= error:
            error = e
            index = i

        i=i+1

    trees.append(threeTrees[index])
    #if j == 0:
    #    for i in range(0, dataCount):
    #        weights[i] = 1/dataCount
    print("Error: ", error)
    # calculate alpha
    alpha = 0.5 * (math.log((1-error)/error))
    print("aplha round: ", j+1, " :",alpha)
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

j = range(0,ita)
plt.title("Level 3 Trees")
plt.plot(j, trainAccList, 'r-', label= 'train accuracy')
plt.plot(j, testAccList, 'b-', label='test accuracy')
plt.legend(loc='center')
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
coordinate_alphas = []
for i in range(0, len(oneTrees)):
    coordinate_alphas.append(1/22)

print("Adaboost on trees with 1 attribute")
trainAccList = []
testAccList = []
ite = 200
for j in range(0,ite):
    error = 1
    index = 0
    i = 0
    for tree in oneTrees:
        e = computeError(tree, d, weights)
        if e < error:
            error = e
            index = i

        i=i+1

    trees.append(oneTrees[index])
    #if j == 0:
    #    for i in range(0, dataCount):
    #        weights[i] = 1/dataCount
    # calculate alpha
    alpha = 0.5 * (math.log((1-error)/error))
    print("aplha round: ", j+1, " :",alpha)
    alphas.append(alpha)
    # update weights
    trainedVal = getLabelValues(oneTrees[index], d)
    for i in range(0,dataCount):
        if trainedVal[i] != d[i][0]:
            trainval = 1
        else:
            trainval = -1
        weights[i] = (((math.exp(trainval*alpha)))*weights[i])/(2*(math.sqrt(error*(1-error))))
    #print(weights)
    trainAcc = findAccuracy(d, trees, alphas)
    testAcc = findAccuracy(testData, trees, alphas)
    #print("train acc on 1 level tree: ", trainAcc)
    #print("test acc on 1 level tree: ", testAcc)
    trainAccList.append(trainAcc)
    testAccList.append(testAcc)

j = range(0,ite)
plt.title("Level 1 Trees")
plt.plot(j, trainAccList, 'r-', label = 'train accuracy')
plt.plot(j, testAccList, 'b-', label='test accuracy')
plt.legend(loc='center')


# use d for coordinate descent
# get 1 rooted trees (22 of them)
print("initial coordinate alphas: \n",coordinate_alphas)
expVal = 0
for values in d:
    total = 0
    for i in range(0,numFeatures-1):
       total = total + coordinate_alphas[i]*getVal(oneTrees[i], values)

    total = (-values[0]) * total
    expVal = expVal + math.exp(total)

print("Exponential Loss before descent: ", expVal)
# for 10 iterations:
trainAccList = []
testAccList = []
for it in range(0, ite):
    # for all numFeatures-1 features
    for featureId in range(0,len(oneTrees)):
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
                for j in range(0,len(oneTrees)):
                    if j != featureId:
                        value = value + coordinate_alphas[j]*getVal(oneTrees[j], d[i])
                equals = equals + math.exp(-d[i][0] * (value))
            else:
                value = 0
                for j in range(0,len(oneTrees)):
                    if j != featureId:
                        value = value + coordinate_alphas[j]*getVal(oneTrees[j], d[i])
                unequals = unequals + math.exp(-d[i][0] * value)

        if equals != 0 and unequals != 0:
            new_alpha = 0.5 * math.log(equals/unequals)
            coordinate_alphas[featureId] = new_alpha

    testCoordAcc = findCoordinateAccuracy(testData, oneTrees, coordinate_alphas)
    trainCoordAcc = findCoordinateAccuracy(d, oneTrees, coordinate_alphas)
    trainAccList.append(trainCoordAcc)
    testAccList.append(testCoordAcc)

j = range(0,ite)
plt.plot(j, trainAccList, 'g-', label = 'coord train accuracy')
plt.plot(j, testAccList, 'y-', label='coord test accuracy')
plt.legend(loc='center')
plt.show()
expVal = 0
for values in d:
    total = 0
    for i in range(0,len(oneTrees)):
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
