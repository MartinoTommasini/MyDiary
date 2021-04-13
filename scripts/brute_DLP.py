h=3107
g=3
p=4327

a=1
while True:
    print(a)
    if pow(g,a,p)==h:
        print("Found a: "+str(a))
        exit(1)
    a  += 1


   
