clc;
clear all;
data=importdata('mush_train.data');
[m,n] = size(data);
label=zeros(m,1);
x=zeros(m,22);
global numNodes;
numNodes = 0;
for index=1:m
    y = data{index};
    [n,p] = size(y);
    if y(1)=='e'
       label(index) = 0;
    else
       label(index) = 1; 
    end
    j = 1;
    k = 3;
    while k <= p
        x(index,j) = y(k);
        k = k + 2;
        j = j + 1;
    end
end
x1 = {'b', 'c', 'x', 'f', 'k', 's'};
p1 = findProb(x, x1, 1);

x2 = {'f','g','y','s'};
p2 = findProb(x, x2, 2);

x3 = {'n','b','c','g','r', 'p','u','e','w','y'};
p3 = findProb(x, x3, 3);

x4 = {'t','f'};
p4 = findProb(x, x4, 4);

x5 = {'a','l','c','y','f', 'm','n','p','s'};
p5 = findProb(x, x5, 5);

x6 = {'a','d','f','n'};
p6 = findProb(x,x6,6);

x7 = {'c','w','d'};
p7 = findProb(x, x7,7);

x8 = {'b','n'};
p8 = findProb(x, x8, 8);

x9 = {'k','n','b','h','g', 'r','o','p','u','e', 'w','y'};
p9 = findProb(x, x9, 9);

x10 = {'e','t'};
p10 = findProb(x, x10, 10);

x11 = {'b','c','u','e', 'z','r','?'};
p11 = findProb(x, x11, 11);

x12 = {'f','y','k','s'};
p12 = findProb(x, x12, 12);

x13 = {'f','y','k','s'};
p13 = findProb(x, x13,13);

x14 = {'n','b','c','g','o', 'p','e','w','y' };
p14 = findProb(x, x14,14);

x15 = {'n','b','c','g','o', 'p','e','w','y'};
p15 = findProb(x, x15, 15);

x16 = {'p','u'};
p16 = findProb(x, x16,16);

x17 = {'n','o','w','y' };
p17 = findProb(x, x17, 17);

x18 = {'n','o','t'};
p18 = findProb(x, x18,18);

x19 = {'c','e','f','l','n','p','s','z'};
p19 = findProb(x, x19,19);

x20 = {'k','n','b','h','r','o','u','w','y'};
p20 = findProb(x, x20,20);

x21 = {'a','c','n','s','v','y'};
p21 = findProb(x, x21, 21);

x22 = {'g','l','m','p','u','w','d'};
p22 = findProb(x, x22, 22);

atts = {x1;x2;x3;x4;x5;x6;x7;x8;x9;x10;x11;x12;x13;x14;x15;x16;x17;x18;x19;x20;x21;x22};
pvector = {p1;p2;p3;p4;p5;p6;p7;p8;p9;p10;p11;p12;p13;p14;p15;p16;p17;p18;p19;p20;p21;p22};
localLabel = label;
localX = x;
tree = dTreeDesign(label, atts, pvector,x,localLabel, localX, 0);
dispString = ['No. of nodes: ', num2str(numNodes)];
disp(dispString);
testdata = importdata('mush_test.data');
[m,n] = size(testdata);
testlabel=zeros(m,1);
testx=zeros(m,22);
for index=1:m
    testd = testdata{index};
    [n,p] = size(testd);
    if testd(1)=='e'
       testlabel(index) = 0;
    else
       testlabel(index) = 1; 
    end
    j = 1;
    k = 3;
    while k <= p
        testx(index,j) = testd(k);
        k = k + 2;
        j = j + 1;
    end
end

trainrun_label = getLabels(tree, localX, atts, pvector);
pass = 0;
total_run = 0;
[train_m,train_n] = size(trainrun_label);
for i=1:train_m
    if trainrun_label(i) > -1
        if trainrun_label(i) == localLabel(i)
           pass = pass + 1;
        end
        total_run = total_run + 1;
    end
