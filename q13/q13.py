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
# *********************************************************************************************************
# Continue working on your exposure time calculator software by adding routines to calculate the S/N 
# of a given exposure. You will want to call your count equation routine to get the signal for an object 
# of some input magnitude, call it again to get the background for a given sky brightness, allow for an 
# input sky area/image size (with suitable default value), and call a routine to return the readout noise 
# for an input pixel scale and input sky area/image size. Validate your routine using the results from 
# the previous question. 


import numpy as np

# FUNCTIONS:

def telescope_area(R):       # Area of telescope mirror with R radius
    return np.pi*(R**2.0)    #   (preferably in centimeters)


def flux_star(lambd, mag):
    Fvega = 3.6E-9 * ((lambd/5500)**-2.0)   # Flux of Vega at particular inputted wavelength
    return Fvega*10.0**(mag/(-2.5))         #   Units: ergs/cm^2/s/A


def photon_flux(Fstar, h, c, lambd):        # Photon flux at detector
    return (Fstar*lambd)/(h*c)              #   Units: photons/cm^2/s/A


def atmos(a, lambd):          # Atmospheric transmission efficiency
    return a


def system(tele, instr, filt, detector, lambd):  # System efficiency
    q = tele*instr*filt*detector                 #   includes efficiency of telescope, 
    return q                                     #   instrument, filter, and detector


def background(B, lambd):     # Background sky contribution
    return B


def aperture_area(seeing, platescale, lambd):  # Area of aperture, given some radius or plate scale
    r = seeing / platescale
    return np.pi*(r**2)


def numpix(Npx, lambd):       # Number of pixels in aperture area
    return Npx


def sigma_rn(readout, lambd): # Readout noise 
    return readout            #   Units: electrons/pixel or photons/pixel


def integral(lambd_initial, lambd_final, binsize, q, a, mag):
    steps = np.arange(lambd_initial,lambd_final,binsize)   # Array of lambda values between initial and
    temp = 0                                               #   final with stepsize equal to 'binsize'
    summ = 0
    for i in steps:
        temp = (flux_star(i,mag)*q*a) * i                  # For each step, compute integral
        summ += temp                                       # Sum up all values from each step
    return summ


def lambd_i(lambd, bandwidth):
    return (lambd - (bandwidth/2))     # Initial value to pass integral limit - Angstroms
   
def lambd_f(lambd, bandwidth):
    return (lambd + (bandwidth/2))     # Final value to pass integral limit - Angstroms

def exposure_time(S, q, a, T, h, c, lambd, bandwidth, mag):
    binsize=0.5                             # Step size for integral function summing
    lambd_initial = lambd_i(lambd, bandwidth)
    lambd_final = lambd_f(lambd, bandwidth)
    return (S * (h*c)) / (T*integral(lambd_initial, lambd_final, binsize, q, a, mag))
           # Solve Count Equation for t (exposure time)


def snr(t, T, h, c, lambd, bandwidth, B, A, Npx, readout, q, a, mag):
    binsize=0.5
    lambd_initial = lambd_i(lambd, bandwidth)
    lambd_final = lambd_f(lambd, bandwidth)
    S = ((t*T)/(h*c))*integral(lambd_initial, lambd_final, binsize, q, a, mag)
    return (S / np.sqrt(S + B*A + Npx*(readout**2.0)))




#----------------------------------------------------------------------------------------------------------
# CODE:

print 'Welcome to the Apache Point Observatory 1-meter Telescope Exposure Time Calculator!'
answer = input('Would you like to calculate an estimated exposure time (1) or a signal-to-noise ratio snr (2) ? ')

# If user does not enter a 1 (exosure time) or a 2 (snr)
if answer != 1 and answer != 2:   # Trying to find a way to loop through this until user enters 1 or 2 and breaks out
    answer = input('Please type "1" to calculate an estimated exposure time, or type "2" to calculate a signal-to-noise ratio: ')


# Collecting necessary information from user, regardless of answer (1) or (2)
lambd = input('Please enter the central wavelength of the bandpass in which you will observe (in Angstroms): ')
bandwidth = input('Please enter the width of your bandpass (in Angstroms): ')
mag = input('Please enter the magnitude of the star you will observe: ')

# Define constants (all in cgs!):
h = 6.626E-27                # erg*s
c = 2.998E18                 # Angstroms/s
q = system(1,1,1,0.5,lambd)  # Telescope efficiency
a = atmos(0.8,lambd)         # Atmospheric transmission efficiency
R = 50                       # 0.5 meters in centimeters (radius of the 1m telescope)
T = telescope_area(R)        # Area of 1m telescope - use function telescope_area

# User selects to calculate an exposure time
if answer == 1:
    sn = input('Finally, please enter your desired Signal-To-Noise Ratio: ')
    S = sn**2    # Signal-To-Noise ratio is approximately the square root of the Signal - simplification for now

#    Fstar = flux_star(lambd, mag)  # Flux of specified star - flux_star uses flux of Vega as standard

    t = exposure_time(S, q, a, T, h, c, lambd, bandwidth, mag)

    print 'Your recommended exposure time (in seconds) is: ', t

# User selects to calculate Signal-To-Noise Ratio
elif answer == 2:
    seeing = input('Please enter the seeing in units of arcseconds (Default value is 1 arsec): ')
    platescale = input('Please enter the plate scale in units of arseconds/pixel (Default value is 0.5 arcsec/pix): ')
    t = input('Finally, please enter your desired exposure time in seconds: ')
    B = background(21, lambd)
    A = aperture_area(seeing, platescale, lambd)
    Npx = numpix(4, lambd)
    readout = sigma_rn(5, lambd)
    snratio = snr(t, T, h, c, lambd, bandwidth, B, A, Npx, readout, q, a, mag)

    print 'Your estimated Signal-To-Noise Ratio is: ', snratio
