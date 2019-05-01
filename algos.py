'''
algos.py

This module contains some of the well known algorithms, that help in the thesis
'''

import numpy as np
#import scipy.linalg

def LeastSquaresNumpy(A,b):
    '''
    Gets least squares aproximation.

    Gets x that minimzes Ax=b
    '''
    return np.linalg.lstsq(A,b,rcond=None) #(A'A)^(-1) * A'b  returns x, res, rank, sss

def LeastSquares(A,b):
    '''
    Gets least squares aproximation.

    Gets x that minimzes Ax=b
    '''
    return  np.dot( np.linalg.pinv(A),b) #(A'A)^(-1) * A'b 

def LeastSquaresOldSchool(A,b):
    '''
    Gets least squares aproximation.

    Gets x that minimzes Ax=b
    '''
    return np.dot(np.dot(np.linalg.inv(np.dot(A.T,A)),A.T),b)

def LeastSquaresOldSchoolPinved(A,b):
    '''
    Gets least squares aproximation.

    Gets x that minimzes Ax=b
    '''
    return np.dot(np.dot(np.linalg.pinv(np.dot(A.T,A)),A.T),b)

def MeanSquaredError(a,b=None):
    '''
    Sum of squared error, or sum of squared, of every element in a matrix, element wise
    '''
    
    if(b is not None):
        a=a-b

    return np.sqrt(np.sum(a**2))


#this is how wikipedia does it
def procrustes(X,Y):
    '''
    Get closest matrix that minimizes R : min RX-Y such that R.T*R is Identity 

    Gets x that minimzes Ax=b
    '''

    #get mean
    muX = X.mean(0)
    muY = Y.mean(0)

    #center X and Y around mean
    X0 = X - muX
    Y0 = Y - muY

    # optimum rotation matrix of Y
    H = np.dot(X0.T, Y0)
    U,s,Vt = np.linalg.svd(H)
    V = Vt.T


    if np.linalg.det(V) < 0: # == -1
        b = V[:,-1]
        b= b*-1
        V[:,-1] = b


    R = np.dot(V, U.T)
    t = muX - np.dot(muY, R)

 

    return R, t



#same as procrustes 1 but arguments are inverted - (This is how it is done in  the paper - Estimating 3-D rigid body transformations: a comparison of four major algorithms)
def procrustes2(X,Y):
    '''
    Get closest matrix that minimizes R : min RX-Y such that R.T*R is Identity 

    Gets x that minimzes Ax=b
    '''
    muX = X.mean(0)
    muY = Y.mean(0)

    X0 = X - muX
    Y0 = Y - muY

    # optimum rotation matrix of Y
    H = np.dot(X0.T, Y0)
    U,s,Vt = np.linalg.svd(H)
    V = Vt.T


    if np.linalg.det(V) < 0: # == -1
        b = V[:,-1]
        b= b*-1
        V[:,-1] = b


    R = np.dot(U, Vt)
    t = muX - np.dot(muY, R)

    

    return R, t

def nullspace(A, atol=1e-13, rtol=0):
    """Compute an approximate basis for the nullspace of A.

    The algorithm used by this function is based on the singular value
    decomposition of `A`.

    Parameters
    ----------
    A : ndarray
        A should be at most 2-D.  A 1-D array with length k will be treated
        as a 2-D with shape (1, k)
    atol : float
        The absolute tolerance for a zero singular value.  Singular values
        smaller than `atol` are considered to be zero.
    rtol : float
        The relative tolerance.  Singular values less than rtol*smax are
        considered to be zero, where smax is the largest singular value.

    If both `atol` and `rtol` are positive, the combined tolerance is the
    maximum of the two; that is::
        tol = max(atol, rtol * smax)
    Singular values smaller than `tol` are considered to be zero.

    Return value
    ------------
    ns : ndarray
        If `A` is an array with shape (m, k), then `ns` will be an array
        with shape (k, n), where n is the estimated dimension of the
        nullspace of `A`.  The columns of `ns` are a basis for the
        nullspace; each element in numpy.dot(A, ns) will be approximately
        zero.
    """

    A = np.atleast_2d(A)
    u, s, vh = np.linalg.svd(A)
    tol = max(atol, rtol * s[0])
    nnz = (s >= tol).sum()
    ns = vh[nnz:].conj().T
    
    return ns