end
accuracy = (pass/total_run)*100;
dispString = ['TrainData Accuracy: ', num2str(accuracy)];
disp(dispString);

testrun_label = getLabels(tree, testx, atts, pvector);
pass = 0;
total_run = 0;
for i=1:m
    if testrun_label(i) > -1
        if testrun_label(i) == testlabel(i)
           pass = pass + 1; 
        end
        total_run = total_run + 1;
    end
end
accuracy = (pass/total_run)*100;
dispString = ['TestData Accuracy: ', num2str(accuracy)];
disp(dispString);

function y = getLabels(tree, testx, atts, pvector)
    [xi, xj] = size(testx);
    y = zeros(xi,1);
    for i = 1:xi
        y(i,1) = getLabel(tree, testx(i,1:xj), atts,pvector);
    end
end

function y = getLabel(tree, xvector, atts, pvector)
    [xi, xj] = size(xvector);
    att = tree.getValues();
    if isempty(att)
       y = -1;
       return;
    elseif att{1} == 'E'
        y = 0;
        return;
    elseif att{1} == 'P'
        y = 1;
        return;
    end
    val = xvector(1, att{1});
    checkAttribute = atts{att{1}};
    [ci, cj] = size(checkAttribute);
    y = -1;
    for i=1:cj
        if char(val) == (checkAttribute{1,i})
            if ~isempty(att{i+1})
               y = getLabel(att{i+1},xvector,atts,pvector);
               if y == -1
                  val = xvector(1,xj);
                  tieatt = atts{22};
                  [ck,cl] = size(tieatt);
                  for j=1:cl
                      if val == tieatt{1,j}
                          break;
                      end
                  end
                  probs = pvector{22};
                  prob = probs(1,j);
                  mean = 1/cl;
                  if prob > mean
                      y = 0;
                  else
                      y = 1;
                  end
               end
               break;
            else
               disp("Ran out of attributes"); 
            end
        end
    end
end

%recursive approach
function y = dTreeDesign(label, atts, pvector,x, localLabel, localX, depth)
    [lrows, lcols] = size(label);
    [xrows, xcols] = size(x);
    global numNodes;
    if checkConsistency(label)
       if label(1) == 1
           disp("Cutting short..Poisonous");
           numNodes=numNodes+1;
          y = tree('P'); 
       else
          disp("Cuttin short..Edible");
          numNodes=numNodes+1;
          y = tree('E');
       end
       return;
    end
    py = findProba(label);
    yentropy = labelEntropy(py);
    ygivenx = zeros(22,1);
    ig = zeros(22,1);
    maxig = 0;
    maxigi = 0;
    for i=1:22
       ygivenx(i) = getYGivenX(label,atts{i},pvector{i},x);
       ig(i) = yentropy - ygivenx(i);
       if maxig <= ig(i) && x(1,i) ~= -1
           maxig = ig(i);
           maxigi = i;
       end
    end
    if (maxigi == 0)
        disp("No more edges at this depth");
        if checkConsistency(label)
            if label(1) == 1
                disp("Poisonous");
                numNodes=numNodes+1;
                y = tree('P');
            else
                disp("Edible");
                numNodes=numNodes+1;
                y = tree('E');
            end
        else
            disp("Algorithm failed to converge");
        end
        return;
    end
    dispString = ['Partition over ', num2str(maxigi)];
    disp(dispString);
    [attsrows, attsCols] = size(atts{maxigi});
    [y id] = tree(maxigi);
    for j = 1:attsCols
        llabel = findLabel(label, atts{maxigi}{j}, maxigi, x);
        llx = findX(x, atts{maxigi}{j}, maxigi);
        [a, b] = size(llabel);
        [c,d] = size(llx);
        if (llabel(1,1) == -2 || llx(1,1) == -2)
            dispString = ['Edge ', atts{maxigi}{j}, ' None'];
            [y cid] = y.addnode(id, []);
            disp(dispString);
            continue;
        end
        dispString = ['Going to edge: ', atts{maxigi}{j}, ' depth=',num2str(depth)];
        disp(dispString);
        numNodes=numNodes+1;
        t = dTreeDesign(llabel, atts, pvector, llx, localLabel, localX, depth+1);
        [y cid] = y.addnode(id, t);
    end
    dispString = ['DFS Done At depth: ', num2str(depth)];
    disp(dispString);
