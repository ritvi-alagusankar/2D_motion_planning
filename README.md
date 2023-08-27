# 2D_motion_planning

* [About](#about)

* [Finding Nearest Neighbour](#finding-nearest-neighbour)
  
    * [K-Nearest Neighbors Algorithm](#k-nearest-neighbors-algorithm)
  
    * [Euclidean distance (cdist)](#euclidean-distance---cdist)

* [PRM Path](#prm-path)

* [Post Processing](#post-processing)

## About
Probabilistic Roadmap Algorithms serve a crucial role in robotics by facilitating the discovery of collision-free routes between an initial point and a final destination within obstacle-laden maps. Once a path devoid of collisions is established, the integration of a post-processing algorithm, such as the Path Shortcutting algorithm, becomes instrumental. This subsequent step aims to extract the most concise route between the starting point and the target by optimizing the path through sampled points.

## Finding Nearest Neighbour
I used two algorithms to find the nearest neighbours of points:-
* Euclidean distance (cdist) - Requires less number of sample points
* K-Nearest Neighbors Algorithm - Requires more number of sample points
### Euclidean distance - cdist
I found that when utilizing Euclidean distance (cdist) to create the network of nearest neighbours, I only had to use a few samples of points (600) to pass all test cases. 
This is the network created using 600 points (Number of Neighbours per point = 20).
Although the network does not cover the entire area as seen in the picture below, it is able to pass all test cases.
![Cdist 600](https://github.com/Ritzzer764/2D_motion_planning/assets/114499776/de181525-babe-48c6-b1d9-88e6fda66a39)

Observations: Overall the speed for running cdist over 600 points is much faster than running KNN for 5000 points. The issue of less area coverage can be mitigated by increasing the number of sample points, but the run-time increased significantly so I refrained from doing so.

This is the images for the shortest path for the test case (size_x = 10, size_y = 6, number of obstacles = 5):

Path before post-processing (Euclidean distance)            |  Shortest path after path shortcutting (Euclidean distance)
:-------------------------:|:-------------------------:
![spt_img_(10, 6, 5)](https://github.com/Ritzzer764/2D_motion_planning/assets/114499776/5d827173-8dd8-437f-9daa-3a2f4b825e2a) | ![Opt_img_(10, 6, 5)](https://github.com/Ritzzer764/2D_motion_planning/assets/114499776/e5ee4cce-2540-4a3f-9ee7-9f4adc9c6dac) 

### K-Nearest Neighbors Algorithm 

While utilizing the KNN algorithm (Number of Neighbours = 20, radius = 0.4), I found that I had to use more sample points (5000) than cdist to pass all test cases (more pictures are there in the test_images folder).
![Cdist 5000](https://github.com/Ritzzer764/2D_motion_planning/assets/114499776/511dc447-32d0-4505-9b77-858e1bcc39a4)
Although KNN required more points and took more time to run, the network was able to cover a much larger area than cdist due to the number of points as seen above.

This is the shortest path for the test case (size_x = 10, size_y = 6, number of obstacles = 5):
Path before post-processing (KNN)          |  Shortest path after path shortcutting (KNN)
:-------------------------:|:-------------------------:
![KNN_5000_spt](https://github.com/Ritzzer764/2D_motion_planning/assets/114499776/c9749596-9a23-4bea-b5a8-5dc0e3de8ec5)  | ![KNN_5000_opt](https://github.com/Ritzzer764/2D_motion_planning/assets/114499776/f43bdcec-84cd-4cea-9ac6-ae452c052091)

## PRM Path
### Dijkstra's algorithm
Dijkstra's algorithm is used for finding the shortest path from a starting point to a destination. It works by exploring neighboring points, picking the one that's closest to the starting point, and gradually moving towards the destination. It keeps track of distances as it goes along, ensuring it always takes the shortest route available. Once it reaches the goal, it traces back its steps to reveal the optimal path that leads from the source to the destination.
The PRM path for the given problem is obtained using the Dijkstra's Algorithm

## Post Processing 
The paths found by the planning methods of Section Path planning are collision-free but might not be optimal in terms of path length. 
The following two approaches can be utilized to optimize the PRM path obtained: 
* Shortcut Method
* Two pointer Method

### Shortcut Method
1) Utilize the path from the Dijkstra's algorithm. Pick 2 random nodes and check if the line created by joining them is valid (:- does not intersect an obstacle)
2) If the line created is valid, delete all elements between the two points in the path, and update the path
3) Repeat the process max_rep (250) times

Constraints: Although this is very unlikely, the number of repetitions may not be enough to get the most optimal path. Since the shortcut points are 
randomly chosen, we may have a case where a certain shortcut point is missed out.

### Two pointer Method
1) Utilize the path from the Dijkstra's algorithm. Create a loop that checks if the line joining the left pointer and right pointer of the path is valid (:- does not intersect an obstacle)
2) The right pointer is decremented until the line is valid. The valid point is now appended to the shortest path list, and the left pointer of the loop is the valid point. The right pointer is changed back to len(path) - 1
3) This process is repeated until the left pointer is equal to len(path) - 1, and the shortest path is returned

Constraints: Although this method is very accurate as it always gives the most optimal path, it is less efficient than the shortcut method.




