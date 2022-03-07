import os
import numpy as np
import rasterio
from scipy.ndimage import label, generate_binary_structure

# Convert the numpy array to Geotiff
def Write2Tiff(data, meta, filename):
    tiff = rasterio.open(filename, 'w', **meta)
    tiff.write(data)
    tiff.close()

dataPath = os.getcwd()
if __name__ == '__main__':
    # Read the population density data
    popTiff = rasterio.open('%s/Data/HomeDensity_CHN.tif' % (dataPath))
    densityData = popTiff.read(1)
    meta = popTiff.meta.copy()
    popTiff.close()

    savePath = '%s/Result/PCCA/' % (dataPath)
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    # iterate over all possible population density thresholds
    values = np.unique(np.floor(densityData / 10))
    thresholds = np.intersect1d(values[values >= 0], values[values <= 300]) * 10
    thresholds.sort()

    meta['dtype'] = 'int32'
    meta['nodata'] = 0
    meta['compress'] = 'lzw'
    for t in thresholds:
        # merge grids with values larger than the thresholds into clusters (8-neighbors)
        ccaData, ccaNum = label((densityData > t), generate_binary_structure(2, 2))
        Write2Tiff(ccaData[np.newaxis, :], meta, '%scca_thres%d.tif' % (savePath, t))