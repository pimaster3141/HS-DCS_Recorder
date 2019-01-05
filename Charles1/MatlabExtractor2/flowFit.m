function [fits, fval] = flowFit(g2, snr, tau, rho, mua, mus)
    no=1.33;%Skin  %Bone 1.56;
    k0=2*pi*no/(8.48e-5); %cm
    aDbr0=0.5e-8;
    betaScale = 1E-8;
    
    DIVISION_LIMIT = 200000;

%     op=optimset('fminsearch');
%     options=optimset(op,'MaxIter',5000,'MaxFunEvals',5000,'TolFun',1.000e-16,'TolX',1.000e-16,'Display','off');
    
    options = optimoptions('fmincon'...
    , 'ConstraintTolerance', 1e-20...
    , 'DiffMaxChange', 1E-10...
    , 'Display', 'off'...
    , 'MaxFunctionEvaluations', 5000 ...
    , 'MaxIterations', 5000 ...
    , 'OptimalityTolerance', 1E-20 ...
    );

    fits=nan(size(g2,1),2);
    fval=nan(size(g2,1),1);
    
    x0 = [aDbr0, 0.5*betaScale];
    A = [];
    b = [];
    Aeq = [];
    beq = [];
    lb = [0, 0.01*betaScale];
    ub = [1e-6, .8*betaScale]; % change for HF-DCS;
   
    if(size(g2, 1) > DIVISION_LIMIT)
        disp("dividing inputs");
        parfor ii = 1:DIVISION_LIMIT
            fun = @(x) (g1diff(x(1), x(2)./betaScale, g2(ii,:), snr(ii,:), tau(1,:), rho , no, k0, mua, mus));
            [fits(ii,:), fval(ii)] = fmincon(fun, x0, A, b, Aeq, beq, lb, ub, [], options);
        end
        
        parfor ii = DIVISION_LIMIT+1 : size(g2, 1)  
            fun = @(x) (g1diff(x(1), x(2)./betaScale, g2(ii,:), snr(ii,:), tau(1,:), rho , no, k0, mua, mus));
            [fits(ii,:), fval(ii)] = fmincon(fun, x0, A, b, Aeq, beq, lb, ub, [], options);
        end
        
        
    else   
        parfor ii = 1:size(g2,1)
            fun = @(x) (g1diff(x(1), x(2)./betaScale, g2(ii,:), snr(ii,:), tau(1,:), rho , no, k0, mua, mus));
            [fits(ii,:), fval(ii)] = fmincon(fun, x0, A, b, Aeq, beq, lb, ub, [], options);
        end
    end
    
    fits(:, 2) = fits(:,2)./betaScale;
end