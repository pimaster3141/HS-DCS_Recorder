function segments = filterSTD(segments, numSTD)
    n = numSTD;
    stdlimit = nanstd(segments,[], 1);
    meanlimit = nanmean(segments, 1);
    limit = n*stdlimit + meanlimit;
        
    badPoints = segments > limit;
%     segmentsNew = segments;
    segments(badPoints) = nan;
end
