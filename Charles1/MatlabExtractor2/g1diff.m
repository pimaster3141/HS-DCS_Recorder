function [dif] = g1diff(aDbr0,  beta,  g2, snr, tau, rho , no, k0, mua, musp)
    g1an = g1analytical(aDbr0, tau', rho , no, k0, mua, musp);
    
    G1 = sqrt(abs((g2-1)./beta));
    G1 = G1';
    
    snr = snr.*(snr>1);
    dif = sum(((G1 - g1an).* snr' ).^2);
end