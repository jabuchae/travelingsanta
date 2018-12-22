from QTree import QTree, Point, Node
import random
from distances import *

my_tree = QTree()

#get the list of kids and create a list of points in the plane
with open('nice_list.txt', "r") as file:
	points = []
	for line in file:
		line = line.split(';')
		lonlat = get_lon_lat(line[2], line[1])
		points.append(Point(lonlat[0], lonlat[1], int(line[3]), int(line[0])))


#add all points to the Quad Tree
for p in points:
	my_tree.add_point(p)
	
#create the divisions inside the Quad Tree (the implementation divides nodes when the sum of all weights is above 10 tons)
my_tree.subdivide()


#remove duplicate nodes and calculate total weight of each trip. We'll use this to see if we can make two or more trips without returning to base
leaf_nodes = my_tree.get_leaves();

all_children = set()
results = []
for node in leaf_nodes:
	trip = []
	for p in node.get_points():
		if(p not in all_children):
			trip.append(p)
			all_children.add(p)

	weight = sum([p.get_weight() for p in node.get_points()])
	results.append([trip, weight])

	
#merge trips where the total weight of both trips is still less than 10 tons
old_len = 0
quit = False
initial_i = 1
while initial_i < len(results):
	old_len = len(results)
	i=initial_i
	while i < len(results):
		if(results[i-initial_i][1] + results[i][1] < 10000000):
			results[i-initial_i][0] += results[i][0]
			results[i-initial_i][1] += results[i][1]
			del(results[i])
			i+=1
			quit = False
		i+=1
	if old_len == len(results):
		initial_i += 1

#for each trip, sort the houses to visit by their distance to (0,0) (not optimal but a little improvement from no sorting it at all)
for r in results:
	r[0] = sort_by_distance(r[0])

#write the results
with open('results.txt', 'w') as results_file:
	for result, weight in results:

		if len(result) != 0:
			results_file.write('; '.join([str(x.get_kid()) for x in result]) + '\n')



#see a graphic representation of the quad tree and kids locations
#my_tree.graph() 

