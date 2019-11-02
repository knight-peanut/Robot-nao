global angleKey=[] 
 

def addData(data):
    if not judge():
        return
    
    if (type(anglekey[0])!=list):
        angleKey.append(data)
    else:
        if(angleKey[-1]>0) and (data<0):
            angleKey.append(data)
        if(angleKey[-1]<0) and (data>0):
            angleKey.append(data)

def IsError(data):
    if abs(data)>40*almath.TO_RAD:
        return False
    else:
        return True


