import numpy as np
from py2neo import Node, Relationship, Graph

#A neo4j node, but with 3d coordinates
class TwoNode(Node):
	position = np.array
	def __init__(self, row, y, *args, **kwargs):
		#For if you are creating a node from scratch
		try:
			super(self.__class__, self).__init__(*args, **kwargs)
			self.position = np.array([row,col])
		except Exception as e:
			raise e

	def __repr__(self):
		super(self.__class__, self).__repr__()
		print "Position:", self.position

	def __array__(self):
		return np.asarray([self.id, self.get_position()])

	def get_position(self):
		return self.position

	def set_position(row, col):
		self.coords = np.array([row, col])
