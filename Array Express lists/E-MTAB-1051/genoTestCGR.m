close all;
clear all;
clc;

tStr = strcat('SNPdata','.mat');
if ~isempty(dir(tStr))
    load(tStr);
else
    % read data
    fprintf('Reading data .... \n');
    A = readtable('calls.csv','ReadVariableNames',false);
    [r,c] = size(A);
    totalSeq = c-1;
    AcNmb = table2cell(A(1,2:c));
    nmValSeq = cell(1,totalSeq);
    labelSeq = cell(1,totalSeq);

    fprintf('Cleaning data .... \n');
    seqTable = A(2:r,2:c);
    seqCell = table2cell(seqTable);
    idx = strncmpi(seqCell,'-1',2);
    seqCell(idx) = {'3'};

   for i=1:totalSeq  %what???
       sc = seqCell(:,i);
       sc = sc.';
       nms = str2double(sc);
   %    nms(nms==3) = -1;
       nmValSeq{i} = nms;
    end

    %num to ACGT
    nmValSH = cell(1,totalSeq);
    for i=1:totalSeq
        nms = nmValSeq{i};
      %  nms(nms==-1) = 3;
        nm2 = string(nms);
        nm22 = regexprep([nm2{:}],'\s+','');
        nmValSH{i} = regexprep(nm22,{'6','7','8','11'},{'T','C','A','G'});
    end

    % rearrange data as per clusters
    fprintf('Finding data labels.... \n');
    B = readtable('E-MTAB-1051-labels.csv','ReadVariableNames',false);
    [r2,c2] = size(B);
    tabHeaders = table2cell(B(1,1:c2));
    anListIdx = find(strcmp(tabHeaders, 'Source Name'));
    anList = table2cell(B(2:r2,anListIdx));
    labelListIdx = find(strcmp(tabHeaders, 'Characteristics-OrganismPart'));
    labelList = table2cell(B(2:r2,labelListIdx));

    for i=1:totalSeq
        strg = AcNmb{i};
        for j=1:length(anList)
            if(strncmpi(strg,anList{j},length(anList{j}))) %what is strncmpi
               labelSeq{i} =  labelList{j};
               break;
            end
        end
    end

    [labelSeq,sortIdx] = sort(labelSeq);
    AcNmb = AcNmb(sortIdx);
    nmValSeq = nmValSeq(sortIdx);

    [uvals, ~, uidx] = unique(labelSeq);
    output = [uvals, accumarray(uidx, 1)];

    numberOfClusters = length(output)-1;
    pointsPerCluster = output{length(output)};
    clusterNames = uvals;

    pts = cell(1,numberOfClusters);
    for i=1: numberOfClusters
        pts{i} = pointsPerCluster(i);
    end
    pointsPerCluster = pts;
end

fprintf('Computing Fourier Transform.... \n');
f=cell(1,totalSeq);
lg=cell(1,totalSeq);
nss=cell(1,totalSeq);
%imshow(imcomplement(nss{2}));
for i = 1:totalSeq
    nsNew = cgr(nmValSH{i},'ACGT',9);
    nss{i} = nsNew;
    f{i} = fft2(nsNew);
    lg{i} = abs(f{i});
end

fprintf('Computing Distance matrix .... \n');
lgl = cell(1,totalSeq);
for i=1:totalSeq
    lgl{i} =  reshape(lg{i},1,[]);
end
fm=cell2mat(lgl(:));
disMat = f_dis(fm,'cor',0,1);

%Multi-dimensional Scaling   what's going on here
fprintf('Multi-dimensional scaling .... \n');
[Y,eigvals] = cmdscale(disMat,6);

fprintf('Generating 3D plot .... \n');
selectedFolder = 'SNP dataset';
index=1;
counter=1;
Cluster = zeros(1,totalSeq);

for i=1:totalSeq
    Cluster(i)=index;
    if(counter==pointsPerCluster{index})
        index=index+1;
        counter=0;
    end
    counter= counter+1;
end
uniqueClusters  = unique(Cluster);
cmap = distinguishable_colors(numberOfClusters);
hf = figure;
hold on;
for h=1:numberOfClusters
    cIndex = Cluster == uniqueClusters(h);
    plot3(Y(cIndex,1),Y(cIndex,2),Y(cIndex,3),'.','markersize', 15, 'Color',cmap(h,:),'DisplayName',clusterNames{h});
end
view(3), axis vis3d, box on, datacursormode on
xlabel('x'), ylabel('y'), zlabel('z')
tname = strcat(selectedFolder,' (',int2str(totalSeq),' Sequences',')');
title(tname)
hdt = datacursormode(hf);
set(hdt,'UpdateFcn',{@myupdatefcn,Y,AcNmb})
legend('show');

treeLbl=cell(1,length(AcNmb));
id=1;
for i=1:numberOfClusters
    for j=1:pointsPerCluster{i}
        aid=strcat(clusterNames{i},'_',AcNmb{id});
        treeLbl{id} = regexprep(aid,'[^a-zA-Z0-9]','_');
        id=id+1;
    end
end
UPGMAtree = seqlinkage(disMat,'UPGMA',treeLbl);
phytreewrite('UPTree.tree',UPGMAtree,'Branchnames',false);

clear a;
a=[];
for i=1:numberOfClusters
    for j=1:pointsPerCluster{i}
        a=[a; i];
    end
end
ATestlg = [disMat a];
rng(15,'twister');

alabels = a;
fprintf('Performing classification .... \n');
folds=2;
if (totalSeq<folds)
    folds = totalSeq;
end
[accuracy, avg_accuracy, clNames, cMat] = classificationCode(disMat,alabels, folds, totalSeq);
acc = [accuracy avg_accuracy];
s.ClassifierModel=cellstr(clNames.');
s.Accuracy=cell2mat(acc).';
ClassificationAccuracyScores = struct2table(s)

fprintf('**** Processing completed ****\n');
