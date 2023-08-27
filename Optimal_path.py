import random
import numpy
class PostProcessing(object):
    def optimal_path(self, prm : object, path : list, points : numpy.array([[]])) -> list:
        """
        Post-processing : To obtain the most optimal path by applying shortcuts to the
        path returned by Dijkstra's algorithm
        """
        if (len(path) > 2):
            rep = 250 # Set maximum number of repitions to 250
            while (rep > 0):
                a = random.randint(0, len(path)-1)
                b = random.randint(0, len(path)-1)
                # a and b are the two shortcut points which are randomly generated
                if(a > b):
                    a, b = b, a
                    # Set a to be lower value to prevent error while indexing
                if not prm.checkline_col(points[path[a]], points[path[b]]):
                    del path[a+1:b]
                    # Removes the elements between the two points in the path
                rep = rep - 1
            return path

        else:
            return path
    def optimal_path_two_pointer(self, prm : object, path : list, points : numpy.array([[]])) -> list:
        """
        Post-processing : To obtain the most optimal path by applying the two point method
        to the path returned by Dijkstra's algorithm
        """
        if (len(path) > 2):
            # We add source to path
            opt_path = [0]
            left = 0
            right = len(path) - 1
            while (left < len(path) - 1):
                """
                We check line collision with obstacles between the two points, 
                if there is no collision then the path is shortcut
                """
                if not prm.checkline_col(points[path[left]], points[path[right]]):
                    opt_path.append(path[right])
                    #Valid point is added to path and left pointer is updated
                    left = right
                    right = len(path) - 1
                    continue
                right = right - 1
            return opt_path
        else:
            return path