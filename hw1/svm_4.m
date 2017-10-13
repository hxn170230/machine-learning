data=importdata('mystery.data');
x=data(:,:);
x(:,5) = 1;
label=data(:,5:5);
H=eye(5,5);
H(5,5) = 0;
B=ones(1,1000);
for i=1:1000
    B(1, i) = -1;
end
w = quadprog(H,zeros(1,5),-1.*label.*x,B);