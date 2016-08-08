import numpy as np
import json 

ORIGIN=np.array([0,0,0])
GRAPH = Graph(os.environ["NEO4J_URL"])

class PathCloud:
	#handles the assembling of multiple paths 

class PointPath:
	#represents a single path, represented as 3-d points
	path = []
	origin_node = None
	def __init__(path):
		try:
			self.path = json.loads(path)
			self.origin_node = self.path["start"]
		except Exception as e:
			raise e
		
	def generate_points(distance_scale=1):
		#TODO include weighting in positioning
		#paths look like this:
		"""
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
