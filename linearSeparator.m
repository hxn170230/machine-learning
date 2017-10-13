clc;
clear all;
data=importdata('problem2');
label=data(:,3:3);
x=data(:,1:2)
w=[0 0];
b=0;
[m,n]=size(label);

for k=1:2
    dw = [0 0];
    db = 0;
    for j=1:m
        y(j) = w(1)*(x(j,1)*sin(x(j,2))) + w(2)*(x(j,1));
        y(j) = y(j) + b;
        error(j) = -y(j)*label(j)
        if error(j) >= 0
           dw(1) = dw(1) - (label(j)*(x(j,1)*sin(x(j,2))));
           dw(2) = dw(2) - (label(j)*(x(j,1)));
           db = db - label(j);
        end
    end
    w
    dw
    w = w - dw;
    b = b - db;
end
figure
plot(y);