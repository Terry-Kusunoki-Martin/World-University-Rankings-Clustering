from unsupervisedLearning import *
import matplotlib.pyplot as plt
import numpy as np
import math
import random
from time import sleep

def main():
    kmeans = KMeans(3, "universities.points", "universities.labels")
    kmeans.findCentroids()


class KMeans(UnsupervisedLearning):
    """
    A class to implement Kmeans.
    """
    def __init__(self, k, pointFile, labelFile):
        """k is the number of centroids to create when clustering.

        centroids is a dictionary that maps each label 'c1', 'c2', ..., 'ck'
        to a centroid point, represented as an array.

        members is a dictionary that maps each label to a list of points
        in that label, represented as arrays.

        labels is a dictionary that maps a tuple representation of each point
        to its current cluster label
        """
        UnsupervisedLearning.__init__(self, pointFile, labelFile)
        self.k = k
        self.centroids = {}
        self.members = {}
        self.labels = {}
        self.error = 0
        self.updateFlag = False

    def showClusters(self, verbose=False):
        """Display data about each cluster, including its centroid,
        the number of points assigned to it. When verbose is True 
        also show each of the member points."""
        print "Current error:", self.error
        for key in self.centroids:
            print "-"*20
            print "Cluster:", key, "Length:", len(self.members[key])
            print "Cluster point:", 
            self.showPoint(self.centroids[key])
            if verbose:
                for point in self.members[key]:
                    self.showPoint(point)

    def showPoint(self, point):
        """Compactly display a point using 3 decimal places per dimension.
        If it has a label in the labels dictionary, show this as well.
        """
        for floatVal in point:
            print "%.3f" % floatVal,
        if tuple(point) in self.labels:
            print self.labels[tuple(point)]
        else:
            print

    def plotClusters(self):
        """Plots 2d data about each centroid and its members.  Uses 8 unique
        colors.  When the number of centroids is 8 or less, each cluster
        will have a unique color.  Otherwise colors will be repeated.
        The centroid of each cluster is plotted as an x, all other points
        are plotted aas o's.
        """
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        for i,cluster in enumerate(self.centroids.keys()):
            plt.xlim(0,1)
            plt.ylim(0,1)
            x = [p[0] for p in self.members[cluster]]
            y = [p[1] for p in self.members[cluster]]
            plt.plot(x, y, colors[i%len(colors)]+ 'o')
            centroid = self.centroids[cluster]
            plt.plot(centroid[0], centroid[1], colors[i%len(colors)]+ 'x')
        plt.show()
    
    def initClusters(self):
        """Chooses random data points to be the initial cluster centroids.

        k unique random points from self.points are selected as initial
        cluster centroids.
        The centroids dictionary is initialized to map each cluster label
        to one of these centroid points.
        The members dictionary is initialized to map each cluster label
        to an empty list.
        """
        indlist = range(len(self.labelList))
        for i in range(self.k):
            ind = random.choice(indlist)
            while self.labelList[ind] in self.centroids:
                ind = random.choice(indlist)
            self.centroids[self.labelList[ind]] = self.pointList[ind]


    def assignPoints(self):
        """E step: assigns every point to the closest centroid.
        Returns True or False, indicating whether any points changed clusters.

        Uses self.dist() to find the closest centroid to each point.
        Loops over points one cluster at a time, according to the old 
        members dictionary, so that as each point is assigned to a cluster
        in the new members dictionary, it can easily be determined whether
        that point has switched clusters.

        Also updates self.error, by initializing it to zero and keeping track
        of the squared distance from each point to its assigned centroid.
        """
        for p in self.pointList:
            dist, cl = self.findClosestCentroid(p)
            self.error += dist**2
            self.members[cl].append(p)
            hashable_p = str([x for x in p])
            if hashable_p in self.labels:
                if self.labels[hashable_p] != cl:
                    self.labels[hashable_p] = cl
                    self.updateFlag = True
            else:
                self.labels[hashable_p] = cl
                self.updateFlag = True




    def findClosestCentroid(self, point):
        bestDist = (float("inf"), None)
        for cl in self.centroids:
            d = self.dist(self.centroids[cl], point)
            if d < bestDist[0]:
                bestDist = (d, cl)
        return bestDist

    def updateCentroids(self):    
        """M step: computes new centroids for each cluster.

        Each cluster's new centroid is the average along each dimension of
        the points in that cluster. This computation is simplified by the
        fact that points are represented as numpy arrays, which support
        elementwise addition with + and mutliplication/division of all
        elements by a constant.

        The resulting centroid points are stored in the self.centroids dict.
        """
        for cl in self.centroids:
            assigned_pts = self.members[cl]
            new_avg = 0.0
            for p in assigned_pts:
                new_avg += p
            new_avg /= len(assigned_pts)
            self.centroids[cl] = new_avg


    def findCentroids(self):
        """Runs k-means to find a centroid for each of the k clusters.

        Initializes the centroids to random points in the data set. Then
        while the members of a centroid continue to change, the centroids
        are recalibrated and the points are reassigned.

        The  methods initClusters, assignPoints, and updateCentroids
        have been provided for you, but you are encouraged to create
        additional helper methods as needed.
        """
        self.initClusters()
        ct = 0
        while True:
            ct+=1
            self.updateFlag = False
            self.error = 0.0
            for cl in self.centroids:
                self.members[cl] = []
            self.assignPoints()
            print "\n\nITERATION %d\n" % (ct)
            self.showClusters(True)
            self.plotClusters()
            if not self.updateFlag:
                break
            self.updateCentroids()



if __name__ == '__main__':
    main()
