import re

def singularize (word) :
    """
    Singularizes English nouns.
    Taken from http://www.bermi.org/inflector/
    """
    rules = [
        ['(?i)(quiz)zes$' , '\\1'],
        ['(?i)(matr)ices$' , '\\1ix'],
        ['(?i)(vert|ind)ices$' , '\\1ex'],
        ['(?i)^(ox)en' , '\\1'],
        ['(?i)(alias|status)es$' , '\\1'],
        ['(?i)([octop|vir])i$' , '\\1us'],
        ['(?i)(cris|ax|test)es$' , '\\1is'],
        ['(?i)(shoe)s$' , '\\1'],
        ['(?i)(o)es$' , '\\1'],
        ['(?i)(bus)es$' , '\\1'],
        ['(?i)([m|l])ice$' , '\\1ouse'],
        ['(?i)(x|ch|ss|sh)es$' , '\\1'],
        ['(?i)(m)ovies$' , '\\1ovie'],
        ['(?i)(s)eries$' , '\\1eries'],
        ['(?i)([^aeiouy]|qu)ies$' , '\\1y'],
        ['(?i)([lr])ves$' , '\\1f'],
        ['(?i)(tive)s$' , '\\1'],
        ['(?i)(hive)s$' , '\\1'],
        ['(?i)([^f])ves$' , '\\1fe'],
        ['(?i)(^analy)ses$' , '\\1sis'],
        ['(?i)((a)naly|(b)a|(d)iagno|(p)arenthe|(p)rogno|(s)ynop|(t)he)ses$',
         '\\1\\2sis'],
        ['(?i)([ti])a$' , '\\1um'],
        ['(?i)(n)ews$' , '\\1ews'],
        ['(?i)s$' , ''],
    ];

    uncountable_words = ['equipment', 'information', 'rice', 'money', 'species', 'series', 'fish', 'sheep','sms'];

    irregular_words = {
        'people' : 'person',
        'men' : 'man',
        'children' : 'child',
        'sexes' : 'sex',
        'moves' : 'move'
    }

    lower_cased_word = word.lower();

    for uncountable_word in uncountable_words:
        if lower_cased_word[-1*len(uncountable_word):] == uncountable_word :
            return word
    for irregular in irregular_words.keys():
        match = re.search('('+irregular+')$',word, re.IGNORECASE)
        if match:
            return re.sub('(?i)'+irregular+'$', 
                match.expand('\\1')[0]+irregular_words[irregular][1:], word)

    for rule in range(len(rules)):
        match = re.search(rules[rule][0], word, re.IGNORECASE)
        if match :
            groups = match.groups()
            for k in range(0,len(groups)) :
                if groups[k] == None :
                    rules[rule][1] = rules[rule][1].replace('\\'+str(k+1), '')
            return re.sub(rules[rule][0], rules[rule][1], word)
    return word

from math import sqrt
def pearson(v1,v2):
    # Simple sums
    sum1=sum(v1)
    sum2=sum(v2)
    # Sums of the squares
    sum1Sq=sum([pow(v,2) for v in v1])
    sum2Sq=sum([pow(v,2) for v in v2])
    # Sum of the products
    pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
    # Calculate r (Pearson score)
    num=pSum-(sum1*sum2/len(v1))
    den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
    if den==0: return 0
    return 1.0-num/den