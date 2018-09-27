function segments = extractSegments(trace, indexPositions, preWindow, postWindow)
    segments = NaN(length(indexPositions), 1+preWindow+postWindow, size(trace, 2));
    trace = [NaN(preWindow, size(trace, 2)); trace; NaN(postWindow, size(trace, 2))];
    indexPositions = indexPositions + preWindow;
    
    
    for ii = 1:length(indexPositions)
        data = trace(indexPositions(ii)-preWindow : indexPositions(ii)+postWindow, :);

        data = data - nanmean(data);
        
        segments(ii, :, :) = data;
    end
    
    % -------------- exclude data > mean + std------------------------ % 
    n = 2;
    stdlimit = nanstd(segments,[], 1);
    meanlimit = nanmean(segments, 1);
    limit = n*stdlimit + meanlimit;
        
    badPoints = segments > limit;
    segmentsNew = segments;
    segmentsNew(badPoints) = nan;

    % You have to plot the right channel to see changes... It worked
    % all along, the plot was wrong.
    for chl = 1:4
        figure
%         plot(segmentsNew(:, :, chl)');
        shadedErrorBar(-preWindow:postWindow, nanmean(segmentsNew(:, :, chl)), nanstd(segmentsNew(:, :, chl)));
    end
         
    % --------------------------------------------------------------- %
        
    
end
