import numpy as np
import pylab as pl
import sys
sys.path.append('/')
import environment_2d
import PRM
import Dijkstra
import Optimal_path

pl.ion()
np.random.seed(4)
size_x = 10
size_y = 6
no_obs = 5
no_pts = 600
env = environment_2d.Environment(size_x, size_y, no_obs)
prm_plan = PRM.prm(no_pts, env)
djk = Dijkstra.Dijkstra_PRM()
post_process = Optimal_path.PostProcessing()
pl.clf()

env.plot()
q = env.random_query()

if q is not None:
  x_start, y_start, x_goal, y_goal = q
  env.plot_query(x_start, y_start, x_goal, y_goal)

# Generate sample points
xcoords, ycoords = prm_plan.gen_sample_points(size_x, size_y)
# Find valid sample points and plot them
points = prm_plan.valid_points(xcoords, ycoords)
# Find the nearest neighbours of points and return the graph containing adjacency lists
graph = prm_plan.check_dist()
# graph = prm_plan.check_knn() - KNN can also be used
# Find the shortest path using the Dijkstra's algorithm
path = djk.shortest_distance(points, graph, no_pts)


if path == [-1]:
  print("Could not find path to goal")
else:
  # djk.plot_path(path, points) To plot graph before Post-Processing
  print("Path : ", path)
  optimal = post_process.optimal_path(prm_plan, path, points)
  #optimal = post_process.optimal_path_two_pointer(prm_plan, path, points) Two pointer method of post-processing
  print("Optimal Path after path shortcutting : ", optimal)
  djk.plot_path(optimal, points)

pl.show(block=True)
pl.close()

