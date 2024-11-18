from astropy.io import fits
from astropy import table
import matplotlib.pyplot as plt

# grab the data with 8 being the SC_GEOM HDU index in the FITS file
table_data = table.Table(fits.getdata('legus/frc_fits_files/hlsp_legus_hst_uvis_ngc3344_f336w_v1_drc.fits', 8))

# this is the most elegant way I can think of to grab a 27x153 data
# as a numpy array
array_data = table_data.to_pandas().values

# use Matplotlib to show the image
plt.imshow(array_data)