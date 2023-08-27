import pylab as pl
import numpy
class Dijkstra_PRM(object):
    """
    To find the shortest distance from start to goal and return the path
    """
    def shortest_distance(self, points : numpy.array([[]]), graph : list, num_points : int) -> list:
        """
        This method utilizes Dijkstra's algortithm to find the shortest distance from start to goal.
        Notes down the previous nodes connecting each node in its shortest path from the source.
        """
        import heapq
        pq = []
        heapq.heappush(pq, (0, 0))
        # We initialize all distances as infinite
        dist = [float('inf')] * (num_points + 2)
        prev = [float('inf')] * (num_points + 2)
        dist[0] = 0
        # Set distance of the source point to be 0
        while pq:
            d, u = heapq.heappop(pq)
            for v, weight in graph[u]:
                # Check if there is a shorter path to v through u.
                if dist[v] > dist[u] + weight:
                    # Updating distance of v
                    dist[v] = dist[u] + weight
                    prev[v] = u
                    # Previous node is added to the list
                    heapq.heappush(pq, (dist[v], v))

        return self.shortest_path(prev, len(points) - 1)

    def shortest_path(self, prev_node : list, end : int) -> list:
        """
        The list containing the previous nodes of each node is utilized to generate the shortest path
        """
        # The first node is the goal point, and we obtain the previous node of goal
        p_node = prev_node[end]
        path = [end]
        while p_node != float('inf'):
            # We keep iterating through the previous nodes till we reach the source, and thus we obtain the path in reverse
            path.append(p_node)
            temp = p_node
            p_node = prev_node[temp]
        path.reverse() # Correct order of path is obtained
        if(len(path) == 1):
            return [-1]
        else:
            return path
    def plot_path(self, path : list, points : numpy.array([[]])) -> None:
        for i in range(1, len(path)):
            start = path[i - 1]
            end = path[i]
            pl.plot([points[start][0], points[end][0]],[points[start][1], points[end][1]], c = 'y')
            pl.scatter(points[start][0], points[start][1], c = 'y')
        pl.scatter(points[path[len(path)-1]][0], points[path[len(path)-1]][1], c = 'y')
