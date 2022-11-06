# Constructing multi-level urban clusters based on population distributions and interactions
by Wenpu Cao, Lei Dong, Ying Cheng, Lun Wu, Qinghua Guo, and Yu Liu

## Abstract
A city (or an urban cluster) is not an isolated spatial unit, but a combination of areas with closely linked socio-economic activities. However, so far, we lack a consistent and quantitative approach to define multi-level urban clusters through these socio-economic connections. Here, using granular population distribution and flow data from China, we propose a bottom-up aggregation approach to quantify urban clusters at multiple spatial scales. We reveal six "phases" (i.e., levels) in the population density-flow diagram, each of which corresponds to a spatial configuration of urban clusters from large to small. Besides, our results show that Zipf's law appears only after the fifth level, confirming the spatially dependent nature of urban laws. Our approach does not need pre-defined administrative boundaries and can be applied effectively on a global scale.

## Replication data and codes
1. Data
- HomeDensity\_CHN: Population density data.
- clusterAreas: Area of each population cluster under each density threshold.
- clusterFlows: Flow ratio between any two population clusters under each density threshold.
2. Codes 
- 1-PCCA: Clustering by population density thresholds.
- 2-DensityFlow: Grouping by flow ratio thresholds
- 3-Phase: Plot the density-flow phase diagram.
- 4-Map: Generate maps of urban clusters at each level.
3. Results
- UrbanClusters: Maps of urban clusters at each level.

Contact: caowenpu56@gmail.com
