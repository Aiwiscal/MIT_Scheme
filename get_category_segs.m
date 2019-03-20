function SEGs = get_category_segs( category, overlap, records, seg_length, data_path )
%根据check_nums_overlaps的计算结果切取指定类别数据;
%--------------------------------------------------------------------------
%   category:指定类别，包括'N','S','V','F,'Q';
%   overlap:指定相邻切片间的重叠长度，由函数check_nums_overlaps计算或人为指定;
%   records:目标记录集合;
%   seg_length:切片长度;
%   data_path: 数据库存放路径;
%--------------------------------------------------------------------------
%返回一二维矩阵，切片个数*切片长度
CLASS = ['N','S','V','F','Q'];
INCLUDES{1} = [1,2,3,34,11]; % 各大类所包含小类的标记代号，下同;
INCLUDES{2} = [8,4,7,9];
INCLUDES{3} = [5,10];
INCLUDES{4} = [6];
INCLUDES{5} = [13];
if isempty(find(CLASS==category, 1))
    error('Targeted class must be (char):N,S,V,F,or Q.');
end
[~,target_class_nb]=find(CLASS==category);
target_class = INCLUDES{target_class_nb};
SEGs = [];
fprintf('>  Get segs for ');fprintf(category);fprintf(' ...\n');
for na=1:length(records)
    Name=num2str(records(na));
    PATH=data_path;   
    HEADERFILE=strcat(Name, '.hea');     
    ATRFILE=strcat(Name, '.atr');     
    DATAFILE=strcat(Name, '.dat');
    SAMPLES2READ=650000;          
%%  解析数据
    fprintf(1,'\\n$> WORKING ON %s ...\n', Name);
    signalh= fullfile(PATH, HEADERFILE);   
    fid1=fopen(signalh,'r');    
    z= fgetl(fid1);             
    A= sscanf(z, '%*s %d %d %d',[1,3]); 
    nosig= A(1);    
    sfreq=A(2);     
    clear A;       
    for k=1:nosig           
        z= fgetl(fid1);
        A= sscanf(z, '%*s %d %d %d %d %d',[1,5]);
        dformat(k)= A(1);           
        gain(k)= A(2);              
        bitres(k)= A(3);           
        zerovalue(k)= A(4);         
        firstvalue(k)= A(5);       
    end
    fclose(fid1);
    clear A;
    if dformat~= [212,212], error('this script does not apply binary formats different to 212.'); end
    signald= fullfile(PATH, DATAFILE);            
    fid2=fopen(signald,'r');
    A= fread(fid2, [3, SAMPLES2READ], 'uint8')';  
    fclose(fid2);
    M2H= bitshift(A(:,2), -4);       
    M1H= bitand(A(:,2), 15);          
    PRL=bitshift(bitand(A(:,2),8),9);     
    PRR=bitshift(bitand(A(:,2),128),5);   
    M( : , 1)= bitshift(M1H,8)+ A(:,1)-PRL;
    M( : , 2)= bitshift(M2H,8)+ A(:,3)-PRR;
    if M(1,:) ~= firstvalue, error('inconsistency in the first bit values'); end
    switch nosig
    case 2
        M( : , 1)= (M( : , 1)- zerovalue(1))/gain(1);
        M( : , 2)= (M( : , 2)- zerovalue(2))/gain(2);
        TIME=(0:(SAMPLES2READ-1))/sfreq;
    case 1
        M( : , 1)= (M( : , 1)- zerovalue(1));
        M( : , 2)= (M( : , 2)- zerovalue(1));
        M=M';
        M(1)=[];
        sM=size(M);
        sM=sM(2)+1;
        M(sM)=0;
        M=M';
        M=M/gain(1);
        TIME=(0:2*(SAMPLES2READ)-1)/sfreq;
    otherwise 
        disp('Sorting algorithm for more than 2 signals not programmed yet!');
    end
    clear A M1H M2H PRR PRL;
    atrd= fullfile(PATH, ATRFILE);     
    fid3=fopen(atrd,'r');
    A= fread(fid3, [2, inf], 'uint8')';
    fclose(fid3);
    ATRTIME=[];
    ANNOT=[];
    sa=size(A);
    saa=sa(1);
    i=1;
    while i<=saa
        annoth=bitshift(A(i,2),-2);
        if annoth==59
            ANNOT=[ANNOT;bitshift(A(i+3,2),-2)];
            ATRTIME=[ATRTIME;A(i+2,1)+bitshift(A(i+2,2),8)+...
                    bitshift(A(i+1,1),16)+bitshift(A(i+1,2),24)];
            i=i+3;
        elseif annoth==60
        elseif annoth==61
        elseif annoth==62
        elseif annoth==63
            hilfe=bitshift(bitand(A(i,2),3),8)+A(i,1);
            hilfe=hilfe+mod(hilfe,2);
            i=i+hilfe/2;
        else
            ATRTIME=[ATRTIME;bitshift(bitand(A(i,2),3),8)+A(i,1)];
            ANNOT=[ANNOT;bitshift(A(i,2),-2)];
        end
       i=i+1;
    end
    ANNOT(length(ANNOT))=[];       
    ATRTIME(length(ATRTIME))=[];   
    clear A;
    ATRTIME= (cumsum(ATRTIME))/sfreq;
    ind= find(ATRTIME <= TIME(end));
    ATRTIMED= ATRTIME(ind);
    ANNOT=round(ANNOT);
    ANNOTD= ANNOT(ind);

%% 按指定切片长度和重叠长度切取片段
    s=M(:,1);
    ecg_i=s';
    R_TIME=ATRTIMED(ANNOTD==1 | ANNOTD ==2 | ANNOTD==3 | ANNOTD==34 | ANNOTD==11 |ANNOTD==8 | ANNOTD ==4 | ANNOTD==7 | ANNOTD==9 | ANNOTD==5 |ANNOTD==10| ANNOTD ==6 | ANNOTD==12 | ANNOTD==38 |  ANNOTD==13 );
    REF_ind=round(R_TIME'.* 360);
    ann=ANNOTD(ANNOTD==1 | ANNOTD ==2 | ANNOTD==3 | ANNOTD==34 | ANNOTD==11 |ANNOTD==8 | ANNOTD ==4 | ANNOTD==7 | ANNOTD==9 | ANNOTD==5 |ANNOTD==10| ANNOTD ==6 | ANNOTD==12 | ANNOTD==38 |  ANNOTD==13 );
    start_point = 1;
    end_point = start_point+seg_length-1;
    if isempty(intersect(ann,target_class))
        continue;
    end
    while end_point <= length(ecg_i)    
        label_collect_index = find(REF_ind>=start_point & REF_ind<=end_point);
        label_collect = ann(label_collect_index);
        seg_label = 1;
        if sum(label_collect) > length(label_collect)
            label_collect = label_collect(label_collect~=1);
            seg_label = mode(label_collect);
        end
       
        if ~isempty(find(target_class==seg_label,1))
            seg_t = ecg_i(start_point:end_point);
            SEGs = [SEGs;seg_t];
        end
        
        start_point = end_point+1-overlap;
        end_point = start_point+seg_length-1;
    end
    
end
end

