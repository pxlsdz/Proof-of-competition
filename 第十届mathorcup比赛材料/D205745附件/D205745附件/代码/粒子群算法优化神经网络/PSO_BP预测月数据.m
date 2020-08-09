%%��ջ���
clc
clear

%%��ȡ����
T=24;
data=[];
for t=1:10 
    load 'G:\jupyter_notebook�ļ�����\mathorcup\����2\all.mat'
    %ѵ�����ݺ�Ԥ������
    l=1+T*(t-1);
    mid=l+20;
    r=T*t;
    l
    mid
    r
    input_train=input(l:mid,:)';
    input_test=input(mid+1:r,:)';
    output_train=output(l:mid)';
    output_test=output(mid+1:r)';
	
	%%�ڵ����
    inputnum=3;
    hiddennum=4;
    outputnum=1;

    %ѡ����������������ݹ�һ��
    [inputn,inputps]=mapminmax(input_train);
    [outputn,outputps]=mapminmax(output_train);


    %��������
    net=newff(inputn,outputn,hiddennum);

    %% ������ʼ��
    %����Ⱥ�㷨�е���������
    c1 = 1.49445;
    c2 = 1.49445;

    mgen=50;   % ��������  
    sizepop=100;   %��Ⱥ��ģ

    Vmax=1;
    Vmin=-1;
    popmax=5;
    popmin=-5;

    for i=1:sizepop
        pop(i,:)=5*rands(1,21);
        V(i,:)=rands(1,21);
        fitness(i)=fun(pop(i,:),inputnum,hiddennum,outputnum,net,inputn,outputn);
    end


    % ���弫ֵ��Ⱥ�弫ֵ
    [bestfitness bestindex]=min(fitness);
    zbest=pop(bestindex,:);   %ȫ�����
    gbest=pop;    %�������
    fitnessgbest=fitness;   %���������Ӧ��ֵ
    fitnesszbest=bestfitness;   %ȫ�������Ӧ��ֵ

    %% ����Ѱ��
    for i=1:mgen
        for j=1:sizepop

            %�ٶȸ���
            V(j,:) = V(j,:) + c1*rand*(gbest(j,:) - pop(j,:)) + c2*rand*(zbest - pop(j,:));
            V(j,find(V(j,:)>Vmax))=Vmax;
            V(j,find(V(j,:)<Vmin))=Vmin;

            %��Ⱥ����
            pop(j,:)=pop(j,:)+0.2*V(j,:);
            pop(j,find(pop(j,:)>popmax))=popmax;
            pop(j,find(pop(j,:)<popmin))=popmin;

            %����Ӧ����
            pos=unidrnd(21);
            if rand>0.95
                pop(j,pos)=5*rands(1,1);
            end

            %��Ӧ��ֵ
            fitness(j)=fun(pop(j,:),inputnum,hiddennum,outputnum,net,inputn,outputn);
        end

        for j=1:sizepop
            %�������Ÿ���
            if fitness(j) < fitnessgbest(j)
                gbest(j,:) = pop(j,:);
                fitnessgbest(j) = fitness(j);
            end

            %Ⱥ�����Ÿ���
            if fitness(j) < fitnesszbest
                zbest = pop(j,:);
                fitnesszbest = fitness(j);
            end

        end

        yy(i)=fitnesszbest;    

    end

    %% �������
    plot(yy)
    title(['��Ӧ������  ' '��ֹ������' num2str(mgen)]);
    xlabel('��������');ylabel('��Ӧ��');


    %% �����ų�ʼ��ֵȨֵ��������Ԥ��
    % %���Ŵ��㷨�Ż���BP�������ֵԤ��
    x=yy;
    w1=x(1:inputnum*hiddennum);
    B1=x(inputnum*hiddennum+1:inputnum*hiddennum+hiddennum);
    w2=x(inputnum*hiddennum+hiddennum+1:inputnum*hiddennum+hiddennum+hiddennum*outputnum);
    B2=x(inputnum*hiddennum+hiddennum+hiddennum*outputnum+1:inputnum*hiddennum+hiddennum+hiddennum*outputnum+outputnum);

    net.iw{1,1}=reshape(w1,hiddennum,inputnum);
    net.lw{2,1}=reshape(w2,outputnum,hiddennum);
    net.b{1}=reshape(B1,hiddennum,1);
    net.b{2}=B2;

    %% BP����ѵ��
    %�����������
    net.trainParam.epochs=100;
    net.trainParam.lr=0.1;
    %net.trainParam.goal=0.00001;

    %����ѵ��
    [net,per2]=train(net,inputn,outputn);

    %% BP����Ԥ��
    %���ݹ�һ��
    inputn_test=mapminmax('apply',input(l:r,:)',inputps);
    an=sim(net,inputn_test);
    test_simu=mapminmax('reverse',an,outputps);
    %error=test_simu-output_test;
    for i=1:T
        test_simu(i)=round(test_simu(i))
    end
    MAPE=0;
    for i=22:T
        test_simu(i)=round(test_simu(i))
        MAPE=MAPE+(abs(test_simu(i)-output_test(i-21)))/output_test(i-21);
    end 
    
    data=[data;output_train,output_test,0;test_simu,MAPE]
    MAPE=MAPE/3;
    break;
end
