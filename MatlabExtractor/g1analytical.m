function g1=g1analytical(alpha,tau,rho, no, k0, mua, musp)

k=sqrt(3*mua*musp+6*musp*musp*k0*k0*alpha*tau);
n=no/1;
Reff=-1.44/(n*n)+0.710/n+0.668+0.00636*n;
zb=(2*(1+Reff))/(3*musp*(1-Reff));
r1=sqrt(1/(musp*musp)+rho*rho);
rb=sqrt((2*zb+1)^2/(musp*musp)+rho*rho);
G1=exp(-k*r1)/r1-exp(-k*rb)/rb;
G1_0=exp(-sqrt(3*mua*musp)*r1)/r1-exp(-sqrt(3*mua*musp)*rb)/rb;
g1=G1/G1_0;

end