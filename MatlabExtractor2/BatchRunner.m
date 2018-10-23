tic;
% [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt16-10-2018\flat_initialProcessed', 2E6, 2);
% save('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt16-10-2018\flat_initial', '-v7.3');
% clear all;
[tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt16-10-2018\down_20Processed', 2E6, 2);
save('D:\Users\jason\DataDumps\DCS\Processed_Data\HeadTilt16-10-2018\down_20', '-v7.3');
clear all;
[tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt16-10-2018\down_40Processed', 2E6, 2);
save('D:\Users\jason\DataDumps\DCS\Processed_Data\HeadTilt16-10-2018\down_40', '-v7.3');
clear all;
[tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt16-10-2018\uptiltProcessed', 2E6, 2);
save('D:\Users\jason\DataDumps\DCS\Processed_Data\HeadTilt16-10-2018\uptilt', '-v7.3');
clear all;
toc

% 
% [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\M13\M13_Rotation6Processed', 2E6, 2);
% save('D:\Users\jason\DataDumps\DCS\ProcessedData\M13\M13_Rotation6', '-v7.3');
% clear all;
% [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\M13\M13_Rotation7Processed', 2E6, 2);
% save('D:\Users\jason\DataDumps\DCS\ProcessedData\M13\M13_Rotation7', '-v7.3');
% 
% 
% clear all;
% [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\M13\M13_ExsProcessed', 2E6, 2);
% save('D:\Users\jason\DataDumps\DCS\ProcessedData\M13\M13_Exs', '-v7.3');
% 
% clear all;
% [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\M13\M13_Rotation1Processed', 2E6, 2);
% save('D:\Users\jason\DataDumps\DCS\ProcessedData\M13\M13_Rotation1', '-v7.3');
% clear all;
% [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\M13\M13_Rotation2Processed', 2E6, 2);
% save('D:\Users\jason\DataDumps\DCS\ProcessedData\M13\M13_Rotation2', '-v7.3');
% clear all;
% [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\M13\M13_Rotation3Processed', 2E6, 2);
% save('D:\Users\jason\DataDumps\DCS\ProcessedData\M13\M13_Rotation3', '-v7.3');
% clear all;
% 
% [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\M13\M13_Rotation4Processed', 2E6, 2);
% save('D:\Users\jason\DataDumps\DCS\ProcessedData\M13\M13_Rotation4', '-v7.3');
% clear all;
% [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\M13\M13_Rotation5Processed', 2E6, 2);
% save('D:\Users\jason\DataDumps\DCS\ProcessedData\M13\M13_Rotation5', '-v7.3');
% clear all;


