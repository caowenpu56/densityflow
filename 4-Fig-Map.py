import os
import numpy as np
import pickle
import rasterio

# Convert the numpy array to Geotiff
def Write2Tiff(data, meta, filename):
    tiff = rasterio.open(filename, 'w', **meta)
    tiff.write(data)
    tiff.close()

dataPath = os.getcwd()
if __name__ == '__main__':
    fr = open('%s/Result/DensityFlow/DensityFlow.pkl' % (dataPath), 'rb')
    # {density threshold: {flow threshold: {urban cluster id: {population cluster id: area} }}}
    urbanClusters = pickle.load(fr)
    fr.close()

    phaseThresholds = {1: (0, 0), 2: (10, 0), 3: (20, 2), 4: (50, 2), 5: (210, 5), 6: (330, 28)}
    for phase in phaseThresholds:
        dThres = phaseThresholds[phase][0]  # population density threshold
        fThres = phaseThresholds[phase][1]  # flow ratio threshold

        ccaTiff = rasterio.open('%s/Result/PCCA/cca_thres%d.tif' % (dataPath, dThres))
        ccaData = ccaTiff.read(1)
        ccaMeta = ccaTiff.meta.copy()
        ccaTiff.close()
        rRows, rCols = ccaMeta['height'], ccaMeta['width']
        ccaMeta['dtype'] = 'int32'
        ccaMeta['compress'] = 'lzw'

        # population_cluster_id to urban cluster_id
        cID2uID = {}
        for uID in urbanClusters[dThres][fThres]:
            for cID in urbanClusters[dThres][fThres][uID]:
                cID2uID[cID] = uID

        # construct urban cluster map (GeoTIFF)
        urbanTiffData = np.zeros((rRows, rCols))
        for i in range(rRows):
            for j in range(rCols):
                if ccaData[i][j] in cID2uID:
                    urbanTiffData[i][j] = cID2uID[ccaData[i][j]]

        if not os.path.exists('%s/Result/UrbanClusters/' % (dataPath)):
            os.makedirs('%s/Result/UrbanClusters/' % (dataPath))
        urbanTiff = '%s/Result/UrbanClusters/UrbanCluster_%d_%d.tif' % (dataPath, dThres, fThres)
        Write2Tiff(urbanTiffData[np.newaxis, :].astype(ccaMeta['dtype']), ccaMeta, urbanTiff)