"""
CamPoseGetter.py

This module contains the a class receives all the images and observations of the cameras, and calculates stuff with it
"""

import numpy as np
import cv2

from libs import *


class PosesCalculator(object):
    def __init__(self,N_objects):

        self.estimating='R'
        
        self.N_objects = N_objects

 


        #A.T A initialized
        self.ATAR = np.zeros((self.N_objects*3,self.N_objects*3))

        #A.T A initialized
        self.ATAt = np.zeros((self.N_objects*3,self.N_objects*3))

        #A.T b initialized
        self.ATb = np.zeros((self.N_objects*3,1))
        
    def AddObservations(self,obsR,obsT):

        #calculates rotations
        if self.estimating =='R':
            
            #only if there are observations it makes the A matrix
            if  ids is not None and len(ids)>1:

                A =  probdefs.rotationProbDef(obsR,self.Nmarkers)

                self.ATAR = self.ATAR  + np.dot(A.T,A)

        #calculates translations
        elif self.estimating == 't':
            
            if  ids is not None and len(ids)>1:

                A,b =  probdefs.translationProbDef(obsT,self.state.R,self.Nmarkers)

                self.ATAt = self.ATAt + np.dot(A.T,A) #way to save the matrix in a compact manner

                self.ATb = self.ATb + np.dot(A.T,b) #way to save the matrix in a compact manner

        else:
            print("Not Estimating Anything")

    def CalcRthenStartT(self):
            
            rotSols = algos.RProbSolv1(self.ATAR,3,self.N_objects)

            #converts to world coordinates or into them
            rotSolsNotUsed = mmnip.Transposer(rotSols)

            #converts in first ref coordinates , 
            rr = mmnip.genRotRelLeft(rotSolsNotUsed)

            visu.ViewRefs(rr)

            self.R=rr

            self.estimating='t'

    
    
    def CalcT(self):

        x = np.dot(np.linalg.pinv(self.ATAt),self.ATb)
    
        solsplit2 = np.split(x,self.N_cams)
        
        visu.ViewRefs(self.R,solsplit2,refSize=0.1,showRef=True)

        self.t=solsplit2        



        



    



            

            
            
        
        




   