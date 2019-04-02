import pprint
import numpy as np
import Rtmat
import pickler as pickle


def main():

    d = pickle.Out("pickles/TLS01-04-2019 20-28-02.pickle")
    haa  =  np.random.rand(12,12)
    a = np.dot(haa.T,haa)

    b= d['C']

    print("a")
    pprint.pprint(a)    
    print("b")
    pprint.pprint(b)    

    DoMatrixStuff(a)

    DoMatrixStuff(b)


def DoMatrixStuff(A):

    print(A.shape)
    print("How Symmetric 0 is better:",abs(A-A.T).max())

    u,s,vh = np.linalg.svd(A)

    print("Howequal",abs(u-vh.T).max())


if __name__ == '__main__':
    main()
