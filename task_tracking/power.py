#def power(a,n):
#    if n == 0:
#        return 1
#    return a * power(a, n-1)
#a = float(input())
#n = int(input())
#result = power(a,n)
#print(result)
#def power(a,n):
#    res = 1
#    i = 1
#    while 1 <= abs(n):
#        res  *=  a
#        i += 1 
#    if n < 0: 
#        return 1 / res
#    return res 
#a = float(input())
#n = int(input())
#result = power(a,n)
#print(result)
#def power(a,n): 
#    if n == 0:
#        return 1 
#    if n % 2 != 0:
#        return a * power(a, n-1) 
#    return power(a * a, n // 2) 

#a = float(input())
#n = int(input())
#result = power(a,n)
#print(result)


def  move(n, start= 1, finish=3):
    if n ==  1:
        print(n, start,finish)
    else:
        temp =  6 - (start + finish)
        move(n - 1, start, temp)
        print(n, start, finish)
        move(n - 1, temp,finish)


n = int(input())
move(n)