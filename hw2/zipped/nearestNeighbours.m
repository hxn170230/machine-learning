data = load('wdbc_train.data');
x = data(:,2:11);
y = data(:,1);
x = zscore(x);
K = [1,5,11,15,21];
vData = load('wdbc_valid.data');
xV = vData(:, 2:11);
xV = zscore(xV);
yV = vData(:,1);
index = 0;
max_acc = 0;
for i = 1:5    
    y_label = k_nn(x,y,xV,K(1,i));
    acc = findAccuracy(yV,y_label);
    dispString = ["Accuracy(ValidData): ", num2str(acc*100), " at k: ", num2str(K(1,i))];
    disp(dispString);
    if acc > max_acc
        index = i;
        max_acc = acc;
    end
end
tData = load('wdbc_test.data');
yT = tData(:,1);
xT = tData(:, 2:11);
xT = zscore(tData(:,2:11));
for i = 1:5    
    y_label = k_nn(x,y,xV,K(1,i));
    acc = findAccuracy(yV,y_label);
    dispString = ["Accuracy(TestData): ", num2str(acc*100), " at k: ", num2str(K(1,i))];
    disp(dispString);
    if acc > max_acc
        index = i;
        max_acc = acc;
    end
end

function y = findAccuracy(given,learnt)
    correct = 0;
    [m n] = size(given);
    for i=1:m
        if given(i,1)*learnt(i,1) > 0
            correct = correct+1;
        end
    end
    y = correct/m;
end

function y = k_nn(x,y,x_in,k)
    [p q] = size(x_in);
    [m n] = size(x);
    label = [];
    d = pdist2(x_in,x);
    for i = 1:p
        count = 0;
        d_cur = d(i,:);
        d_tmp = d(i,:);
        d_cur = sort(d_cur);
        for i = 1:k
            tmp = d_tmp == d_cur(1,i);
            tmp = sum(y'.*tmp,2);
            count = count + tmp(1,1);            
        end
        if count > 0
            label = [label; 1];
        else
            label = [label;-1];
        end
    end
    y = label;  
end