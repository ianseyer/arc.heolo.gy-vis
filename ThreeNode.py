import numpy as np
from py2neo import Node, Relationship, Graph

#A neo4j node, but with 3d coordinates
class ThreeNode(Node):
	coords = np.array
	def __init__(self, x, y, z, *args, **kwargs):
		try:
			super(self.__class__, self).__init__(*args, **kwargs)
			self.coords = np.array([x,y,z])
		except Exception as e:
			raise e

	def __repr__(self):
		super(self.__class__, self).__repr__()
		print "Coordinates:", coords

	def __array__(self):
		#TODO write this method so that numpy likes us

	def coords(self):
		return self.coords
