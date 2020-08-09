n_c = size(all,2);  % number of column 数据的列数
H = zeros(1,4);  % 初始化节省时间和消耗
P = zeros(1,4);
for i = 1:n_c
    [h,p] = jbtest(all(:,i),0.05);
    H(i)=h;
    P(i)=p;
end
H
P