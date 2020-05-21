close all;
clear all;
clc;

warning('off','all');
%change dSet name to your 
dSet = 'ReplaceWithExcelName';
ext = '.xlsx';
%use ext as .xlsx for your excel files
dName = strcat(dSet,ext);
acn = readcell(dName);
%acn = importdata(dName);

path = pwd;
nPath = strcat(path,'\',dSet);
if ~exist(nPath, 'dir')
    mkdir(nPath)
end
cd(nPath);
%need R2019 version of MATLAB

%if your script fails during running because it times out, look to the
%right in the workspace to see where 1 stopped, to continue where you left
%off in the line below, 'for i=1:length(acn)', change the 1 to the number
%it stopped e.g. if it stopped at 134, the script should be changed to 'for
%i=134:length(acn) and rerun the script
for i=1:length(acn)
    fnm = strcat(num2str(i),'.fasta');
    fnm = regexprep(acn{i},'[^A-Z,^0-9]','','ignorecase');
    fnm = strcat(fnm,'.fasta');
    try
        sq = getgenbank(acn{i},'FileFormat', 'fasta');        
        fastawrite(fnm, sq);
    catch
        try
            sq = getmissinggenbankfasta(acn{i},'test.txt');
            fastawrite(fnm, sq);
        catch
            sq = getWGS(acn{i});
            fastawrite(fnm, sq);
        end
    end
end

cd(path);

%can remove this but this sound only goes off when the script is fully
%complete
sound(sin(1:3000))