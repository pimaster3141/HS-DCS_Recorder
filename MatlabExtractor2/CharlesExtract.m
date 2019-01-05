function [tauList, g2, sigNoise, vap, beta, count, dbfit, fval] = CharlesExtract(path, fs, rho)
    disp("extracting: " + path);
    g20 = csvread(strcat(path, '\G2channel0'));
    g21 = csvread(strcat(path, '\G2channel1'));
    g22 = csvread(strcat(path, '\G2channel2'));
    g23 = csvread(strcat(path, '\G2channel3'));
    g2 = cat(3, g20, g21, g22, g23);
%     g2 = permute(g2, [3,1,2]);
    
    tauList = csvread(strcat(path, '\TAU'));
    
    vap0 = fread(fopen(strcat(path, '\VAPchannel0')), 'uint8=>uint8');
    vap1 = fread(fopen(strcat(path, '\VAPchannel1')), 'uint8=>uint8');
    vap2 = fread(fopen(strcat(path, '\VAPchannel2')), 'uint8=>uint8');
    vap3 = fread(fopen(strcat(path, '\VAPchannel3')), 'uint8=>uint8');
    vap = cat(2, vap0, vap1, vap2, vap3);
%     vap = permute(vap, [2,1]);
    
    dataLength = size(g20, 1);
    sigNoise = zeros(size(g2));
%     
%     
%     
%     for ii = 1:4
%         [g1i, betai, counti] = g1Converter(g2(:, :, ii), fs);
%         g1(:,:,ii) = g1i;
%         beta(:,ii) = betai;
%         count(:,ii) = counti;
%     end
    
    disp("Calculating SNR");
    for ii = 1:4
        sigNoise(:,:, ii) = calcSNR(g2(:,:,ii));
    end
    
    
    
    dbfit = zeros(dataLength, 4);
    beta = zeros(dataLength, 4);
    fval = zeros(dataLength, 4);
    
    for ii = 1:4
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