end
%debug function to check label consistency when dfs is done
function y = checkConsistency(label)
    [m,n] = size(label);
    val0 = 0;
    val1 = 0;
    for i=1:m
        if label(i,1) == 1
            val1 = val1+1;
        else
            val0 = val0+1;
        end
    end
    if val0 == 0 && val1 > 0 
       y = true;
    elseif val0 > 0 && val1 == 0
        y = true;
    else
        y = false;
    end
end
%partition of label over attribute and its index
function y = findLabel(label, attribute, attIndex, xlocal)
    [xi, xj] = size(xlocal);
    y(1,1) = -2;
    yi = 0;
    for i=1:xi
        if xlocal(i,attIndex) == attribute
            yi = yi+1;
            y(yi,1) = label(i);
        end
    end
    
end
%partition of X over attribute and its index
function y = findX(X, attribute, attIndex)
    [xi, xj] = size(X);
    for j=1:xj
       y(1,j) = -2; 
    end
    yi = 0;
    for i=1:xi
       if X(i,attIndex) == attribute
          yi = yi + 1;
          for j=1:xj
              if j == attIndex
                y(yi,j) = -1;  
              else
                y(yi, j) = X(i,j);
              end
          end
       end
    end
end
%P(Y|X)
function y = findConditionalProb(label, x, input,index)
    [inputrows, inputcols] = size(input);
    val = 0;
    total = 0;
    for i=1:inputrows
        if input(i,index) == x
            total=total+1;
            if label(i) == 0
                val = val + 1;
            end
        end
    end
    if (val == 0)
        y(1) = 0;
    else
        y(1) = val/total;
    end
    y(2) = 1 - y(1);
end
%conditional entropy
function y = getYGivenX(label, x, pvector, input)
    [x1,x2] = size(x);
    val = 0;
    for i=1:x2
       probX = pvector(i);
       probYGivenX = findConditionalProb(label, x{i}, input,i);
       if probYGivenX(1) == 0
           l0 = 0;
       else
          l0 = log(probYGivenX(1)); 
       end
       
       if probYGivenX(2) == 0
           l1 = 0;
       else
           l1 = log(probYGivenX(2));
       end
       val = val - (probX * (probYGivenX(1)*l0 + probYGivenX(2)*l1));
    end
    y = val;
end
%proabability of label
function y = findProba(label)
    [m,n] = size(label);
    val = 0;
    total = 0;
    for i = 1:m
        if label(i,1) == 0
            val = val + 1;
        end
        total = total + 1;
    end
    y(1) = val/total;
    y(2) = 1-y(1);
end
%entropy of label
function y = labelEntropy(pvector)
    [m,n] = size(pvector);
    val = 0;
    for i = 1:m
        for j=1:n
           if pvector(i,j) == 0
            l = 0;
           else
            l = log(pvector(i,j));
           end
           val = val - pvector(i,j)*l;
        end
    end
    y = val;
end
%probability of attributes
function y = findProb(x, x1, attIndex)
    [m,n] = size(x);
    [p, x1len] = size(x1);
    for x1index=1:x1len
        value = 0;
        total = 0;
        for i=1:m
           if x(i, attIndex) == x1{x1index}
               value = value + 1;
           end
           total = total + 1;
        end
        y(x1index) = value/total;
        if y(x1index) == 0
            attIndex;
            y(x1index);
        end
    end
end