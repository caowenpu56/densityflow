import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from math import log10
from mpl_toolkits.axes_grid1 import make_axes_locatable
from sklearn.cluster import KMeans
import seaborn as sns

textSize = 8
tickSize = 6
barColor = '#4751b0'
lineWidth = 1

dataPath = os.getcwd()
if __name__ == '__main__':
	scaleX = 100   # 0, 10, 20, 30, ... , 1000 people/km2 (unscaled)
	scaleY = 100   # 0%, 1%, ... , 100%
	popScale = 13827100000/99724732  # scale factor

	fr = open('%s/Result/DensityFlow/DensityFlow.pkl' % (dataPath), 'rb')
	# {density threshold: {flow threshold: {urban cluster id: {population cluster id: area} }}}
	urbanClusters = pickle.load(fr)
	fr.close()

	phase = np.zeros((scaleX, scaleY))
	for dThres in range(scaleX):
		for fThres in range(scaleY):
			clusterSizes = []
			for uID in urbanClusters[dThres * 10][fThres]:
				# area of urban cluster = sum of (area of population cluster within the urban cluster)
				clusterSize = np.array(list(urbanClusters[dThres * 10][fThres][uID].values())).sum()
				clusterSizes.append(clusterSize)
			sizeArray = np.array(clusterSizes)
			sizeArray.sort()
			largestSize = sizeArray[len(sizeArray) - 1]
			phase[dThres][fThres] = log10(largestSize)

	# Plot the density-flow phase diagram
	fig = plt.figure(figsize=(7, 3.5), dpi=600)
	gs = fig.add_gridspec(2, 4)

	ax_phase = fig.add_subplot(gs[:, 0: 2])
	scPhase = ax_phase.imshow(phase, cmap='RdYlBu_r', origin='lower', aspect='auto')
	ax_phase.set_xticks(range(0, scaleX, 10))
	ax_phase.set_yticks(np.arange(0, 14000, 1000) / popScale, np.arange(0, 14000, 1000))
	ax_phase.set_title('Largest cluster', fontsize=textSize)
	ax_phase.set_xlabel('Flow ratio (%)', fontsize=textSize)
	ax_phase.set_ylabel('Density (people/$km^2$)', fontsize=textSize)
	ax_phase.tick_params(labelsize=tickSize)
	dividerPhase = make_axes_locatable(ax_phase)
	caxPhase = dividerPhase.append_axes('right', size='5%', pad=0.05)
	cbarPhase = fig.colorbar(scPhase, ax=ax_phase, cax=caxPhase)
	cbarPhase.ax.tick_params(labelsize=tickSize)
	cbarPhase.ax.set_yticks([3, 4, 5], ['$10^{3}$', '$10^{4}$', '$10^{5}$'])
	cbarPhase.ax.set_title('Area($km^2$)', fontsize=tickSize)

	# Plot the histogram
	dataset = []
	for i in range(phase.shape[0]):
		for j in range(phase.shape[1]):
			dataset.append([phase[i, j]])
	kmeans = KMeans(n_clusters=7, max_iter=10000, tol=1e-10, random_state=0)
	fit = kmeans.fit(dataset)

	ax_hist = fig.add_subplot(gs[0, 2: 4])
	values = phase.flatten()
	sns.histplot(values, ax=ax_hist, bins=100, color=barColor, kde=False, stat='probability', element='bars')
	labelTransfrom = {}
	prevLabel = -1
	newLabel = 1
	intervalNum = 10000
	interval = (values.max() - values.min()) / intervalNum
	for i in range(intervalNum + 1):
		curV = values.min() + interval * i
		label = fit.predict([[curV]])[0]
		if prevLabel != label:
			labelTransfrom[label] = newLabel
			newLabel += 1
			prevLabel = label
			if newLabel != 3:
				ax_hist.axvline(curV, c='gray', ls='dotted', lw=lineWidth)
	ax_hist.tick_params(labelsize=tickSize)
	ax_hist.set_xlabel('Largest area ($km^2$)', fontsize=textSize)
	ax_hist.set_ylabel('Density', fontsize=textSize)
	ax_hist.set_xticks([3, 4, 5], ['$10^{3}$', '$10^{4}$', '$10^{5}$'])

	groupPhase = np.zeros((scaleX, scaleY))
	for i in range(phase.shape[0]):
		for j in range(phase.shape[1]):
			label = fit.predict([[phase[i, j]]])[0]
			groupPhase[i, j] = labelTransfrom[label]

	for l in range(3, 4):
		array2d = groupPhase.copy().astype(int)
		array2d[array2d != l] = 0
		for i in range(array2d.shape[0]):
			for j in range(array2d.shape[1]):
				if array2d[i, j] != 0:
					if j > 0:
						if array2d[i, j - 1] == 0:
							ax_phase.plot([j - 0.5, j - 0.5], [i - 0.5, i + 0.5], lw=0.5, color='black')
					if j < array2d.shape[1] - 1:
						if array2d[i, j + 1] == 0:
							ax_phase.plot([j + 0.5, j + 0.5], [i - 0.5, i + 0.5], lw=0.5, color='black')
					if i > 0:
						if array2d[i - 1, j] == 0:
							ax_phase.plot([j - 0.5, j + 0.5], [i - 0.5, i - 0.5], lw=0.5, color='black')
					if i < array2d.shape[0] - 1:
						if array2d[i + 1, j] == 0:
							ax_phase.plot([j - 0.5, j + 0.5], [i + 0.5, i + 0.5], lw=0.5, color='black')

	newPhase = phase[0: 10, 0: 20]
	ax_label = fig.add_subplot(gs[1, 2: 4])
	scLabel = ax_label.imshow(newPhase, cmap='RdYlBu_r', origin='lower', aspect='auto', vmin=phase.min(), vmax=phase.max())
	ax_label.set_yticks(np.arange(0, 1380, 200) / popScale, np.arange(0, 1400, 200))
	ax_label.set_xticks(range(0, 20, 2))
	ax_label.tick_params(labelsize=tickSize)

	groupPhase = groupPhase[0: 10, 0: 20]
	for l in range(4, 7):
		array2d = groupPhase.copy().astype(int)
		array2d[array2d != l] = 0
		for i in range(array2d.shape[0]):
			for j in range(array2d.shape[1]):
				if array2d[i, j] != 0:
					if j > 0:
						if array2d[i, j - 1] == 0:
							ax_label.plot([j - 0.5, j - 0.5], [i - 0.5, i + 0.5], lw=0.5, color='black')
					if j < array2d.shape[1] - 1:
						if array2d[i, j + 1] == 0:
							ax_label.plot([j + 0.5, j + 0.5], [i - 0.5, i + 0.5], lw=0.5, color='black')
					if i > 0:
						if array2d[i - 1, j] == 0:
							ax_label.plot([j - 0.5, j + 0.5], [i - 0.5, i - 0.5], lw=0.5, color='black')
					if i < array2d.shape[0] - 1:
						if array2d[i + 1, j] == 0:
							ax_label.plot([j - 0.5, j + 0.5], [i + 0.5, i + 0.5], lw=0.5, color='black')

	fig.tight_layout()
	fig.savefig('%s/1Phase.eps' % (dataPath), bbox_inches='tight', dpi=600, pad_inches=0.1)