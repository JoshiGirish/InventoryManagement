
def getColumns(state):
    a=[]
    b=[]
    c=[]
    cols = state.productfiltercolumn_set.all()
    for col in cols:
        if col.visible == True:
            b.append(col.position)
            c.append(col.name)
    for i in range(0,len(b)):
        k = -1
        index = 0
        for j,val in enumerate(b):
            if val>k:
                k=val
                index = j
        a.append(c.pop(index))
        b.pop(index)
        a=a[::-1] # reverses the array
    return a
