clc;
data=importdata('problem3.1');
x=data(:, 1:2);
label=data(:,3:3);
[m,n]=size(label);
w=[0 0];
b=0;
step=1;
for k=1:1
    dw = [0 0];
    db = 0;
    y=zeros(m);
    error=zeros(m);
   for j=1:m
      y(j)= w(1)*x(j,1) + w(2)*x(j,2) + b;
      error(j)=-y(j)*label(j);
      if error(j) >= 0
         dw(1) = dw(1)-label(j)*x(j,1);
         dw(2) = dw(2)-label(j)*x(j,2);
         db = db - label(j);
      end
   end
   w = w - step.*dw
   b = b - step*db
end