tic;

clear all;
source = 'D:\Users\jason\DataDumps\DCS\Raw_Data\850Stability\';
output = 'D:\Users\jason\DataDumps\DCS\Processed_Data\850Stability\';
if ~exist(output, 'dir')
   mkdir(output);
end
fileList = {...
    'debugLog31Hz'...
%     ,'palm120Hz'...
%     ,'back120Hz'...
    
    };

disp('checking files');
for ii = 1:length(fileList)
    if(~exist([source, char(fileList(ii))], 'dir'))
        disp('here');
        throw(MException('MATLAB:rmpath:DirNotFound', char([source, char(fileList(ii))])));
    end
end

fs = 2E6
rho = 2.5;
average = [1 1];

for ii = 1:length(fileList)
    [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = AveragingCharlesExtract([source, char(fileList(ii))], fs, rho, average);
    save([output, char(fileList(ii))], '-v7.3');
    % clear all;
end

toc