def TotalLeastSquares(C,Nleast=1,Nmarkers=1):
    '''
    Get the X that minimizes AX=0 through svd, and splits it up

    Args:
        C: matrix A in the equation
        Nleast: how many of the eigenvectors with the smallest eigenvalues do we want?
        Nmarkers: total number of markers, it is used to split up the fetched lowest eigenvectors 
    Returns:
        rotsols: Split up lower eigenvalued, eigenvectors (the least significat)
    '''
    #print(C)
    u,s,vh = np.linalg.svd(C)
    
    #if symettirc, u.T = vh

    #IF there is indeed a null space, then svd breaks
    #print("vh")
    #print(vh)
    #print("u")
    #print(u.T)
    #print("UVH")
    #print(np.dot(u,vh))

    return u[:,-Nleast:]


def RProbSolv1(C,Nleast=1,Nmarkers=1):

    solution = TotalLeastSquares(C,Nleast,Nmarkers)

    rotsols=[] 

    solsplit = np.split(solution,Nmarkers)  

    #get actual rotation matrices by doing the procrustes
    for sol in solsplit:
        print("opt1")
        print(np.linalg.det(sol))
        print(np.dot(sol.T,sol))

        r,t=procrustes(np.eye(3),sol)
        rotsols.append(r)


    return rotsols

def RProbSolv2(C,Nleast=1,Nmarkers=1):

    solution = TotalLeastSquares(C,Nleast,Nmarkers)   



    Icol=(np.array([1,0,0,0,1,0,0,0,1])[np.newaxis]).T

    qmao=np.array([[1,0,0,0,0,0],
    [0,1,0,0,0,0],
    [0,0,1,0,0,0],
    [0,1,0,0,0,0],
    [0,0,0,1,0,0],
    [0,0,0,0,1,0],
    [0,0,1,0,0,0],
    [0,0,0,0,1,0],
    [0,0,0,0,0,1],
    ])

    




    solsplit = np.split(solution,Nmarkers)  
    

    print("before")
    for sol in solsplit:
        print(np.linalg.det(sol))
        print(np.dot(sol.T,sol))



    iii = np.empty((0,1))
    vacols=np.empty((0,9))

    #get actual rotation matrices by doing the procrustes
    for sol in solsplit:
        vacols = np.vstack([vacols,np.kron(sol,sol)])

        iii = np.vstack([iii,Icol])
    
    x = LeastSquares(np.dot(vacols,qmao),iii)

    Q=np.array([[x[0],x[1],x[2]],
    [x[1],x[3],x[4]],
    [x[2],x[4],x[5]]])
    Q=np.squeeze(Q)
    
    u,s,v=np.linalg.svd(Q)
    
    G=np.squeeze(np.dot(u,np.diag(np.sqrt(s))))
    
    
    rotestimate=[]
    print("after")
    for sol in solsplit:
        ps=np.dot(sol,G)
        print(np.linalg.det(ps))
        print(np.dot(ps.T,ps))
        r,t=procrustes(np.eye(3),ps)
        print(np.linalg.det(r))
        print(np.dot(r.T,r))
        rotestimate.append(r)

    return rotestimate


