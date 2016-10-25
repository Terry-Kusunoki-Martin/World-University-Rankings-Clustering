from unsupervisedLearning import *
from nltk import Tree
import random

def main():
    c = HierarchicalClustering("universities.points", "universities.labels")
    print c.tree
    c.plotTree()

class HierarchicalClustering(UnsupervisedLearning):
    """
    A class to build agglomerative clusters from the bottom up.
    """
    def __init__(self, pointFile, labelFile):
        """The dictionary self.distances is keyed a on pair of clusters, and
        stores the distance between them.

        self.distances is a dictionary with keys (clusterName1, clusterName2)
        and values dist(clusterName1, clusterName2) used to store
        computations so they don't have to be recomputed during iterarions
        of building the tree

        self.centroids is a dictionary with cluster names as keys and cluster
        centroid points as values. The centroid of a cluster is the point
        where each dimension's value is the average value of that dimension
        over all points in the cluster.

        self.tree is represented as a tuple of the form (root, left, right).
        """
        UnsupervisedLearning.__init__(self, pointFile, labelFile)
        self.distances = {} # caches distance computations we may need again
        self.centroids = {} # maps clusters to centroids
        self.pointcounts = {} # maps clusters to num_points
        self.labelcount = 0
        # replace this with another function to explore other
        # measures of cluster similarity

        self.closestClusters = self.averageLinkClosest
        self.tree = self.buildTree()

    def initClusters(self):
        """
        Initializes the self.centroids dictionary to map the original
        labels to their points.  Also initializes all point counts in
        self.pointcounts to 1.
        """
        if len(self.labelList) != len(self.pointList):
        	raise ValueError("Label List and Point List not the same length!")
        for i in range(len(self.labelList)):
            self.centroids[self.labelList[i]] = self.pointList[i]
            self.pointcounts[self.labelList[i]] = 1


    def averageLinkClosest(self):
        """
        Finds the distance between each pair of clusters and returns the
        labels of the two closest clusters (according to the average link
        criterion).

        Uses the class variable self.distances to store and reuse previous
        distance calculations.
        """
        #bestDist stores lowest dist between labels along with the labels themselves
        bestDist = (float("inf"), None, None)
        for l1 in self.centroids:
            for l2 in self.centroids:
                if l1 == l2:
                    pass
                else:
                    d = self.getDistance(l1, l2)
                    if d < bestDist[0]:
                        bestDist = (d, l1, l2)
        return (bestDist[1], bestDist[2])

    def getNumPoints(self, l1, l2):
        """
        returns tuple containing number of points contained in centroid 1 and centroid 2.
        Used in simplifying centroid combination
        """
        n1 = self.pointcounts[l1]
        n2 = self.pointcounts[l2]
        self.pointcounts[('Cl_%d' % self.labelcount, l1, l2)] = n1 + n2
        return (n1, n2)

    def getDistance(self, l1, l2):
        if (l1, l2) in self.distances:
            return self.distances[(l1, l2)]
        else:
            d = self.dist(self.centroids[l1], self.centroids[l2])
            self.distances[(l1, l2)] = d
            return d


    def buildTree(self):
        """
        Starting with each point as its own cluster, initializes the
        dictionary self.centroids that maps cluster labels to their
        center points.

        Repeatedly calls self.closestClusters to calculate the distances
        between all current clusters and find the pair with the minimum
        distance, clusterA and clusterB.  Removes clusterA and clusterB from
        the centroids dictionary and adds a new cluster with key:
        (clNUM, clusterA, clusterB).  Where the root is named using a
        counter NUM that is incremented after each cluster is formed.
        The value for this key is the centroid of the new cluster, which
        is the average of the original cluster points for clusterA and
        clusterB. Continues this process until there is a single cluster
        joining together all points.

        The key of this final single cluster is a tuple in the form:
        (root, branch, branch) where each branch has the same format.
        The tuple represents the clustering tree. The leaves of this
        tree are the labels of the orginal points.

        The unique (root, branch, branch) key remaining in self.centroids
        is returned.
        """
        self.initClusters()
        while len(self.centroids) > 1:
            print "Iteration %d" % self.labelcount
            for i in self.centroids:
            	print self.centroids[i], i
            
            l1, l2 = self.closestClusters()
            n1, n2 = self.getNumPoints(l1, l2)

            self.centroids[('Cl_%d' % self.labelcount, l1, l2)] = \
            (n1*self.centroids[l1] + n2*self.centroids[l2])/(n1 + n2)
            
            del self.centroids[l1]
            del self.centroids[l2]
            self.labelcount += 1


        return ('Cl_%d' % (self.labelcount-1), l1, l2)


        
    def plotTree(self):
        """
        Builds and plots a tree using the NLTK library.
        """
        t = self.make(self.tree)
        t.draw()

    def make(self, tree):
        """
        Recursively creates the tree using the tuple that was constructed
        in buildTree.
        """
        if type(tree) != type(()):
            return tree
        return Tree(tree[0], [self.make(tree[1]), self.make(tree[2])])
            
if __name__ == '__main__':
    main()
