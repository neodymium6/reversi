
def PickUp(ban,pos,dir1):
    res=[]
    i=1
    flag=-1<pos+i*dir1<64
    if flag:
        flag=flag and ban[pos+i*dir1]!=0
        flag=flag and not ((pos+(i-1)*dir1)%8==0 and (pos+i*dir1)%8==7)
        flag=flag and not ((pos+(i-1)*dir1)%8==7 and (pos+i*dir1)%8==0)
    while flag:
        res.append(ban[pos+i*dir1])
        i+=1
        flag=-1<pos+i*dir1<64
        if flag:
            flag=flag and ban[pos+i*dir1]!=0
            flag=flag and not ((pos+(i-1)*dir1)%8==0 and (pos+i*dir1)%8==7)
            flag=flag and not ((pos+(i-1)*dir1)%8==7 and (pos+i*dir1)%8==0)
    return res
        
def CanPut(ban,pos,turn):
    if ban[pos]!=0:
        return False
    direction=[-9,-8,-7,-1,1,7,8,9]
    for dir1 in direction:
        tmp=PickUp(ban,pos,dir1)
        i=0
        flag=i<len(tmp)
        flag= flag and tmp[i]==3-turn 
        while flag:
            i+=1
            flag=i<len(tmp)
            flag= flag and tmp[i]==3-turn 
        #print(i,tmp)
        if 0<i<len(tmp):
            if tmp[i]==turn:
                return True
    return False
def Reverse(ban,pos,turn):
    direction=[-9,-8,-7,-1,1,7,8,9]
    reverse_num=[0]*8
    for dir1 in direction:
        tmp=PickUp(ban,pos,dir1)
        i=0
        flag=i<len(tmp)
        flag= flag and tmp[i]==3-turn 
        while flag:
            i+=1
            flag=i<len(tmp)
            flag= flag and tmp[i]==3-turn 
        if 0<i<len(tmp):
            if tmp[i]==turn:
                reverse_num[direction.index(dir1)]=i
    for i in range(len(direction)):
        for j in range(reverse_num[i]):
            ban[pos+(j+1)*direction[i]]=turn














