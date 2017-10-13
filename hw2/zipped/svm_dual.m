data = load('wdbc_train.data');
x = data(:,2:11);
y = data(:,1);
[m n] = size(x);
f = -1.*ones(m,1);
beq = 0; 
Aeq = y';
lb = zeros(m,1);
c = [1,10,100,1000,10000,100000,1000000,10000000,100000000];
sigma = [0.1,1,10,100,1000];
lambda = [];
d = [];
for i = 1:9
    ub = c(1,i).*ones(m,1);
    for j = 1:5
        H = guass(x,y,sigma(1,j));
        val = quadprog(H,f,[],[],Aeq,beq,lb,ub);
        lambda = [lambda val];
    end
end
for i=1:9
    for j = 1:5
        k = (i-1)*5 + j;
        d =[d y - gW(lambda(:,k),x,y,x,0,sigma(1,j))];
    end
end

for i = 1:9
    for j = 1:5
        k = (i-1)*5 + j;
        y_out = gW(lambda(:,k),x,y,x,d(1,k),sigma(1,j));
        result = accur(y,y_out);
        dispString = ["Accuracy with train_data: ", num2str(result*100)];
        disp(dispString);
    end
end

vData = load('wdbc_valid.data');
max_e = 0;
max_sigma = 0;
m = 0;
xV = vData(:,2:11);
yV = vData(:,1);
for i = 1:9
    for j = 1:5
        k = (i-1)*5+j;
        y_out = gW(lambda(:,k),x,y,xV,d(1,k),sigma(1,j));
        acc = accur(yV,y_out);
        dispString = ["Accuracy with validData: ", num2str(acc*100)];
        disp(dispString);
        if acc > m
            m = acc;
            max_e = i;
            max_sigma = j;
        end
    end  
end

tData = load('wdbc_test.data');
yT = tData(:,1);
xT = tData(:,2:11);
index = (max_e-1)*5 + max_sigma;
yTest = gW(lambda(:,index),x,y,xT,d(1,index),sigma(1,max_sigma));
result = accur(yT,yTest);
dispString = ["Accuracy with test data: ", num2str(result*100)];
disp(dispString);

function y = accur(label,pY)
    correct = 0;
    [m n] = size(label);  
    for i=1:m
        if label(i,1)*pY(i,1) > 0
            correct = correct+1;
        end
    end   
    y = correct/m;
end

function H = guass(x,y,sigma)
    mod_x = sum(x.*x,2);
    X = x*x';    
    [m n] = size(x);
    tmp1 = mod_x.*ones(m,m);
    tmp2 = mod_x'.*ones(m,m);
    K = 2.*X - tmp1 - tmp2;    
    K = exp(1/(2*sigma.^2).*K);    
    Y = y*y';
    H = Y.*K;   
end

function wx = gW(lambda,x,y,x_in,b,sigma)
    [m n] = size(x);   
    [M N] = size(x_in); 
    tmp = [];
    for i = 1:M
        X = x_in(i,:);
        X = X.*ones(m,n) - x;
        X = exp(-1/(2*sigma.^2).*sum(X.*X,2));
        tmp = [tmp;sum(lambda.*y.*X)+b];
    end    
    wx = tmp;   
end