"""
computeDistances.py

"""
from scipy.spatial import distance


def computeDistances(fv):
    # Inputs
    # fv: A N-by-D array containing D-dimensional feature vector of 
    #     N number of data (images)
    # 
    # Output
    # D: N-by-N square matrix containing the pairwise distances between
    #    all samples, i.e. the first row shows the distance
    #    between the first sample and all other samples 
    #    (columns)
    #
    
    # This is the baseline distance measure: Euclidean (L2) distance
    D = distance.squareform(distance.pdist(fv, 'cosine') )
    
        
    # END OF YOUR CODE
    #########################################################################
    return D