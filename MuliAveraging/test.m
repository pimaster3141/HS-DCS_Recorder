folder = 'F:\2positionDCS\therealthing\labjack\';
project = 'data_';
ext = '.dat';
N = 0:3; 
subfile = strtrim(cellstr(num2str(N'))');
fsPO = 100; 
for m = 1:length(N)
     data = dlmread([folder project subfile{m} ext],'',8,0);
     time{m} = data(:,1);
     marker{m} = data(:,2);
     intensity{m} = data(:,3);
end
