#reset();

def log2(x):
    return log(x*1.)/log(2.);

#####################################

def gauss_binomial(m,r,q):
    x = 1;
    for i in range(r):
        x = x*(1-q^(m-i))/(1-q^(i+1));
    
    return x;


#####################################################################

##Gilbert - Varshamov distance of a code over Fq, with length n and dimension k
##Nw is the number of codewords with weight d (not considering scalar multiples)
def gv_distance(n,k,q):
   
    d = 1;
    right_term = q^(n-k);
    left_term = 0;
    while left_term <= right_term:
        left_term += binomial(n,d)*(q-1)^d;
        d+=1;
    d = d-1;
   
    Nw = binomial(n,d)*(q-1)^(d-2)*q^(k-n+1)*1.;
   
    return d, Nw;


#############################################################
#Stern's adaptation of ISD over Fq, due to Peters
#It returns both complexity and optimal parameters
def peters_isd(n,k,q,w):

    x = floor(k/2);

    log2q=log2(q);
    mincost=10000000;
    bestp=0;
    bestl=0;
    max_p = min(w//2,floor(k/2));
    for p in range(0,max_p):
        Anum=binomial(x,p);
        Bnum=binomial(k-x,p);
        #for(l=1,floor(log(Anum)/log(q)+p*log(q-1)/log(q))+10,\
        for l in range(1,floor( log(Anum)/log(q)+p*log(q-1)/log(q))+10 +1):
            if n-k-l <= w-2*p:
                continue

           # if(q==2):
            ops=0.5*(n-k)^2*(n+k)+ ((0.5*k-p+1)+(Anum+Bnum)*(q-1)^p)*l+ q/(q-1.)*(w-2*p+1)*2*p*(1+(q-2)/(q-1.))*Anum*Bnum*(q-1)^(2*p)/q^l;
          #ops=(n-k)^2*(n+k)\
         #     + ((0.5*k-p+1)+(Anum+Bnum)*(q-1)^p)*l\
         #     + q/(q-1.)*(w-2*p+1)*2*p*(1+(q-2)/(q-1.))*\
         #       Anum*Bnum*(q-1)^(2*p)/q^l;

            prob=Anum*Bnum*binomial(n-k-l,w-2*p)/binomial(n,w);
            cost=log2(ops)+log2(log2q)-log2(prob);
            if cost<mincost:
                mincost=cost;
                bestp=p; bestl=l;

    cost=mincost;
    p=bestp;
    l=bestl;
#    print("Given q=",q,", n=",n,", k=",k,", w=",w);
#    print("parameters p=",p, " and l=",l," yield 2^",cost," bit ops");
    return cost, p, l;
####################################################################

#Cost of Leon's algorithm to solve the linear equivalence problem
def leon_cost(n,k,q):
    
    #Find optimal w
    u = 10;
    w = 2;
    while u>1:
        Nw = binomial(n,w)*(q-1)^(w-1)*(q^k-1)/(q^n-1)*1.;
        if Nw>1:
            u = round(n*(1-w/n)^Nw);
            if u>1:
                w = w+1;
        else:
            w = w+1;
    
    w = w+1;
    #consider cost of ISD 
    C_isd,p,l = peters_isd(n,k,q,w);
    cost = C_isd+log2(log(Nw));

    return cost, w, Nw*1.

#############################################################

#Optimize the cost of Beullens' algorithm with improved subcodes finding strategy 
def improved_linear_beullens(n,k,q):
    
    w_in, Nw = gv_distance(n,k,q);
    
    max_w = n-k+2;

    best_cost = 100000000000000;
    best_w = 0;
    best_L_prime = 0;
    best_w_prime = 0;
    
    for w_prime in range(w_in,max_w):
       # print(w_prime);
        Nw_prime = binomial(n,w_prime)*(q-1)^(w_prime-1)*(q^k-1)/(q^n-1);
        
        for w in range(w_prime+1,min(2*w_prime,n)):
            
            pr_w_w_prime = binomial(w_prime,2*w_prime-w)*binomial(n-w_prime,w-w_prime)/binomial(n,w_prime); #zeta probability in the paper
            
            L_prime = (2*Nw_prime^2/(pr_w_w_prime)*(2*log(n*1.)))^0.25;
            
            if L_prime < Nw_prime:
                
                x = 2*w_prime - w;
                pw = 0.5*binomial(n,w-w_prime)*binomial(n-(w-w_prime),w-w_prime)*binomial(n-2*(w-w_prime),2*w_prime-w)*factorial(2*w_prime-w)*(q-1)^(w-2*w_prime+1)/(binomial(n,w_prime)*binomial(n-w_prime,w-w_prime)*binomial(w_prime,2*w_prime-w));

                M_second = pr_w_w_prime*L_prime^4/4*pw*(pr_w_w_prime-2/(Nw_prime^2));    
                
                
                if M_second < 1:
                        
                    C_isd,p,l = peters_isd(n,k,q,w_prime);         
                    #cost = C_isd+log2(2*log(1.-L_prime/Nw_prime)/log(1.-1/Nw_prime)/Nw_prime);
#                    cost = C_isd+ log2(L_prime/Nw_prime);
                    
                    
                    
                    if L_prime < Nw_prime/2:
                        cost = C_isd+ log2(L_prime/Nw_prime);
                    else:
                        cost = C_isd+log2(2*log(1.-L_prime/Nw_prime)/log(1.-1./Nw_prime)/Nw_prime);
                    
                    
                    if cost < best_cost:
        #                    print(cost);
                            best_cost = cost;
                            best_w = w;
                            best_w_prime = w_prime;
                            best_L_prime = L_prime;
                    
    return best_cost, best_w, best_w_prime, best_L_prime;        


#######################################

#Complexity of original Beullen's algorithm to solve linear equivalence

def linear_beullens(n,k,q):
    
    
    max_w = n-k+2;

    best_cost = 100000000000000;
    best_w = 0;
    best_L = 0;
    best_Nw2 = 0;
    
    w_in, Nw = gv_distance(n,k,q);
        
    for w in range(w_in,max_w):
        
        Nw2 = binomial(n,w)*(q^2-1)^w*gauss_binomial(k,2,q)/((q^2-q)*(q^2-1))/gauss_binomial(n,2,q);
        
        if Nw2>1:
            
            L = (Nw2*ceil(n*(n-1)/(2*w*(n-w))))^0.5;            

            if L < Nw2:
            
                        
                C_isd,p,l = peters_isd(n,k,q,w);         
                
                #uncomment to consider Prange's ISD
#                    C_isd = log2((n^3+binomial(k,2))/(binomial(w,2)*binomial(n-w,k-2)/binomial(n,k)))
                cost = C_isd+log2(2*log(1.-L/Nw2)/log(1.-1/Nw2)/Nw2);
                cost = C_isd + log2(L/Nw2);
                    
                if cost < best_cost:
    #                    print(cost);
                    best_cost = cost;
                    best_w = w;
                    best_L = L;
                    best_Nw2 = Nw2;
                    
    return best_cost, best_w, best_L, best_Nw2;


# Cost of Prange's ISD adaption to find d-dimensional subcodes with support size w

def beullens_isd(q, n, k, d, w, Nw):
    success_pr = binomial(w, d) * binomial(n - w, k - d) / binomial(n, k);
    c_iter = k ^ 3 + binomial(k, d);

    #print(c_iter, 1 - (1 - success_pr) ^ Nw)
    return log2(c_iter) - log2(1 - (1 - success_pr) ^ Nw);


# Cost of ISD; depending on d, it considers either Peter's ISD or Belleuns' ISD
def cost_isd(q, n, k, d, w, Nw):
    if d == 1:

        # c_isd = peters_isd(q,n,k,w);

        # if c_isd.imag()!=0:

        pr_isd = binomial(w, 1) * binomial(n - w, k - 1) / binomial(n, k);
        cost = k ^ 3 + binomial(k, 1);

        if (k - 2) < (n - w):
            pr_isd += binomial(w, 2) * binomial(n - w, k - 2) / binomial(n, k);
            cost += binomial(k, 2) * (q - 1);

        if pr_isd == 0:
            c_isd = 10000000000;
        else:
            c_isd = log2(cost / (1 - (1 - pr_isd) ^ Nw));

    else:

        c_isd = beullens_isd(q, n, k, d, w, Nw);

    return max(0, c_isd);
##Testing the complexity on some instances

#n = 200;
#k = 100;
#
#max_q = 256;
#
#P = Primes();
#q_values = [2];
#q = 2;
#while q < max_q:
#    q = P.next(q);
#    if q < max_q:
#        q_values.append(q);
#
#
#Leon = [];
#Beullens = [];
#improved_Beullens = [];
#
#q_values = [11, 17, 53, 103, 151, 199, 251];
#for q in q_values:
#
#
#    print("For q = "+str(q));
#
#    cost_Leon,  w, Nw = leon_cost(n,k,q);
#
#    print("Leon: cost is "+str(cost_Leon)+", w = "+str(w));
#
#
#    improved_cost_Beullens, best_w, best_w_prime, best_L_prime = improved_linear_beullens(n,k,q);
#    Nw_prime = binomial(n,best_w_prime)*(q-1)^(best_w_prime-1)*q^(k-n)*1.;
#
#    print("Improved Beullens: cost is "+str(improved_cost_Beullens)+", w_prime = "+str(best_w_prime)+", w = "+str(best_w)+", L_prime = "+str(best_L_prime)+", Nw_prime = "+str(Nw_prime));
#
#
#    cost_Beullens, best_w, best_L, best_Nw2 = linear_beullens(n,k,q);
#    print("Beullens: cost is "+str(cost_Beullens)+", w = "+str(best_w)+", L = "+str(best_L)+", Nw2 = "+str(best_Nw2*1.));
#
#
#
#    Leon.append((q, cost_Leon));
#    improved_Beullens.append((q,improved_cost_Beullens));
#    Beullens.append((q,cost_Beullens));
#
#
#
#
#
#    print("-------------");
