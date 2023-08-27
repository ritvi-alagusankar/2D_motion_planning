import numpy as np
from shapely.geometry import LineString, Polygon
import scipy.spatial.distance as distance
import pylab as pl
from sklearn.neighbors import NearestNeighbors
class prm(object):
    """
    Class to generate the sample of points and find the nearest neighbours
    of each point. An adjacency list containing the nearest neighbours of each point
    is generated.
    """
    def __init__(self, num_points, env):
        self.env = env
        self.num_points = num_points
        self.xcoords = np.array([])
        self.ycoords = np.array([])
        self.points = np.array([0, 0])
        self.graph = self.graph = [[] for _ in range(num_points + 2)]

    def gen_sample_points(self, size_x : int, size_y : int) -> (np.array([]), np.array([])):
        """
        This method generates a random sample of points
        """
        self.xcoords = np.random.rand(self.num_points) * size_x
        self.ycoords = np.random.rand(self.num_points) * size_y
        return (self.xcoords, self.ycoords)


    def valid_points(self, xcoords : np.array([]), ycoords : np.array([])) -> np.array([[]]):
        """
        This method is used to check for the validity of each point in the sample
        that we generated. It returns only the points which are free (:- not in the obstacle)
        """
        # Add the start coordinates to the start of the numpy array
        self.points = np.vstack(
            [self.points, [self.env.x_start, self.env.y_start]])
        for i in range(len(xcoords)):
            if not self.env.check_collision(xcoords[i], ycoords[i]):
                # If the point is not in any of the obstacles we add it to points
                pl.scatter(xcoords[i], ycoords[i], c='b', s=1)
                self.points = np.vstack(
                    [self.points, [xcoords[i], ycoords[i]]])
        # Add the goal coordinates to the end of the numpy array
        self.points = np.vstack(
            [self.points, [self.env.x_goal, self.env.y_goal]])
        self.points = self.points[1:]
        return self.points

    def check_dist(self) -> list:
        """
        This is a method of finding nearest neighbours using cdist.
        We obtain the euclidean distance of 20 closest points which are valid
        and append it to the adjacency list.
        """
        for coordinate, p in enumerate(self.points):
            k = 20
            # We obtain the neighbours of each point
            d = distance.cdist(p.reshape(1, -1), self.points, 'euclidean').flatten()
            neighbour_index = np.argpartition(d, 40)[:40]

            for neighbour in neighbour_index:
                if k >= 0:
                    end = self.points[neighbour]
                    if self.checkline_col(p, end):
                        continue
                    else:
                        # We keep traversing until we obtain 20 neighbours of each point
                        k = k - 1
                        # Append the index of the neighbour and its distance from the point to graph
                        self.graph[coordinate].append((neighbour, d[neighbour]))
                        # We obtain an adjacency list for each point
        return self.graph

    def check_knn(self) -> list:
        """
        This is a method of finding nearest neighbours using KNN algorithm.
        We obtain the nearest neighbours and append it to the adjacency list.
        """
        model = NearestNeighbors(n_neighbors=20, radius=0.4)

        # Fits the model to the sample points
        model.fit(self.points)

        # Gets the distances and indices of the nearest neighbors for each node
        d, indices = model.kneighbors(self.points)
        # Iterate through the indices and distances for each node
        for ind, coordinates in enumerate(self.points):

            # Iterates through all the neighbors of the node
            for j, neighbor in enumerate(self.points[indices[ind][1:]]):
                # Checks if line joining the coordinate and neighbour point passes through any of the obstacles
                if self.checkline_col(coordinates, neighbor):

                    continue
                else:
                    self.graph[ind].append((indices[ind][j+1], d[ind][j + 1]))
        return self.graph


    def checkline_col(self, start, end) -> bool:
        """
        This method is used to check if the line joining the start and end point
        passes through any of the obstacles
        """
        line = LineString([start, end])
        for ob in self.env.obs:
            obstacleShape = Polygon([[ob.x0, ob.y0], [ob.x1, ob.y1], [ob.x2, ob.y2]])
            if line.intersects(obstacleShape):
                # Returns true if the line intersects any of the obstacles
                return True
        return False