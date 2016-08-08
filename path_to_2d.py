from py2neo import Node as StockNode
from py2neo import Relationship as StockRelationship
from py2neo import Graph, Relationship
from 2dNode import 2dNode as Node
from 2dRelationship import 2dRelationship as Relationship
import numpy as np
import json

ORIGIN=np.array([0,0,0])
GRAPH = Graph(os.environ["NEO4J_URL"])

class PathCloud:
	"""
	This class is responsible for digesting multiple paths, and collapsing shared nodes.
	TODO make it do more things, like maximize "relevance" weight (inverse min cost)
	"""
    members = np.array
    def __init__(pointpaths=[]):
        for pointpath in pointpaths:
            members+=pointpath #TODO write a custom __array__ method for 2d & 3d nodes

class PointPath:
	"""
	This class constructs an nparray of 2d points to represent a path
	TODO make it use relevance weighting
	"""
	path = []
	origin_node = None
	def __init__(path):
		try:
			self.path = json.loads(path)
			self.origin_node = self.path["start"]
		except Exception as e:
			raise e

	def generate_points(distance_scale=1):
		"""
		TODO include weighting in positioning
		Neo4j Paths look like this:
			[ {
			  "relationships" : [ "http://localhost:7474/db/data/relationship/68", "http://localhost:7474/db/data/relationship/77" ],
			  "nodes" : [ "http://localhost:7474/db/data/node/96", "http://localhost:7474/db/data/node/98", "http://localhost:7474/db/data/node/102" ],
			  "directions" : [ "->", "->" ],
			  "start" : "http://localhost:7474/db/data/node/96",
			  "length" : 2,
			  "end" : "http://localhost:7474/db/data/node/102"
			}, {
			  "relationships" : [ "http://localhost:7474/db/data/relationship/69", "http://localhost:7474/db/data/relationship/75" ],
			  "nodes" : [ "http://localhost:7474/db/data/node/96", "http://localhost:7474/db/data/node/99", "http://localhost:7474/db/data/node/102" ],
			  "directions" : [ "->", "->" ],
			  "start" : "http://localhost:7474/db/data/node/96",
			  "length" : 2,
			  "end" : "http://localhost:7474/db/data/node/102"
			} ]
		from: http://neo4j.com/docs/rest-docs/current/#rest-api-graph-algos
		"""
		for node in self.path:
