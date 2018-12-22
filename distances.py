import math

def calculate_distance(p1, p2):
	'''
	Calculates the distance between two points in a plane
	'''
	return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )


def get_lon_lat(lon, lat):
	'''
	Translates form longitude and latitude to a plane from (0,0) to (10,10)
	'''
	lat = float(lat)
	lat = lat / 18

	lon = float(lon)
	lon = lon / 36

	lon = (lon+5) % 10
	lat = (lat+5) % 10



	return (lon, lat)


def calculate_trip_distance(trip):
	'''
	Given a list of points, calculates the total distance of going through them in the list's order
	'''

	current_point = trip[0]
	d = 0
	for p in trip[1:]:
		d += calculate_distance((current_point.x, current_point.y), (p.x, p.y))
		current_point = p

	return d

def sort_by_distance(points):
	'''
	Given a small list of points, sorts the list (in-place) representing the shortest path through all of them
	'''

	from random import shuffle
	lowest_distance = calculate_trip_distance(points)
	best_shuffle = points[:]
	current_shuffle = points[:]
	
	for i in range(100):
		shuffle(current_shuffle)
		current_distance = calculate_trip_distance(current_shuffle)
		if(lowest_distance > current_distance):
			best_shuffle = current_shuffle[:]
			lowest_distance = current_distance

	return best_shuffle


