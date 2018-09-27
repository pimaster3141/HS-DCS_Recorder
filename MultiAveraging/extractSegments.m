function segments = extractSegments(trace, indexPositions, preWindow, postWindow)
    segments = NaN(length(indexPositions), 1+preWindow+postWindow, size(trace, 2));
    trace = [NaN(preWindow, size(trace, 2)); trace; NaN(postWindow, size(trace, 2))];
    indexPositions = indexPositions + preWindow;
    
    
    for ii = 1:length(indexPositions)
        data = trace(indexPositions(ii)-preWindow : indexPositions(ii)+postWindow, :);

%         data = data - nanmean(data);
%         data = data ./ nanmean(data) * 100;
        
        segments(ii, :, :) = data;
    end
        
    
end
