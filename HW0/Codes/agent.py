import random

# from tic_tac_toe_gui import Ui_window


#################################################################################
# Functions
#################################################################################

def ai_action(game_state):
    ''' Generate and play move from tic tac toe AI'''
    #################################################################################
    # "*** YOUR CODE HERE ***"
    #################################################################################
    
    
    conditions = [
            # horizontal
            (game_state[0], game_state[1], game_state[2], game_state[3]),
            (game_state[1], game_state[2], game_state[3], game_state[4]),
            (game_state[5], game_state[6], game_state[7], game_state[8]),
            (game_state[6], game_state[7], game_state[8], game_state[9]),
            (game_state[10], game_state[11], game_state[12], game_state[13]),
            (game_state[11], game_state[12], game_state[13], game_state[14]),
            (game_state[15], game_state[16], game_state[17], game_state[18]),
            (game_state[16], game_state[17], game_state[18], game_state[19]),
            (game_state[20], game_state[21], game_state[22], game_state[23]),
            (game_state[21], game_state[22], game_state[23], game_state[24]),

            # vertical
            (game_state[0], game_state[5], game_state[10], game_state[15]),
            (game_state[5], game_state[10], game_state[15], game_state[20]),
            (game_state[1], game_state[6], game_state[11], game_state[16]),
            (game_state[6], game_state[11], game_state[16], game_state[21]),
            (game_state[2], game_state[7], game_state[12], game_state[17]),
            (game_state[7], game_state[12], game_state[17], game_state[22]),
            (game_state[3], game_state[8], game_state[13], game_state[18]),
            (game_state[8], game_state[13], game_state[18], game_state[23]),
            (game_state[4], game_state[9], game_state[14], game_state[19]),
            (game_state[9], game_state[14], game_state[19], game_state[24]),

            # diagonal
            (game_state[0], game_state[6], game_state[12], game_state[18]),
            (game_state[6], game_state[12], game_state[18], game_state[24]),
            (game_state[4], game_state[8], game_state[12], game_state[16]),
            (game_state[8], game_state[12], game_state[16], game_state[20]),
            (game_state[1], game_state[7], game_state[13], game_state[19]),
            (game_state[5], game_state[11], game_state[17], game_state[23]),
            (game_state[3], game_state[7], game_state[11], game_state[15]),
            (game_state[9], game_state[13], game_state[17], game_state[21]),

        ]
    if game_state.count(2) > 0:
            return None
    p=check(conditions,game_state)[0]
    if p>=0:
        return p
    emptyStates = []
    beststates=[12,7,11,13,17]
    best2=[6,8,18,16]
    # for i in range(0,25):     
    #         if game_state[i] ==0:
    #             por(i,game_state)
    # if game_state[12]==None:
    #     return 12 
    maxindex=porkardan(conditions,game_state)
    if maxindex!=-1:
        return maxindex
    for i in range(0,25):     
            if game_state[i] is None:
                    emptyStates.append(i)
    for k in beststates:
        if k in emptyStates:
            return k
    for k in best2:
        if k in emptyStates:
            return k
    return random.choice(emptyStates)
    
    # if game_state.count(1)>0:
        
    # com=set(emptyStates).intersection(set(beststates))
    # com2=set()
    # if len(com)>0:
        
    #     return list(com)[0]
    # if len(com)==0:
    #     com2=set(emptyStates).intersection(set(best2))
    # if len(com2)>0:
    #     return list(com2)[0]
    # if(len(com)==0 and len(com2)==0):
    
    
        
        
def porkardan(conditions,game_state):
    idwine=[(0,1,2,3),(1,2,3,4),(6,7,8,9),(10,11,12,13),(11,12,13,14),(15,16,17,18),(16,17,18,19),(20,21,22,23),(21,22,23,24)
            ,(0,5,10,15),(5,10,15,20),(1,6,11,16),(6,11,16,21),(2,7,12,17),(7,12,17,22),(3,8,13,18),(8,13,18,23),(4,9,14,19),(9,14,19,24)
            ,(0,6,12,18),(6,12,18,24),(4,8,12,16),(8,12,16,20),(1,7,13,19),(5,11,17,23),(3,7,11,15),(9,13,17,21)]
    max=0
    maxindex=-1
    for con in idwine:
        current,index=closewinepor(con,game_state)
        if max<current:
            max=current
            maxindex=index
    return maxindex
def winestates(i,condition):
    idwine=[(0,1,2,3),(1,2,3,4),(6,7,8,9),(10,11,12,13),(11,12,13,14),(15,16,17,18),(16,17,18,19),(20,21,22,23),(21,22,23,24)
            ,(0,5,10,15),(5,10,15,20),(1,6,11,16),(6,11,16,21),(2,7,12,17),(7,12,17,22),(3,8,13,18),(8,13,18,23),(4,9,14,19),(9,14,19,24)
            ,(0,6,12,18),(6,12,18,24),(4,8,12,16),(8,12,16,20),(1,7,13,19),(5,11,17,23),(3,7,11,15),(9,13,17,21)]
    listwine=[]
    for  con in idwine:
        if i in con:
                listwine.append(con)
    return listwine
def closewinepor(con,game_state):
        sum=0
        res=-1
        
        for c in con:
            if(game_state[c]==0):
                sum+=1
            elif(game_state[c]==1):
                return (0,0)
            else:
                res=c
        return (sum,res)
def closewine(con,game_state,k):
        sum=0
        res=-1
        
        for c in con:
            if(game_state[c]==k):
                sum+=1
                
            elif(game_state[c]==None):
                res=c
        if(sum==3 and res!=-1):
            return res
        else:
            return -1
def check(condition,game_state):
    listwine=[]
    for i in range(0,25):  
        if game_state[i] ==0:
            listwine=winestates(i,condition)
            for c in listwine:
                m=closewine(c,game_state,0)
                if(m>=0):
                    return (m,0)
    for i in range(0,25):  
        if game_state[i] ==1:
            listwine=winestates(i,condition)
            for c in listwine:
                m=closewine(c,game_state,1)
                if(m>=0):
                    return (m,1)
    
    return (-1,-1)


# film tozih
# https://drive.google.com/file/d/18B3DE199ciUix1xEJ6jOxQTvk-7RIeFv/view?usp=sharing