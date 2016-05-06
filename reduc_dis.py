# Data Reduction Package for DIS data taken 28 Mar 2016

from astropy.io import fits
import numpy as np
import glob
from scipy.optimize import curve_fit

path='/home/holtz/raw/apo/mar16/UT160328/'

# Reads image in and returns the data array of the image
def read(file):
  hd=fits.open(file)
  return hd[0].data

# Reads in data for all files in list, subtracts overscan, and returns a median "combined" frame
def combine(filelist):
  comb=[]
  for file in filelist :
     comb.append(overscan_sub(read(file)))
  return np.median(comb, axis=0)

# Add HeNeAr files
def add(filelist):
  comb=[]
  for file in filelist :
     comb.append(overscan_sub(read(file)))
  return np.sum(comb, axis=0)

# Determine mean value of overscan region, subtract that mean from the total image data array
def overscan_sub(image):
  return image-image[10:1070,2060:2090].mean()

# Subtract the bias image from the data image
def biassub(image, bias):
  return image-bias

# Normalize a flat image and divide the entire original data image by the normalized flat
def normalize(image, flat):
  return image/flat

# Linear fit function
def fit_line(x, a, b):
    return a*x + b

# Determine *linear* relationship between wavelength and pixel number
def pix_to_wave(pixarr,wavearr):
  linear = curve_fit(fit_line, pixarr, wavearr)
  [a, b] = linear[0]

  # Test line fit:
  x=np.array([4200,4600,5000])
  y=(a*x)+b

  intarr=np.arange(0,2098,1)
  HeNeAr_wave=(a*intarr)+b
  return intarr, HeNeAr_wave


##########################################################################################
# Choose which image to reduce:
bl_im=path+'160328.0030b.fits'
re_im=path+'160328.0030r.fits'
Heb=path+'LoResHe.0001b.fits'
Her=path+'LoResHe.0001r.fits'
Neb=path+'LoResNe.0001b.fits'
Ner=path+'LoResNe.0001r.fits'
Arb=path+'LoResAr.0001b.fits'
Arr=path+'LoResAr.0001r.fits'


bl_im_sub=overscan_sub(read(bl_im))
re_im_sub=overscan_sub(read(re_im))

# Wavelength Calibration:
####################################################
# Overscan subtract and combine He,Ne,Ar for blue and red separately
bl_HeNeAr_comb=add([Heb,Neb,Arb])
re_HeNeAr_comb=add([Her,Ner,Arr])

# Determine *linear* relationship between wavelength and pixel number
# BLUE
bl_pixel=np.array([1362,1310,1195,1063,914]) # Values retrieved from
bl_wave=np.array([5015,4922,4713,4471,4198]) #   APO website
# Call pixel to wavelength function to convert:
bl_intarr, bl_HeNeAr_wave = pix_to_wave(bl_pixel,bl_wave)

# RED
strip=np.mean(re_HeNeAr_comb[605:650,:],axis=0) # Line is tilted, find average value

# Having a hard time lining up the lines to those on the APO website...
#   Ran out of time before due date :(
re_pixel=np.array([758,966,1212])  # Values retrieved from
re_wave=np.array([6402,6506,6678]) #   APO website

# Call pixel to wavelength function to convert:
re_intarr, re_HeNeAr_wave = pix_to_wave(re_pixel,re_wave)
####################################################


# Overscan subtract and median ("combine") all Hi-Res BrQrtz flat frames
bl_qrtzfiles=glob.glob(path+'BrQrtz.*b.fits')
re_qrtzfiles=glob.glob(path+'BrQrtz.*r.fits')

bl_qrtzcomb=combine(bl_qrtzfiles)
re_qrtzcomb=combine(re_qrtzfiles)

# Divide the resulting flat image out of the resulting data image
bl_final = normalize(bl_im_sub, bl_qrtzcomb)
re_final = normalize(re_im_sub, re_qrtzcomb)
# final frame is now overscan-subtracted, bias-subtracted, and flat-divided.

# final frame doesn't look right?? Looks like something has been subtracted or divided TOO much ... Can't immediately find my error..

# Ran short on time to display the final images with the wavelength calibrations


