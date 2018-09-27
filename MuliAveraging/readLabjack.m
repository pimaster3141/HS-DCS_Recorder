function [data, time] = readLabjack(folder,N,filename)
%% read in a cascade of labjack files
% folder includes folder name to directory including data files
% Data files need to be of following format "data_n.dat", where n is
% element of N.
%
% N is a vector containing all data files that will be concatinated 
% 
% example: [data,time] = redLabjack('subj0\labjack\labjack.cfg\',2:6,'data_')

%% error handling
if nargin == 2
    filename = [];
elseif nargin == 1
    N = [];
    filename = [];
elseif nargin == 0
    N = [];
    filename = [];
    folder = [];
end
        
if isempty(filename)
    filename = 'data_';
end
if isempty(N)
    N=1;
end
if isempty(folder)
    folder = '';
end

%% load data
data={};
subfile = strtrim(cellstr(num2str(N'))');
ext = '.dat';
for m = 1:length(N)
    temp = dlmread([folder filename subfile{m} ext],'',8,0);
    data{m} = temp(:,2:end);
    time{m} = temp(:,1);
end

%% concatinate data files
data = cat(1,data{:});
time = cat(1,time{:});
time = time - time(1);