import numpy as np

# 1)
# Estimate the number of photons/second you would receive for a star with V=22 with the NMSU 1m 
# assuming that the combined detection efficiency of the telescope and detector is 50 percent. 
# You can assume that the V bandpass is rectangular with a central wavelength of 5500 A, a full 
# width of 1000 A, with an in-band transmission of 80 percent.
#

# Number of photons/second:
# Define constants (all in cgs!):
h = 6.626E-27           # erg*s
c = 2.998E18            # Angstroms/s

lambd = 5500.0          # Angstroms
q = 0.5                 # Telescope efficiency
a = 0.8                 # Atmospheric transmission efficiency
R = 50                  # 0.5 meters in centimeters (radius of the 1m telescope)
T = np.pi*(R**2.0)      # Area of 1m telescope


mag = 22.0
Fvega = 3.6E-9          # Flux of Vega at 5500A. Units: ergs/cm2/s/A
Fstar = Fvega*10.0**(mag/(-2.5))


lambd_initial = 5000.0  # Angstroms
lambd_final = 6000.0    # Angstroms

S = q*a*T*Fstar/(h*c) * 0.5*((lambd_final**2.0) - (lambd_initial**2.0))
 # Constants out front..|..Output of integral

print 'Number of photons/second: ', S
# Number of photons/second outputted by program is: ~4.963 photons/second


#--------------------------------------------------------------------------------------------------------

# 2)
# What is the zeropoint for the V bandpass for the 1m, using the approximate:
#
# standardmag = - 2.5*log(photons/s) + zeropoint
standardmag = 0.0
zp = standardmag + 2.5*np.log10(S)

print 'The zeropoint for the 1m in the V-band is: ', zp
# Zeropoint outputted by program is: ~1.74 mag

