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
    Digests a JSON path returned from a Neo4j query into an nparray of Node and Relationship ids
    @returns {"nodes":node_array, "relationships":relationship_array}
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
    """
    A rudimentary adjacency list storing both Nodes and Paths between them.
    https://en.wikipedia.org/wiki/Adjacency_list
    """
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

    def num_paths(self):
        return len(self.NODE_MASTERGRID) #returns the number of rows (paths)

    def get_longest_path(self):
        """
        Returns a list containing the longest path(s)
        """
        longest = [[]]
        for path in self.NODE_MASTERGRID:
            if len(path) > len(longest[0]):
                longest = [path]
            if len(path) == len(longest[0]):
                longest.append(path)
        return longest

    def get_longest_path_length(self):
        """
        Returns the length of the longest path(s)
        """
        return len(self.get_longest_path[0])

    def compress(self):
        """
        This method is responsible for collapsing shared pathways and removing duplicate nodes in a path matrix.
        E.g. if there exist two paths:
          [
            [1,2,3,4],
            [1,5,3,4]
          ]
        Then we should collapse the resultant to:
        [
            [1,[2,5],3,4]
        ]

        Method:
        1. Find the longest unique paths
        2. Now, find all smaller paths that are subpaths of them
        3. Add the path to the array at it's shared index

        More discussion here: https://gist.github.com/ianseyer/cb9ef79aecb2ddceef34fc3671804dec
        """
        