def TotalLeastSquares(C,Nleast=1,Nmarkers=1):
    
    '''
    Get the X that minimizes AX=0 through svd, and splits it up

    Args:
        C: matrix A in the equation
        Nleast: how many of the eigenvectors with the smallest eigenvalues do we want?
        Nmarkers: total number of markers, it is used to split up the fetched lowest eigenvectors 
    Returns:
        rotsols: Split up lower eigenvalued, eigenvectors (the least significat)
    '''

    #print(C)
    u,s,vh = np.linalg.svd(C)
    
    #if symettirc, u.T = vh

    #IF there is indeed a null space, then svd breaks
    #print("vh")
    #print(vh)
    #print("u")
    #print(u.T)
    #print("UVH")
    #print(np.dot(u,vh))


    print("s")
    print(s)
    #print("u")
    #print(u)
    #print("nullspace")
    #ns = nullspace(C,atol=1e-10)



    
    #solution =np.concatenate((-np.expand_dims(u[:,10],1),-np.expand_dims(u[:,11],1), np.expand_dims(u[:,9],1)),1)
    solution = u[:,-Nleast:]

    #solution=ns
    #print(solution)
    #print(ns)
    #print("sol")
    #print(solution)
   

    return solution



#copy of matlab procrustes function
#https://stackoverflow.com/questions/18925181/procrustes-analysis-with-numpy
def procrustesMatlab(X, Y, scaling=True, reflection='best'):
    """
    A port of MATLAB's `procrustes` function to Numpy.

    Procrustes analysis determines a linear transformation (translation,
    reflection, orthogonal rotation and scaling) of the points in Y to best
    conform them to the points in matrix X, using the sum of squared errors
    as the goodness of fit criterion.

        d, Z, [tform] = procrustes(X, Y)

    Inputs:
    ------------
    X, Y    
        matrices of target and input coordinates. they must have equal
        numbers of  points (rows), but Y may have fewer dimensions
        (columns) than X.

    scaling 
        if False, the scaling component of the transformation is forced
        to 1

    reflection
        if 'best' (default), the transformation solution may or may not
        include a reflection component, depending on which fits the data
        best. setting reflection to True or False forces a solution with
        reflection or no reflection respectively.

    Outputs
    ------------
    d       
        the residual sum of squared errors, normalized according to a
        measure of the scale of X, ((X - X.mean(0))**2).sum()

    Z
        the matrix of transformed Y-values

    tform   
        a dict specifying the rotation, translation and scaling that
        maps X --> Y

    """

    n,m = X.shape
    ny,my = Y.shape

    muX = X.mean(0)
    muY = Y.mean(0)

    X0 = X - muX
    Y0 = Y - muY

    ssX = (X0**2.).sum()
    ssY = (Y0**2.).sum()

    # centred Frobenius norm
    normX = np.sqrt(ssX)
    normY = np.sqrt(ssY)

    # scale to equal (unit) norm
    X0 /= normX
    Y0 /= normY

    if my < m:
        Y0 = np.concatenate((Y0, np.zeros(n, m-my)),0)

    # optimum rotation matrix of Y
    A = np.dot(X0.T, Y0)
    U,s,Vt = np.linalg.svd(A,full_matrices=False)
    V = Vt.T
    T = np.dot(V, U.T)

    if reflection is not 'best':

        # does the current solution use a reflection?
        have_reflection = np.linalg.det(T) < 0

        # if that's not what was specified, force another reflection
        if reflection != have_reflection:
            V[:,-1] *= -1
            s[-1] *= -1
            T = np.dot(V, U.T)

    traceTA = s.sum()

    if scaling:

        # optimum scaling of Y
        b = traceTA * normX / normY

        # standarised distance between X and b*Y*T + c
        d = 1 - traceTA**2

        # transformed coords
        Z = normX*traceTA*np.dot(Y0, T) + muX

    else:
        b = 1
        d = 1 + ssY/ssX - 2 * traceTA * normY / normX
        Z = normY*np.dot(Y0, T) + muX

    # transformation matrix
    if my < m:
        T = T[:my,:]
    c = muX - b*np.dot(muY, T)

    #transformation values 
    tform = {'rotation':T, 'scale':b, 'translation':c}

    return d, Z, tform


