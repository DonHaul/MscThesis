


def extractKeyFromDictList(dictt,keyy):
    return [ item[keyy] for item in dictt ]


def replicateThingInList(thing,N):

    l =[]

    for i in range(N):
        l.append(thing)

    return l



def is_empty(any_structure):
    if any_structure:
        #print('Structure is not empty.')
        return False
    else:
        #print('Structure is empty.')
        return True
