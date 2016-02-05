# 3)
# Start to develop a software module that will use the count equation that will eventually be used 
# for an exposure time calculator. The module should include individual functions that return values 
# for each of the terms on the count equation: photon flux, telescope area, atmospheric transmission, 
# system transmission (split into separate routines for each of telescope throughput, instrument 
# throughput, filter throughput, and detector efficiency). Each routine should accept as input a 
# wavelength or array of wavelengths, and return values at all of the specified input wavelengths. 
# A higher level function should return the estimated counts integrated over all wavelengths; 
# for the initial effort you could just return a constant value at all wavelengths, but look forward 
# to building in the capability for wavelength dependence, e.g., interpolating from a list of 
# wavelength/values from an input file. A higher level function should return the estimated counts 
# integrated over all wavelengths. You should make appropriate use of input keywords and default values. 
# You are strongly encouraged to sketch out the design of the program before starting to write it, 
# considering the eventual use of the program to provide exposure time estimates for all of the APO 3.5m 
# instruments (and perhaps others), where you will have wavelength dependent throughputs for multiple 
# components. Test the program by using it to do the calculation for the NMSU 1m. 


import numpy as np

# FUNCTIONS:

def telescope_area(R):       # Area of telescope mirror with R radius
    return np.pi*(R**2.0)    #   (preferably in centimeters)


def flux_star(lambd, mag):
    Fvega = 3.6E-9 * ((lambd/5500)**-2.0)   # Flux of Vega at particular inputted wavelength
    return Fvega*10.0**(mag/(-2.5))         #   Units: ergs/cm^2/s/A


def photon_flux(Fstar, h, c, lambd):        # Photon flux at detector
    return (Fstar*lambd)/(h*c)              #   Units: photons/cm^2/s/A


def exposure_time(S, q, a, T, h, c, lambd, bandwidth):
    lambd_initial = lambd - (bandwidth/2)  # Angstroms
    lambd_final = lambd + (bandwidth/2)    # Angstroms
    return (S / (q*a*T*Fstar/(h*c) * 0.5*((lambd_final**2.0) - (lambd_initial**2.0))))
    #       Constants out front....|...Output of integral


#----------------------------------------------------------------------------------------------------------
# CODE:

# Define constants (all in cgs!):
h = 6.626E-27              # erg*s
c = 2.998E18               # Angstroms/s
q = 0.5                    # Telescope efficiency
a = 0.8                    # Atmospheric transmission efficiency
R = 50                     # 0.5 meters in centimeters (radius of the 1m telescope)
T = telescope_area(R)      # Area of 1m telescope - use function telescope_area

print 'Welcome to the Apache Point Observatory 1-meter Telescope Exposure Time Calculator!'
lambd = input('Please enter the central wavelength of the bandpass in which you will observe (in Angstroms): ')
mag = input('Please enter the magnitude of the star you will observe: ')
bandwidth = input('Please enter the width of your bandpass (in Angstroms): ')
sn = input('Finally, please enter your desired Signal-To-Noise Ratio: ')

S = sn**2    # Signal-To-Noise ratio is the square root of the Signal

Fstar = flux_star(lambd, mag)  # Flux of specified star - flux_star uses flux of Vega as standard

t = exposure_time(S, q, a, T, h, c, lambd, bandwidth)

print photon_flux(Fstar, h, c, lambd)

print 'Your recommended exposure time (in seconds) is: ', t


