n_c = size(all,2);  % number of column ���ݵ�����
H = zeros(1,4);  % ��ʼ����ʡʱ�������
P = zeros(1,4);
for i = 1:n_c
    [h,p] = jbtest(all(:,i),0.05);
    H(i)=h;
    P(i)=p;
end
H
P