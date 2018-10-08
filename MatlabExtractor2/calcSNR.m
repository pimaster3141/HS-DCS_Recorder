function sigNoise = calcSNR(g2)

    dlength = size(g2, 1);
    sigNoise = zeros(size(g2));
    for ii = 1:dlength
        sigNoise(ii, :) = (mean(g2(max(1, ii-49):min(dlength, ii+50), :), 1) - 1)./std(g2(max(1, ii-49):min(dlength, ii+50), :), 1);
    end
end