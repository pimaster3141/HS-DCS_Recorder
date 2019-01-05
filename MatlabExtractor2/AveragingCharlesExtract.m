function [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = AveragingCharlesExtract(path, fs, rho, avgChannels)
    disp("extracting: " + path);
    g20 = csvread(strcat(path, '\G2channel0'));
    g21 = csvread(strcat(path, '\G2channel1'));
    g22 = csvread(strcat(path, '\G2channel2'));
    g23 = csvread(strcat(path, '\G2channel3'));
    g2r = cat(3, g20, g21, g22, g23);
%     g2 = permute(g2, [3,1,2]);
    
    tauList = csvread(strcat(path, '\TAU'));
    
    vap0 = fread(fopen(strcat(path, '\VAPchannel0')), 'uint8=>uint8');
    vap1 = fread(fopen(strcat(path, '\VAPchannel1')), 'uint8=>uint8');
    vap2 = fread(fopen(strcat(path, '\VAPchannel2')), 'uint8=>uint8');
    vap3 = fread(fopen(strcat(path, '\VAPchannel3')), 'uint8=>uint8');
    vap = cat(2, vap0, vap1, vap2, vap3);
%     vap = permute(vap, [2,1]);
    
    g2 = NaN(size(g2r, 1), size(g2r, 2), size(avgChannels,1));
    
    disp("Averaging Channels");
    parfor ii = 1:size(avgChannels,1)
        g2(:, :, ii) = mean(g2r(:, :, avgChannels(ii,1):avgChannels(ii,2)), 3);
    end


    dataLength = size(g20, 1);
    sigNoise = zeros(size(g2));
    
    
    
    disp("Calculating SNR");
    for ii = 1:size(avgChannels, 1)
        sigNoise(:,:, ii) = calcSNR(g2(:,:,ii));
    end
    
    
    
    dbfit = zeros(dataLength, size(avgChannels, 1));
    beta = zeros(dataLength, size(avgChannels, 1));
    fval = zeros(dataLength, size(avgChannels, 1));
    
    for ii = 1:size(avgChannels, 1)
        disp("Fitting Channel: " + ii);
        [dbfiti, fvali] = flowFit(g2(:,2:end,ii), sigNoise(:,2:end, ii), tauList(2:end), rho, 0.1, 10);
        dbfit(:, ii) = dbfiti(:,1);
        beta(:, ii) = dbfiti(:,2);
        fval(:, ii) = fvali;
    end
    
    count = fs./g2(:,1,:);
    count = squeeze(count);
    
    disp("Done"); 
end