# Data Reduction Package for ARCTIC data taken 27 Mar 2016

from astropy.io import fits
import numpy as np
import glob

path='/home/holtz/raw/apo/mar16/UT160327/'

# Reads image in and returns the data array of the image
def read(file):
  hd=fits.open(file)
  return hd[0].data


im=path+'160327.0069.fits'
dataim = read(im)

# Need to set up a for loop for the below in order to get ALL bias frames
# Attempted this below, but ran out of time before due date.

#biasfiles=glob.glob(path+'ARCTIC_Bias.*.fits')
#print biasfiles

#bi=[[[0]*n]*n]*n
#for i in range(len(biasfiles)):
#  bi[i] = read(biasfiles[i])
#  print bi[i]

bias1=path+'ARCTIC_Bias.0002.fits'
bi1=read(bias1)
bias2=path+'ARCTIC_Bias.0007.fits'
bi2=read(bias2)
bias3=path+'ARCTIC_Bias.0014.fits'
bi3=read(bias3)
bias4=path+'ARCTIC_Bias.0020.fits'
bi4=read(bias4)
bias5=path+'ARCTIC_Bias.0025.fits'
bi5=read(bias5)

# Need to set up a for loop for the below in order to get ALL flats
flat1=path+'BrQrtz_661.0028.fits'
fl1=read(flat1)
flat2=path+'BrQrtz_661.0030.fits'
fl2=read(flat2)
flat3=path+'BrQrtz_661.0032.fits'
fl3=read(flat3)



# Determine mean value of overscan region, subtract that mean from the total image data array
def overscan_sub(image):
  return image-image[10:2030,2060:2090].mean()

# Subtract the bias image from the data image
def biassub(image, bias):
  return image-bias

# Normalize a flat image and divide the entire original data image by the normalized flat
def normalize(image, flat):
  return image/flat


# Subtract overscan region from ALL files
bim = overscan_sub(dataim)
b1 = overscan_sub(bi1)
b2 = overscan_sub(bi2)
b3 = overscan_sub(bi3)
b4 = overscan_sub(bi4)
b5 = overscan_sub(bi5)

f1 = overscan_sub(fl1)
f2 = overscan_sub(fl2)
f3 = overscan_sub(fl3)

# Combine the bias images and flat images into "median"-style average images
bc = np.array([b1,b2,b3,b4,b5])
biascomb = np.median(bc, axis=0)

fc = np.array([f1,f2,f3])
flatcomb = np.median(fc, axis=0)

# Subtract combined bias frame from data image and combined flat frame
im_biassub = biassub(bim, biascomb)
fl_biassub = biassub(flatcomb, biascomb)

# Divide the resulting flat image out of the resulting data image
final = normalize(im_biassub, fl_biassub)
# final frame is now overscan-subtracted, bias-subtracted, and flat-divided.


