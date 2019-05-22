


def extractKeyFromDictList(dictt,keyy):
    return [ item[keyy] for item in dictt ]


def replicateThingInList(thing,N):

    l =[]

    for i in range(N):
        l.append(thing)

    return l