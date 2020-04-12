from scipy import *
from pylab import *

def Distance(R1, R2):
    return sqrt((R1[0]-R2[0])**2+(R1[1]-R2[1])**2)

def TotalDistance(city, R):
    dist=0
    for i in range(len(city)-1):
        dist += Distance(R[city[i]],R[city[i+1]])
    dist += Distance(R[city[-1]],R[city[0]])
    return dist
    
def reverse(city, n):
    nct = len(city)
    nn = (1+ ((n[1]-n[0]) % nct))/2 
    for j in range(nn):
        k = (n[0]+ j) % nct
        l = (n[1]- j) % nct
        (city[k],city[l]) = (city[l],city[k])  
    
def transpt(city, n):
    nct = len(city)
    
    newcity=[]
   
    for j in range( (n[1]-n[0])%nct + 1):
        newcity.append(city[ (j+n[0])%nct ])

    for j in range( (n[2]-n[5])%nct + 1):
        newcity.append(city[ (j+n[5])%nct ])

    for j in range( (n[4]-n[3])%nct + 1):
        newcity.append(city[ (j+n[3])%nct ])
    return newcity

def Plot(city, R, dist):
    # Plot
    Pt = [R[city[i]] for i in range(len(city))]
    Pt += [R[city[0]]]
    Pt = array(Pt)
    title('Total distance='+str(dist))
    plot(Pt[:,0], Pt[:,1], '-o')
    show()

if __name__=='__main__':

    ncity = 100       
    maxTsteps = 100    
    Tstart = 0.2       
    fCool = 0.9     
    maxSteps = 100*ncity     
    maxAccepted = 10*ncity   

    Preverse = 0.5      

    
    R=[]
    for i in range(ncity):
        R.append( [rand(),rand()] )
    R = array(R)

    
    city = range(ncity)

    dist = TotalDistance(city, R)


    n = zeros(6, dtype=int)
    nct = len(R) 
    
    T = Tstart 

    Plot(city, R, dist)
    
    for t in range(maxTsteps): 

        accepted = 0
        for i in range(maxSteps): 
            
            while True: 
                n[0] = int((nct)*rand())     
                n[1] = int((nct-1)*rand())   
                if (n[1] >= n[0]): n[1] += 1   
                if (n[1] < n[0]): (n[0],n[1]) = (n[1],n[0]) 
                nn = (n[0]+nct -n[1]-1) % nct  
                if nn>=3: break
        
           
            n[2] = (n[0]-1) % nct  
            n[3] = (n[1]+1) % nct  
            
            if Preverse > rand(): 
                
                de = Distance(R[city[n[2]]],R[city[n[1]]]) + Distance(R[city[n[3]]],R[city[n[0]]]) - Distance(R[city[n[2]]],R[city[n[0]]]) - Distance(R[city[n[3]]],R[city[n[1]]])
                
                if de<0 or exp(-de/T)>rand(): 
                    accepted += 1
                    dist += de
                    reverse(city, n)
            else:
            
                nc = (n[1]+1+ int(rand()*(nn-1)))%nct  
                n[4] = nc
                n[5] = (nc+1) % nct
        
               
                de = -Distance(R[city[n[1]]],R[city[n[3]]]) - Distance(R[city[n[0]]],R[city[n[2]]]) - Distance(R[city[n[4]]],R[city[n[5]]])
                de += Distance(R[city[n[0]]],R[city[n[4]]]) + Distance(R[city[n[1]]],R[city[n[5]]]) + Distance(R[city[n[2]]],R[city[n[3]]])
                
                if de<0 or exp(-de/T)>rand(): 
                    accepted += 1
                    dist += de
                    city = transpt(city, n)
                    
            if accepted > maxAccepted: break

        # Plot
        Plot(city, R, dist)
            
        print ("T=%10.5f , distance= %10.5f , accepted steps= %d" %(T, dist, accepted))
        T *= fCool            
        if accepted == 0: break  

        
    Plot(city, R, dist)
