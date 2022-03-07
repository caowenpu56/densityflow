import pickle
import os
import networkx as nx

dataPath = os.getcwd()
if __name__ == '__main__':
    if not os.path.exists('%s/Result/DensityFlow/' % (dataPath)):
        os.makedirs('%s/Result/DensityFlow/' % (dataPath))

    # {density threshold: {population cluster id: area}}
    fr = open('%s/Data/clusterAreas.pkl' % (dataPath), 'rb')
    clusterAreas = pickle.load(fr)
    fr.close()

    # {density threshold: {origin population cluster id: {destination population cluster id: flow}}}
    fr = open('%s/Data/clusterFlows.pkl' % (dataPath), 'rb')
    clusterFlows = pickle.load(fr)
    fr.close()

    # {density threshold: {flow threshold: {urban cluster id: {population cluster id: area} }}}
    densityFlowClusters = {}
    for dThres in clusterFlows:
        densityFlowClusters[dThres] = {}

        dThresClusterFlows = clusterFlows[dThres]
        # iterate over all possible flow ratio thresholds
        for fThresIndex in range(101):
            fThres = fThresIndex / 100.0

            nodes = {}
            edges = []
            for o in dThresClusterFlows:
                flows = dThresClusterFlows[o].copy()
                flows = dict(sorted(flows.items(), key=lambda item: item[1], reverse=True))
                if o in flows:
                    flows.pop(o)
                if len(flows) == 0:
                    continue
                # each population is connnected to the cluster with the largest flow ratio
                d = list(flows.keys())[0]
                ratio = flows[d]
                if o not in nodes:
                    nodes[o] = 1
                if d not in nodes:
                    nodes[d] = 1
                if ratio > fThres:
                    edges.append((o, d))

            # merge connected population clusters into one urban cluster
            clusters = {}
            nodes = list(nodes.keys())
            graph = nx.Graph()
            graph.add_nodes_from(nodes)
            graph.add_edges_from(edges)
            for component in nx.connected_components(graph):
                uID = len(clusters) + 1
                clusters[uID] = {}
                for cLabel in component:
                    clusters[uID][cLabel] = clusterAreas[dThres][cLabel]

            densityFlowClusters[dThres][fThresIndex] = clusters

    fw = open('%s/Result/DensityFlow/DensityFlow.pkl' % (dataPath), 'wb')
    pickle.dump(densityFlowClusters, fw)
    fw.close()