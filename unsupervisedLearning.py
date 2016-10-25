import numpy as np
import math

def main():
    ul = UnsupervisedLearning("small.points", "small.labels")
    print "\nLABELS"
    print ul.labelList
    print "\nPOINTS"
    print ul.pointList
    print "\nDICTIONARY of tuple(point) to label"
    print ul.pointToLabel

class UnsupervisedLearning(object):
    """
    A parent class for unsupervised learning techniques.
    """
    def __init__(self, pointFile, labelFile=""):
        """
        Given a file of points (one point per line, with each dimension
        separated by whitespace) and given a file of unique labels for
        each point (one label per line, interpreted as strings), create
        a tree that clusters the points based on Euclidean distance in
        a greedy fashion.

        pointList is a list of numpy array objects
        labelList is a list of string labels associated with each point
        pointToLabel is a dictionary that maps a tuple of each point to its
        label
        """
        self.pointList = self.getPoints(pointFile)
        self.labelList = self.getLabels(labelFile)
        self.pointToLabel = self.makePointDict()

        # replace this with another function to explore other distance measures
        self.dist = self.EuclideanDist

    def makePointDict(self):
        """
        Builds the pointToList dictionary.
        """
        d = {}
        for i in range(len(self.pointList)):
            d[tuple(self.pointList[i])] = self.labelList[i]
        return d

    def EuclideanDist(self, p1, p2):
        """
        Given two numpy arrays representing points, calculates the Euclidean
        distance between them by finding their difference, squaring it, and
        then taking the square root.
        """
        return np.linalg.norm(p1 - p2, 2)

    def getLabels(self, filename):
        """
        Expects file to contain one string per line representing a unique
        label for each corresponding data point.  
        Returns: A list of labels as strings
        """
        fp = open(filename, "r")
        labels = []
        for line in fp:
            label = line.strip()
            labels.append(label)
        fp.close()
        return labels

    def getPoints(self, filename):
        """
        Expects file to contain one pattern per line.  Each pattern consists
        of a sequence of floating point value in the range [0,1] separated by 
        whitespace.
        Returns: A list of data points as numpy arrays
        """
        fp = open(filename, "r")
        points = []
        for line in fp:
            data = line.strip().split()
            data = [float(x) for x in data]
            data = np.array(data)
            points.append(data)
        fp.close()
        return points

if __name__ == '__main__':
    main()
