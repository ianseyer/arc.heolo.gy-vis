"""
This class handles the assembly of multiple paths within the Neo4j instance,
utilizing our TwoNode class to, in addition to all Neo4j properties, store a row, col pair
This allows out to distribute our paths within a matrix, and easily project that matrix onto
a cartesian plane for visualization.
"""
from TwoNode import TwoNode
from py2noe import Graph, Node, Relationship
import numpy as np

GRAPH_URI = os.environ['NEO4J_URI']
try:
    GRAPH = Graph(GRAPH_URI)
except Exception as e:
    raise e

def digest_path(path):
    """
    Digests a JSON path returned from a Neo4J query into an nparray of Node IDs
    @returns [node_array, relationship_array]
    """
    node_path = np.array([])
    relationship_path = np.array([])
    for node in path.nodes:
        id = int(node.split("/data/node/")[1])
        np.append(node_path, id)

    for relationship in path.relationships:
        id = int(node.split("/data/relationship/")[1])
        #NOTE eventually you will store weight information here as well
        #NOTE cont'd: it might be worth extending the py2neo Relationship class
        np.append(relationship_path, id)

    return {"nodes":node_path, "relationships":relationship_path}

class PathMatrix:
    NODE_MASTERGRID = np.array([])
    RELATIONSHIP_MASTERGRID = np.array([]) #this is a "hidden" matrix that stores relationship information between nodes
    BEGINNING_NODE = None
    END_NODE = None
    def __init__(self, paths):
        for path in paths:
            digested = digest_path(path)
            np.concatenate(self.NODE_MASTERGRID, digested["nodes"])
            np.concatenate(self.RELATIONSHIP_MASTER, digested["relationships"])
        #grab first and last node from the query, extract the ID from the url, and then fetch from the graph
        self.BEGINNING_NODE = GRAPH.node(int(paths[0].nodes[0].split("/data/node/")[1]))
        self.END_NODE =       GRAPH.node(int(paths[0].nodes[-1].split("/data/node/")[1]))
