def exp_func(x, y, N):
    exp = bin(y)
    value = x
 
    for i in range(3, len(exp)):
        value = (value * value) % N
        print (i)
        if(exp[i:i+1]=='1'):
            value = (value*x) % N
	    print (i)
    return value
c=810005773870709891389047844710609951449521418582816465831855191640857602960242822
N=1763350599372172240188600248087473321738860115540927328389207609428163138985769311
m=177357260603510007903211978293167625652027411836388457692827332910803940221
e=65537
d=188047321955721375508157638187334651345661324123156155999468187676652730213105073
p=31415926535897932384626433832795028841
q=56129192858827520816193436882886842322337671

c2=70415348471515884675510268802189400768477829374583037309996882626710413688161405504039679028278362475978212535629814001515318823882546599246773409243791879010863589636128956717823438704956995941
e2=3
print(exp_func(c2,1.0/3,N))




