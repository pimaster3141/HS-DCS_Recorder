function [DbFit, fval] = flowFit(g1, tau, fitStop, rho, mua, mus)
    no=1.33;%Skin  %Bone 1.56;
    k0=2*pi*no/(7.85e-5); %cm
    aDbr0=1e-8;

    op=optimset('fminsearch');
    options=optimset(op,'MaxIter',5000,'MaxFunEvals',5000,'TolFun',1.000e-16,'TolX',1.000e-16,'Display','off');
    
    DbFit=nan(size(g1,1),1);
    fval=nan(size(g1,1),1);
    
    parfor ii = 1:size(g1,1)
        i0 = find(g1(ii,:)<fitStop,1)
        [DbFit(ii), fval(ii)] = fminsearch(@(x)g1diff(x,g1(ii,2:i0).',tau(2:i0),rho, no, k0, mua, mus), aDbr0, options); %fitting Db from the diff. equ.
    end
end