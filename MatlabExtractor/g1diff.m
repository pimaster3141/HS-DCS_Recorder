function [dif] = g1diff(aDbr0, G1, tau, rho , no, k0, mua, musp)
    g1an = g1analytical(aDbr0, tau', rho , no, k0, mua, musp);
    size(G1);
    dif = sum((G1 - g1an).^2);
end