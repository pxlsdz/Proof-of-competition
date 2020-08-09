%%清空环境
clc
clear

%%读取数据
T=24;
data=[];
for t=1:10 
    load 'G:\jupyter_notebook文件保存\mathorcup\问题2\all.mat'
    %训练数据和预测数据
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
	
	%%节点个数
    inputnum=3;
    hiddennum=4;
    outputnum=1;

    %选连样本输入输出数据归一化
    [inputn,inputps]=mapminmax(input_train);
    [outputn,outputps]=mapminmax(output_train);


    %构建网络
    net=newff(inputn,outputn,hiddennum);

    %% 参数初始化
    %粒子群算法中的两个参数
    c1 = 1.49445;
    c2 = 1.49445;

    mgen=50;   % 进化次数  
    sizepop=100;   %种群规模

    Vmax=1;
    Vmin=-1;
    popmax=5;
    popmin=-5;

    for i=1:sizepop
        pop(i,:)=5*rands(1,21);
        V(i,:)=rands(1,21);
        fitness(i)=fun(pop(i,:),inputnum,hiddennum,outputnum,net,inputn,outputn);
    end


    % 个体极值和群体极值
    [bestfitness bestindex]=min(fitness);
    zbest=pop(bestindex,:);   %全局最佳
    gbest=pop;    %个体最佳
    fitnessgbest=fitness;   %个体最佳适应度值
    fitnesszbest=bestfitness;   %全局最佳适应度值

    %% 迭代寻优
    for i=1:mgen
        for j=1:sizepop

            %速度更新
            V(j,:) = V(j,:) + c1*rand*(gbest(j,:) - pop(j,:)) + c2*rand*(zbest - pop(j,:));
            V(j,find(V(j,:)>Vmax))=Vmax;
            V(j,find(V(j,:)<Vmin))=Vmin;

            %种群更新
            pop(j,:)=pop(j,:)+0.2*V(j,:);
            pop(j,find(pop(j,:)>popmax))=popmax;
            pop(j,find(pop(j,:)<popmin))=popmin;

            %自适应变异
            pos=unidrnd(21);
            if rand>0.95
                pop(j,pos)=5*rands(1,1);
            end

            %适应度值
            fitness(j)=fun(pop(j,:),inputnum,hiddennum,outputnum,net,inputn,outputn);
        end

        for j=1:sizepop
            %个体最优更新
            if fitness(j) < fitnessgbest(j)
                gbest(j,:) = pop(j,:);
                fitnessgbest(j) = fitness(j);
            end

            %群体最优更新
            if fitness(j) < fitnesszbest
                zbest = pop(j,:);
                fitnesszbest = fitness(j);
            end

        end

        yy(i)=fitnesszbest;    

    end

    %% 结果分析
    plot(yy)
    title(['适应度曲线  ' '终止代数＝' num2str(mgen)]);
    xlabel('进化代数');ylabel('适应度');


    %% 把最优初始阀值权值赋予网络预测
    % %用遗传算法优化的BP网络进行值预测
    x=yy;
    w1=x(1:inputnum*hiddennum);
    B1=x(inputnum*hiddennum+1:inputnum*hiddennum+hiddennum);
    w2=x(inputnum*hiddennum+hiddennum+1:inputnum*hiddennum+hiddennum+hiddennum*outputnum);
    B2=x(inputnum*hiddennum+hiddennum+hiddennum*outputnum+1:inputnum*hiddennum+hiddennum+hiddennum*outputnum+outputnum);

    net.iw{1,1}=reshape(w1,hiddennum,inputnum);
    net.lw{2,1}=reshape(w2,outputnum,hiddennum);
    net.b{1}=reshape(B1,hiddennum,1);
    net.b{2}=B2;

    %% BP网络训练
    %网络进化参数
    net.trainParam.epochs=100;
    net.trainParam.lr=0.1;
    %net.trainParam.goal=0.00001;

    %网络训练
    [net,per2]=train(net,inputn,outputn);

    %% BP网络预测
    %数据归一化
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
