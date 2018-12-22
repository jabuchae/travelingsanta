#most of the code in this file was taken from https://kpully.github.io/Quadtrees/

import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Point():
    def __init__(self, x, y, w, kid_id):
        self.x = x
        self.y = y
        self.w = w
        self.kid_id = kid_id

    def get_kid(self):
        return self.kid_id


    def get_weight(self):
        return self.w

class Node():
    def __init__(self, x0, y0, w, h, points):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.points = points
        self.children = []

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_points(self):
        return self.points

    def get_leaves(self):

        if len(self.children) == 0:
            return [self]


        leaves = []

        for child in self.children:
            leaves += child.get_leaves()

        return leaves

class QTree():
    def __init__(self):
        self.threshold = 10000000 #10 tons in grams
        self.points = []
        self.root = Node(0, 0, 10, 10, self.points)

    def add_point(self, p):
        self.points.append(p)

    def get_points(self):
        return self.points
    
    def subdivide(self):
        recursive_subdivide(self.root, self.threshold)
    
    def graph(self):
        fig = plt.figure(figsize=(12, 8))
        plt.title("Quadtree")
        ax = fig.add_subplot(111)
        c = self.root.get_leaves()
        print "Number of segments: %d" %len(c)
        areas = set()
        for el in c:
            areas.add(el.width*el.height)
        print "Minimum segment area: %.3f units" %min(areas)
        for n in c:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]
        plt.plot(x, y, 'ro')
        plt.show()
        return

    def get_leaves(self):
        return self.root.get_leaves()

def recursive_subdivide(node, k):
    if reduce((lambda x, y: x + y.w), node.points, 0) <= k:
        return
    
    w_ = float(node.width/2)
    h_ = float(node.height/2)

    p = contains(node.x0, node.y0, w_, h_, node.points)
    x1 = Node(node.x0, node.y0, w_, h_, p)
    recursive_subdivide(x1, k)

    p = contains(node.x0, node.y0+h_, w_, h_, node.points)
    x2 = Node(node.x0, node.y0+h_, w_, h_, p)
    recursive_subdivide(x2, k)

    p = contains(node.x0+w_, node.y0, w_, h_, node.points)
    x3 = Node(node.x0 + w_, node.y0, w_, h_, p)
    recursive_subdivide(x3, k)

    p = contains(node.x0+w_, node.y0+w_, w_, h_, node.points)
    x4 = Node(node.x0+w_, node.y0+h_, w_, h_, p)
    recursive_subdivide(x4, k)

    node.children = [x1, x2, x3, x4]
    
    
def contains(x, y, w, h, points):
    pts = []
    for point in points:
        if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+h:
            pts.append(point)
    return pts

