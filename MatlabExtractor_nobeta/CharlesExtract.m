function [tauList, g2, vap, g1, beta, count, dbfit, fval] = CharlesExtract(path, fs, fitLimit)
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
    g1 = zeros(size(g2));
    beta = zeros(dataLength, 4);
    count = zeros(dataLength, 4);
    
    for ii = 1:4
        [g1i, betai, counti] = g1Converter(g2(:, :, ii), fs);
        g1(:,:,ii) = g1i;
        beta(:,ii) = betai;
        count(:,ii) = counti;
    end
    
    
    dbfit = zeros(dataLength, 4);
    fval = zeros(dataLength, 4);
    
    for ii = 1:4
        [dbfiti, fvali] = flowFit(g1(:,:,ii), tauList, fitLimit, 2.5, 0.1, 10);
        dbfit(:,ii) = dbfiti;
        fval(:, ii) = fvali;
    end
    
end