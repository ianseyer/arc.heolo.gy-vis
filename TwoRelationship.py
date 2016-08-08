import numpy as np
from py2neo import Relationship

class TwoRelationship(Relationship):
	start_coords = np.array
    end_coords = np.array
    relationship = Relationship
	def __init__(self, x1, y1, x2, y2, *args, **kwargs):
		try:
			super(self.__class__, self).__init__(*args, **kwargs)
			self.start_coords = np.array([x1,y1])
            self.end_coords = np.array([x2,y2])

		except Exception as e:
			raise e

	def __repr__(self):
		super(self.__class__, self).__repr__()
		print "Start Coordinates:", self.start_coords
        print "End Coordinates:", self.end_coords

	def __array__(self):
		#TODO write this method so that numpy likes us

    def coords(self):
        return np.concatenate((self.start_coords, self.end_coords))
