data = load('wdbc_train.data');
x = data(:,2:11);
y = data(:,1);
[m n] = size(x);
H = diag([ones(1,n) 0 zeros(1,m)]);
b = ones(m,1); 
A = [-1.*y.*x -1.*y.*b -1*eye(m)];
ub = [inf*ones(n,1);  inf ; inf*ones(m,1)];
lb = [-inf*ones(n,1); -inf ; zeros(m,1)];
c = 1;
w = [];
d = [];

for i = 1:9
    f = [zeros(n,1); 0 ; c.*ones(m,1)];
    val = quadprog(H,f,A,-1.*b,[],[],lb,ub);
    localW = val(1:10);
    localD = val(11);
    label = sum(localW'.*x,2) + localD;
    result = findAccuracy(y,label);
    dispString = ["findAccuracy TrainData: ", num2str(result*100), " at C = ", num2str(c)];
    disp(dispString);
    w = [w val(1:10)];
    d = [d val(11)];
    c = c*10;
end

vData = load('wdbc_valid.data');
index = 0;
m = 0;
vX = vData(:,2:11);
vY = vData(:,1);
c = 1;
for i=1:9
    label = sum(w(:,i)'.*vX,2) + d(i);
    acc = findAccuracy(vY,label);
    if acc > m
        m = acc;
        index = i;
    end
    dispString = ["findAccuracy ValidData: ", num2str(acc*100), " at: ", num2str(c*(10^i))];
    disp(dispString);
end
dispString = ["MAX findAccuracy ValidData: ", num2str(m*100), " at: ", num2str(c*10^index)];
disp(dispString);

tData = load('wdbc_test.data');
yT = tData(:,1);
xT = tData(:,2:11);

lTest = sum(w(:,index)'.*xT,2) + d(index);

result = findAccuracy(yT,lTest)*100;
dispString = ["findAccuracy TestData: ", num2str(result)];
disp(dispString);


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


    
