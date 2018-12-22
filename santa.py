from QTree import QTree, Point, Node
import random
from numpy import sign

my_tree = QTree()
correction = 0

def get_lon_lat(lon, lat):
	lat = float(lat)
	lat = lat / 18

	lon = float(lon)
	lon = lon / 36

	#lat_distance = abs(lat) / 5
	#lon = (abs(lon) - 0.5*lat_distance) * sign(lon)

	lon = (lon+5) % 10
	lat = (lat+5) % 10



	return (lon, lat)

with open('nice_list.txt', "r") as file:
	points = []
	for line in file:
		line = line.split(';')
		lonlat = get_lon_lat(line[2], line[1])
		points.append(Point(lonlat[0], lonlat[1], int(line[3]), int(line[0])))



for p in points:
	my_tree.add_point(p)
	
my_tree.subdivide()


leaf_nodes = my_tree.get_leaves();

all_children = set()
results = []
for node in leaf_nodes:
	trip = []
	for p in node.get_points():
		if(p not in all_children):
			trip.append(p.get_kid())
			all_children.add(p)

	weight = sum([p.get_weight() for p in node.get_points()])
	results.append([trip, weight])

	

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
	

with open('results.txt', 'w') as results_file:
	for result, weight in results:

		if len(result) != 0:
			results_file.write('; '.join([str(x) for x in result]) + '\n')




#my_tree.graph() #uncomment this to see a graphic representation of the quad tree and kids locations


