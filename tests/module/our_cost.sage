load('tests/module/cost.sage');

###################################################

def gauss_binomial(m,r,q):
   
    x = 1.;
    for i in range(r):
        x = x*(1.-q^(m-i*1.))/(1.-q^(1.+i));
   
    return x;

##################################
#Compute running time of our algorithm

def compute_new_cost(n,m,q,ell):
   

   
    best_cost = 10000000000000000; #optimal cost (i.e., minimum running time)

    #Optimal parameters
    best_d = 0;
    best_w = 0;
    best_w1 = 0;
    best_u = 0;
    best_isd = 0;
    
    for d in range(1,m+1):

        for w in range(1,n):


            N_w = binomial(n,w)*(q^d-1)^(w-d)*gauss_binomial(m,d,q)/gauss_binomial(n,d,q); #number of desired subcodes


            if N_w>1: #continue only if, on average, at least one subcode exists


                c_isd = cost_isd(q,n,m,d,w,N_w);

                for w1 in range(1,w):

                    w2 = w-w1;

                    T_K = factorial(n)/factorial(n-w1)+factorial(n)/factorial(n-w2)+factorial(n)^2*q^(-d*ell)/(factorial(n-w1)*factorial(n-w2));

                    if log2(T_K)<best_cost:

                        size_K = max(1, factorial(n)/factorial(n-w)*q^(-d*ell));


                        for u in range(1,m):



                            T_L = factorial(n)/factorial(m+w-u) + size_K + factorial(n)*q^(-ell*(u-d))/factorial(m+w-u)*size_K;

                            T_test = factorial(n-w)*q^(-(u-d)*ell)/factorial(m-u)*size_K;

                            cost = log2(2^c_isd + T_K + T_L + T_test);

                            if cost < best_cost:

                                best_cost = cost;

                                best_d = d;
                                best_w = w;
                                best_w1 = w1;
                                best_u = u;
                                best_isd = c_isd;

#                                    print("cost = ",cost);
#                                    print("T_K = ",log2(T_K),", T_L = ", log2(T_L), ", T_test = ",log2(T_test));
#                                    print("[d, w, w1, u] = ",[d,w,w1,u]);
#                                    print("-----------------------");
#    print(best_d, best_w, best_w1, best_u, best_isd, best_cost)
    return best_d, best_w, best_w1, best_u, best_isd, best_cost;

   
#######################################   
#Uncomment the following lines for a quick test

#n = 94;
#r = 55;
#q = 509;
#ell = 1;

#best_d, best_w, best_w1, best_u, best_isd, best_cost = compute_new_cost(n,r,q,ell);
#print("d = ",best_d,", w = ",best_w,", best_w1 = ",best_w1,", best_u = ",best_u,", best_isd = ",best_isd,", best_cost = ",best_cost);
