function [tauList, g2, vap] = MatlabDCSCorrelator(path, fs, fsout, bandwidth, chunkSizeMax)
       
    % constant calculations
    integration = 1/bandwidth;
    SAMPLE_WINDOW = fs * integration;
    SAMPLE_SHIFT = round(fs/fsout);
    NUM_CHUNKS = floor((chunkSizeMax-SAMPLE_WINDOW)/SAMPLE_SHIFT) + 1;
    CHUNK_SIZE = (NUM_CHUNKS - 1)* SAMPLE_SHIFT + SAMPLE_WINDOW;
    OVERLAP_SIZE = CHUNK_SIZE - NUM_CHUNKS*SAMPLE_SHIFT;

    % read in data
    f = fopen(path);
    data = fread(f, CHUNK_SIZE, 'uint16=>uint16');
    
    %start paralell process
%     parpool('local');
    
    %define global structures
    vap = [];
    g2 = [];
    lastChannelData = [0, 0, 0, 0]; %such that diff() returns same number
    cast(lastChannelData, 'uint16');
    overlapData = zeros(OVERLAP_SIZE, 4, 'int8'); %oversample overlap
    
    
    
    
    %initialize global structures
    
%     vapChunk = zeros(CHUNK_SIZE, 4);
%     vapChunk(:, 1) = bitand(data, hex2dec('4000'));
%     vapChunk(:, 2) = bitand(data, hex2dec('8000'));
%     vapChunk(:, 3) = bitand(data, hex2dec('0040'));
%     vapChunk(:, 4) = bitand(data, hex2dec('0080'));
%     vap = [vap; vapChunk];

    channelChunk = zeros(CHUNK_SIZE, 4, 'uint16');
%     channelChunk(1, :) = lastChannelData;
    channelChunk(1:end, 1) = bitshift(bitand(data, hex2dec('0700')), -8);
    channelChunk(1:end, 2) = bitshift(bitand(data, hex2dec('3800')), -11);
    channelChunk(1:end, 3) = bitshift(bitand(data, hex2dec('0007')), 0);
    channelChunk(1:end, 4) = bitshift(bitand(data, hex2dec('0038')), -3);
    lastChannelData = channelChunk(end, :);

    channelChunk = cast(channelChunk, 'int8');
    channelChunk = diff(channelChunk);
    channelChunk = bitand(channelChunk, hex2dec('0007'));
    
    overlapData(:, 4) = channelChunk(end-(OVERLAP_SIZE-1):end, 4);
    
    
    data = fread(f, CHUNK_SIZE - OVERLAP_SIZE, 'uint16=>uint16');
    channelChunk = zeros(CHUNK_SIZE-OVERLAP_SIZE+1, 4, 'uint16');
    
    while(length(data) > 0)
%         vapChunk = zeros(CHUNK_SIZE, 4);
%         vapChunk(:, 1) = bitand(data, hex2dec('4000'));
%         vapChunk(:, 2) = bitand(data, hex2dec('8000'));
%         vapChunk(:, 3) = bitand(data, hex2dec('0040'));
%         vapChunk(:, 4) = bitand(data, hex2dec('0080'));
%         vap = [vap; vapChunk];
        
        % extract raw counts
        channelChunk(1, :) = lastChannelData;
        channelChunk(2:end, 1) = bitshift(bitand(data, hex2dec('0700')), -8);
        channelChunk(2:end, 2) = bitshift(bitand(data, hex2dec('3800')), -11);
        channelChunk(2:end, 3) = bitshift(bitand(data, hex2dec('0007')), 0);
        channelChunk(2:end, 4) = bitshift(bitand(data, hex2dec('0038')), -3);
        lastChannelData(1, :) = channelChunk(end, :);
        
        % flag photon events 
        channelChunk = cast(channelChunk, 'int8');
        channelChunk = diff(channelChunk);
        channelChunk = bitand(channelChunk, hex2dec('0007'));
        
        
        overlapData(:, 4) = channelChunk(end-(OVERLAP_SIZE-1):end, 4);
        
        for channel = 1:4
            channelData = convmtx(channelChunk(:, channel), SAMPLE_WINDOW);
            channelData = channelData(:, SAMPLE_WINDOW:end-SAMPLE_WINDOW+1);
            channelData = channelData(:, 1:SAMPLE_SHIFT:end);
            channelData = flipud(channelData);
%             channelData = channelData'
            
            numG2 = size(channelData, 2);
            intensity = mean(channelData, 1);
            g2T = zeros(SAMPLE_WINDOW - 1, numG2);
            
            parfor i = 1:numG2
                [r, lags] = xcorr(channelData(:, i), 'unbiased');
                r = r./intensity(i);
                g2T(:, i) = r(end-floor(length(r)/2)+1:end);
            end
            
            g2 = [g2 g2T];
            
        end
            
            
            
       
        
        
        tauList = lags;
        data = fread(f, CHUNK_SIZE-OVERLAP_SIZE, 'uint16=>uint16');
    end

end