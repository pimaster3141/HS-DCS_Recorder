function [out, betas, count] = g1Converter(g2, fs)

    betaIntegration=linspace(2,5,4);

    count = zeros(size(g2,1), 1);
    betas = zeros(size(g2,1), 1);
    out = zeros(size(g2,1), size(g2,2));
    
    for ii = 1:size(g2,1)
        betas(ii) = mean(g2(ii, betaIntegration))-1;
    end
    
    parfor ii = 1:size(g2,1)
%         betas(ii) = mean(g2(ii, betaIntegration))-1;
        count(ii) = fs/g2(ii,1);
        out(ii,:) = sqrt(abs(g2(ii,:)-1)./mean(betas));
    end
end
    