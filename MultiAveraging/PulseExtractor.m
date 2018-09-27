location = 'D:\Users\jason\DataDumps\DCS\ProcessedData\HeadTilt\';
file = 'down20Hz';

load([location file]);

pulses = findRisingEdges(vap(:, 4), 0.1);

diffpulses = diff(pulses);
[M, I] = max(diffpulses);
pulses = pulses(I+1:end);

segments = extractSegments(dbfit, pulses, 50, 150);

for ii = 1:size(segments, 1)
    data = segments(ii, :, :);
    data = data ./ nanmean(data) * 100;
    
    segments(ii, :, :) = data;
end

segments = filterSTD(segments, 2);

for ch = 1:4
    for ii = 1:size(segments, 1)
        data = segments(ii, :, ch);
        data = smooth(data, 20);

        segments(ii, :, ch) = data;
    end
end

