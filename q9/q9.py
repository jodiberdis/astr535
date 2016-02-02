# Imagine you are observing a binary star system, but where the stars are so close together 
# that you cannot resolve them, and you see them as a single object. 
# If the two stars have magnitudes of 17 and 18 individually, what is the combined 
# observed magnitude? 
# Write a (short!) software function that takes as input the apparent magnitude of each of 
# two stars, and computes and returns the apparent magnitude of the two stars combined.

import numpy as np

def binarymag(m1,m2):
    ratio_f1f2 = 10.0**((m1-m2)/-2.5)
    comb_mag = m1 + 2.5*np.log10(ratio_f1f2+1.0)
    return comb_mag


m1 = input('Enter the magnitude of your brighter star: ')
m2 = input('Enter the magnitude of your dimmer star: ')
print 'The combined magnitude of your binary star system is: ', binarymag(m1, m2)
