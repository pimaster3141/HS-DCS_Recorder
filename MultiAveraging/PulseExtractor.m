location = 'D:\Users\jason\DataDumps\DCS\ProcessedData\HeadTilt\';
file = 'flat50Hz';

load([location file]);

pulses = findRisingEdges(vap(:, 4), 0.1);

diffpulses = diff(pulses);
[M, I] = max(diffpulses);
pulses = pulses(I+1:end);

segments = extractSegments(dbfit, pulses, 100, 300);

for ii = 1:size(segments, 1)
    data = segments(ii, :, :);
    data = data ./ nanmean(data) * 100;
    
    segments(ii, :, :) = data;
end

segments = filterSTD(segments, 1);

% for ch = 1:4
%     for ii = 1:size(segments, 1)
%         data = segments(ii, :, ch);
%         data = smooth(data, 5);
% 
%         segments(ii, :, ch) = data;
%     end
% end

