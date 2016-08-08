from py2neo import Node as StockNode
from py2neo import Relationship as StockRelationship
from py2neo import Graph, Relationship
from TwoNode import TwoNode
from TwoRelationship import TwoRelationship
import numpy as np
import json

ORIGIN=np.array([0,0,0])
GRAPH = Graph(os.environ["NEO4J_URL"])

class PathCloud:
	"""
	This class is responsible for digesting multiple paths, and collapsing shared nodes.
	TODO make it do more things, like maximize "relevance" weight (inverse min cost)
	"""
    members = []
	WIDTH = 0
	HEIGHT = 0
	VERTICAL_SPACING = 10
    def __init__(pointpaths=[], width=1000, height=1000):
		self.width = width
		self.height = height
        for pointpath in pointpaths:
            members+=pointpath


	def __array__(self):
		array_to_return = []
		for member in members:
			array_to_return.append(np.asarray(member))
		return np.asaarray(array_to_return)

	def determine_scale(self):
		"""
		This function creates an average scaling factor between all member paths.
		"""
		total = 0
		length = len(members)
		for member in self.members:
			total += member.get_scale()
		return total/length

	def get_longest_path(self):
		length = 0
		the_node = None
		for member in self.members:
			if len(member.nodes) > length:
				length = len(member.nodes)
				the_node = member

		return the_node

	def get_width(self):
		"""
		Returns the "width" of the path cloud by finding the longest node,
		and multiplying by its scale
		"""
		longest = self.get_longest_path()
		return len(longest.nodes) * longest.get_scale()

	def get_height(self):
		"""
		Returns the "height" of the tree, which is the number of paths times the vertical spacing factor
		TODO: Perform this calculation AFTER collapsing shared routes
		"""
		return len(self.members) * VERTICAL_SPACING

	def apply_scale(self, scale=None):
		"""
		Gets the average scale factor of all members, and then finds a scale factor given
		the dimensions of the Cloud (self.width, self.height)
		"""
		if scale==None:
			scale = determine_scale()
		for member in self.members:
			#first, average out all the member scales
			scale_factor = scale/member.get_scale()
			member.set_scale(member.get_scale() * scale_factor)
			#then, calculate the total height and width of the cloud
			#and maximize the scale
		horizontal_factor = self.WIDTH/self.get_width()
		vertical_factor = self.HEIGHT/self.get_height()

		#set our horizontal scale again, and then generate new points
		for member in self.members:
			member.set_scale(member.get_scale() * horizontal_factor)
			member.generate_points()
		#now apply our vertical factor
		self.VERTICAL_SPACING*=vertical_factor

	def generate_points(self):
		for index, member in enumerate(members):




class PointPath:
	"""
	This class constructs an nparray of 2d points to represent a path (evenly spaces along x axis)
	TODO make it use relevance weighting
	"""
	path = []
	nodes = []
	origin_node = None
	end_node = None
	distance_scale = 1
	def __init__(path):
		try:
			self.path = json.loads(path)
			self.origin_node = self.path.start
			self.end_node = self.path.nodes[-1]
		except Exception as e:
			raise e

	def __repr__(self):
		array_to_print = []
		for node in self.nodes:
			array_to_print.append(node)
		return array_to_print

	def __array__(self):
		#In order to play nice with numpy arrays, we must make this method
		#it represents nodes lazily as [id, nparray(x, y)]
		if len(nodes) == 0:
			self.generate_points()

		return np.asarray(self.nodes) #call each member 2dNode's __array__ method

	def number_of_nodes(self):
		return len(self.path.nodes)

	def cartesian_length(self):
		return self.number_of_nodes() * self.distance_scale

	def get_scale(self):
		return self.distance_scale

	def set_scale(self, scale):
		self.distance_scale = scale
		return self

	def get_nodes(self):
		return self.nodes

	def generate_points():
		"""
		TODO include weighting in positioning
		For now, this relatively simple point generator evenly spaces points along the x-axis.

		Neo4j Paths look like this:
			{
			  "relationships" : [ "http://localhost:7474/db/data/relationship/68", "http://localhost:7474/db/data/relationship/77" ],
			  "nodes" : [ "http://localhost:7474/db/data/node/96", "http://localhost:7474/db/data/node/98", "http://localhost:7474/db/data/node/102" ],
			  "directions" : [ "->", "->" ],
			  "start" : "http://localhost:7474/db/data/node/96",
			  "length" : 2,
			  "end" : "http://localhost:7474/db/data/node/102"
			}
		from: http://neo4j.com/docs/rest-docs/current/#rest-api-graph-algos
		"""
		for index, node in enumerate(self.path.nodes):
			id = int(node.split("db/data/node/")[1])
			node = GRAPH.node(id)
			node.__class__ = Node #convert our node object to a 2dNode object
			#now, we must generate our coordinates
			node.set_coords(index * distance_scale, 0)
			self.nodes.append(node)
