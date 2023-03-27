load('tests/module/cost.sage');

def binary_entropy(x):

    return -x*log2(x)-(1-x)*log2(1-x);

###################################################

def gauss_binomial(m,r,q):
   
    x = 1.;
    for i in range(r):
        x = x*(1.-q^(m-i*1.))/(1.-q^(1.+i));
   
    return x;

##################################

def binary_entropy(x):

    return -x*log(x*1.)/log(2.) -(1-x)*log(1-x*1.)/log(2.);

########################################


#Cost of KMP algorithm: the estimate is obtained considering the numerical optimization of the algorithm running time

def kmp_cost_numerical(n,r,ell,q):
   
   
    best_cost = 10000000000000000; #lowest running time of the algorithm

    #Parameters that optimize the attack
    best_u = -1;
    best_u1 = -1;

    #List size and number of collisions
    best_L1 = -1;
    best_L2 = -1;
    best_num_coll = -1;

    for u in range(2,r+1):


        u1 = floor((n-r+u)/2);
        u2 = n-r+u-u1;

        L1 = log2(factorial(n)/factorial(n-u1));
        L2 = log2(factorial(n)/factorial(n-u2));
        num_coll = log2(factorial(n)*factorial(n)/factorial(n-u1)/factorial(n-u2)*q^(ell*(n-r-u1-u2)) );

        cost = log2(2^L1+2^L2+2^num_coll);

        if cost < best_cost:
            best_u1 = u1;
            best_u2 = u2;
            best_cost = cost;
            best_L1 = L1;
            best_L2 = L2;
            best_num_coll = num_coll;

    return best_u1, best_u2, best_L1, best_L1, best_num_coll, best_cost;

   
#######################################

#Cost of KMP algorithm: the estimate is obtained considering the asymptotic running time

def kmp_cost_asymptotic(n,r,ell,q):

    R = 1-r/n;

    mu_val = var('mu_val');

    #the optimal value for mu is found by numerical root finding
    th_mu_val = find_root(binary_entropy(mu_val)+mu_val*log(mu_val*n/exp(1.))/log(2.)+ell*log(q*1.)/log(2.)*(R-2*mu_val),0, 1);

    th_coeff = binary_entropy(th_mu_val)+th_mu_val*log2(th_mu_val*n/exp(1.));

    return th_coeff*n;
######################################################

#Uncomment the following lines for a quick test

#n = 94;
#r = 55;
#q = 509;
#ell = 1;


#best_u1, best_u2, best_L1, best_L1, best_num_coll, best_cost = kmp_cost_numerical(n,r,ell,q);
#th_cost = kmp_cost_asymptotic(n,r,ell,q);

#print("Numerical best cost for KMP = 2^",best_cost);
#print("Asymptotic estimate = 2^",th_cost);
