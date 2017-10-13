clc
data=importdata('perceptron.data');
label = data(:,5:5);
x = data(:,1:4);
w = [0 0 0 0];
b = 0;
m = size(label);
step = 1;
k = 0;
for k=1:100
    dw = [0 0 0 0];
    db = 0;
    y = zeros(m);
    error = zeros(m);
    for j=1:m
        y(j) = 0;
        for i=1:4
            y(j) = y(j) + w(i)*x(j,i);
        end
        y(j) = y(j) + b;
        error(j) = -y(j)*label(j);
    end
    for j=1:m
        if error(j) >= 0
            e = [0 0 0 0];
            for i=1:4
                e(i) = (label(j)*x(j,i));
            end
            dw = dw - e;
            db = db - label(j);
        end
    end
    tempw = w - step.*dw;
    tempb = b - step*db;
    eqw = isequal(w, tempw);
    eqb = b == tempb;
    if eqw && eqb
        %prints the iteration at which function converged
        k
        break;
    end
    w = tempw;
    b = tempb;
end
figure
plot(y);