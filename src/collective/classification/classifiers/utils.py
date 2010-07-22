from math import sqrt


def pearson(v1, v2):
    # Simple sums
    sum1=sum(v1)
    sum2=sum(v2)
    # Sums of the squares
    sum1Sq=sum([pow(v, 2) for v in v1])
    sum2Sq=sum([pow(v, 2) for v in v2])
    # Sum of the products
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
    # Calculate r (Pearson score)
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq-pow(sum1, 2)/len(v1))*(sum2Sq-pow(sum2, 2)/len(v1)))
    if den==0:
        return 0
    return 1.0-num/den

def jaccard(v1,v2):
    s1=set(v1)
    s2=set(v2)
    return (1.0*len(s1.intersection(s2)))/len(s1.union(s2))