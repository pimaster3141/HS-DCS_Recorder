function [DbFit, fval] = calcFlow(G2, rho, i0, mua, mus)
%,allana,allG1
%% function [DbFit, fval] = calcFlow(G2, rho, i0, mua, mus)
% 
% 
%
% --------------------------------------------------------------------

switch nargin
    case 0
        error('not enough input arguments')
    case 1
        rho = []; %[cm]
        i0 = [];
        mua = []; %[cm^-1]
        mus = []; %[cm^-1]
    case 2
        i0 = [];
        mua = []; %[cm^-1]
        mus = []; %[cm^-1]
    case 3
        mua = []; %[cm^-1]
        mus = []; %[cm^-1]
    case 4
        mus = []; %[cm^-1]
end
        
%%     
FIRSTDELAY = .5e-6; %1e-7;

no=1.33;%Skin  %Bone 1.56;
k0=2*pi*no/(7.85e-5); %cm
aDbr0=1e-8;

op=optimset('fminsearch');
options=optimset(op,'MaxIter',5000,'MaxFunEvals',5000,'TolFun',1.000e-16,'TolX',1.000e-16,'Display','off');



DelayTime = (1:16)*FIRSTDELAY;
for j = 1:30
    for i = 1:8
        DelayTime(i + (j - 1) * 8 + 16) = DelayTime((j - 1) * 8 + 16 + i - 1) + FIRSTDELAY*2^j;
    end
end

numPoints = 256;
fs = 2E6;

integrationSize = fs*1E-1;
stepSize = fs*1E-2;

tauListN = logspace(0, log10(integrationSize), numPoints);
tauListN = floor(tauListN);
tauListN = unique(tauListN);
tauList = tauListN ./ fs;


DelayTime = tauList;

% i0vec = find(DelayTime>= cutoff);
% i0=i0vec(1);
startpoint=6;%6

%% set default parameters 
    
if isempty(rho)
    rho = 2; %[cm]
end

if isempty(mua)
    mua = 0.1; %[cm^-1]
end

if isempty(mus)
    mus = 10; %[cm^-1]
end

if isempty(i0) %only fit to g1 = 0.7
%     SNR = DCSSNR(G2);
%     [~,i0] = min(SNR>2);
%     i0 = ceil(i0/8)*8;
%     G2temp1 = mean(G2,3);
    G2temp1 = G2;
    G2temp = G2temp1(startpoint:startpoint+2,:);
    beta   = mean(G2temp()-1);
    G1     = sqrt(abs(G2temp1()-1)./beta);
%     g1an = g1analytical(aDbr0, DelayTime, rho , no, k0, mua, mus);
%     ssd = sum((G1' - g1an).^2);
%     if ssd >= 1.25
        i0 = find(G1<0.7,1);
%     end
end



% tau = DelayTime(1:i0);2

%% mean of corrlation
DbFit=nan(size(G2,2),1);
fval=nan(size(G2,2),1);
% G2 = mean(G2,3);
% allana=nan(length(startpoint:256),size(G2,2));
parfor t=1:size(G2,2)
    
    G2temp = G2(startpoint:startpoint+2,t);
    beta   = mean(G2temp(:)-1);
    G1     = sqrt(abs(squeeze(G2(startpoint:i0,t)-1)./beta));
%     g1an = g1analytical(aDbr0, DelayTime(startpoint:i0), rho , no, k0, mua, mus);
    [DbFit(t),fval(t)] = fminsearch(@(x)g1diff(x,G1,DelayTime(startpoint:i0),rho, no, k0, mua, mus), aDbr0, options); %fitting Db from the diff. equ.
%     allana(:,t) = g1analytical(DbFit(t), DelayTime(startpoint:end), rho , no, k0, mua, mus);
%     allG1(:,t) = sqrt(abs(squeeze(G2(startpoint:end,t)-1)./beta));
end
% DbFit = (DbFit)/DbFit(1)*100;

%% mean of flow
% DbFit=nan(size(G2,2),size(G2,3));
% fval=nan(size(G2,2),size(G2,3));
% for chl = 1:size(G2,3)
%     for t=1:size(G2,2)
%         G2temp = G2(startpoint:startpoint+2,t,chl);
%         beta   = mean(G2temp(:)-1);
%         G1     = sqrt(abs(squeeze(G2(startpoint:i0,t,chl)-1)./beta));
%     %     g1an   = g1analytical(aDbr0, tau(startpoint:end), rho);
%         [DbFit(t,chl),fval(t,chl)] = fminsearch(@(x)g1diff(x,G1,DelayTime(startpoint:i0),rho, no, k0, mua, mus), aDbr0, options); %fitting Db from the diff. equ.
%     end
% end
% DbFit = mean(DbFit,2);
% 
% DbFit = (DbFit)./DbFit(1)*100;
end

