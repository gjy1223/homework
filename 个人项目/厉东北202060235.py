import random
n=int(input("请输入你想要的题目数量：") )
symbols=['+','-','*','/']
temp=''
temp2=[]
results=0
def xyz():
    #生成随机数值
    num=random.randint (0,100)
    return num
def SYM():
    #生成随机运算符
    symbol=random.choice(symbols)
    return symbol
    
file=open('subject.txt',mode='w')

while n:
    temp='1.1'
    n=n-1
    while (eval(temp))%1!=0:
        #多个除号的时候情况恶劣 看最后的结果是不是整数
        w=xyz()
        temp=str(w)
        temp2=[w]
        for i in range(1,random.randint (3,4)):#随机数控制运算符的个数
            x=xyz()
            sym=SYM()
            temp2=temp2+[sym,x]
            for each in range(len(temp2)):
                while  temp2[each]=='/' and temp2[each+1]==0 or temp2[each]=='/'and temp2[each-1]%temp2[each+1]!=0 :
                    #判断除数是否为0 和 相除能否除尽
                    x=xyz()
                    temp2[each:each+2]=['/',x]
            temp+=sym+str(x)         #temp=''.join(temp2)     列表含有数值的时候不能使用该方法
    
    results=int(eval(temp))       
    file.write(temp+"="+str(results)+'\n')
    print (temp,"=")
    
file.close()   
    
    
