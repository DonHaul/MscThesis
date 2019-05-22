import numpy as np


def MatrixListError(A,B):

    C=[]

    for a, b in zip(A,B):
        C.append(a-b)

    actualNorm=[]
    for r in C:
        print(r.shape)
        actualNorm.append(np.linalg.norm(r,ord='fro'))

    inds = np.squeeze(np.indices((len(actualNorm),)))

    return actualNorm,inds
