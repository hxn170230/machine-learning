clc;
data=importdata('perceptron.data');
label = data(:,5);
x = data(:,1:4);
w = [0 0 0 0];
b = 0;
[m,n] = size(label);
step = 1;
k = 0;
for k=1:1000000
    dw = [0 0 0 0];
    db = 0;
    y = 0;
    j = mod(k,m);
    if j == 0
        j = j + 1;
    end
    for i=1:4
        y = y + w(i)*x(j,i);
    end
    y = y + b;
    error = -y*label(j);
    if error >= 0
        e = [0 0 0 0];
        for i=1:4
            e(i) = (label(j)*x(j,i));
        end
        dw = dw - e;
        db = db - label(j);
    end
    tempw = w - step.*dw;
    tempb = b - step*db;
    eqw = isequal(w, tempw);
    eqb = b == tempb;
    if eqw && eqb
        %prints the iteration at which function converged
        tempk
     %   break;
    else
        tempk = k;
    end
    w = tempw
    b = tempb
end
%plot the values
yaxis = zeros(m);
for k=1:1000
    yaxis(k) = 0;
    for i=1:4
        yaxis(k) = yaxis(k) + w(i)*x(k,i);
    end
    yaxis(k) = yaxis(k) + b;
end
figure
plot(yaxis);
