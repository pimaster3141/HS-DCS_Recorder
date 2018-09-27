clear all;
[tauList, g2, vap, g1, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt\output\down10HzProcessed', 2E6, 0.6);
save('D:\Users\jason\DataDumps\DCS\ProcessedData\HeadTilt\OLDdown10Hz', '-v7.3');

clear all;
[tauList, g2, vap, g1, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt\output\down20HzProcessed', 2E6, 0.6);
save('D:\Users\jason\DataDumps\DCS\ProcessedData\HeadTilt\OLDdown20Hz', '-v7.3');


clear all;
[tauList, g2, vap, g1, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt\output\up10HzProcessed', 2E6, 0.6);
save('D:\Users\jason\DataDumps\DCS\ProcessedData\HeadTilt\OLDup10Hz', '-v7.3');

clear all;
[tauList, g2, vap, g1, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt\output\up20HzProcessed', 2E6, 0.6);
save('D:\Users\jason\DataDumps\DCS\ProcessedData\HeadTilt\OLDup20Hz', '-v7.3');


clear all;
[tauList, g2, vap, g1, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt\output\flat10HzProcessed', 2E6, 0.6);
save('D:\Users\jason\DataDumps\DCS\ProcessedData\HeadTilt\OLDflat10Hz', '-v7.3');

clear all;
[tauList, g2, vap, g1, beta, count, dbfit, fval] = CharlesExtract('D:\Users\jason\DataDumps\DCS\Raw_Data\HeadTilt\output\flat20HzProcessed', 2E6, 0.6);
save('D:\Users\jason\DataDumps\DCS\ProcessedData\HeadTilt\OLDflat20Hz', '-v7.3');



