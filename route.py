import math

import numpy as np
from scipy import spatial

class Route:
	def _set_route_to_straight_line(self):
		coefficients = np.polyfit([self.start[0], self.end[0]], [self.start[1], self.end[1]], 1)
		polynomial = np.poly1d(coefficients)

		x_values = np.linspace(self.start[0], self.end[0], abs(self.start[0]-self.end[0]+1))
		y_values = [int(round(y)) for y in polynomial(x_values)]

		self.route = list(zip(x_values, y_values))

	@property
	def suitability(self):
		pass

	def _find_neighbours(self, coords):
		neighbours = []
		for pair in self.route:
			if 0 < abs(spatial.distance.euclidean(coords, pair)) < 2:
				neighbours.append(pair)
		return neighbours

	def _try_move(self, route_index):
		coords = self.route[route_index]
		neighbours = self._find_neighbours(coords)
		x = coords[0]
		y = coords[1]

		print(neighbours)

	def _try_move_all(self):
		for i, pair in enumerate(self.route):
			self._try_move(i)

	def __init__(self, initial_starting_point, initial_end_point):
		self.start = initial_starting_point
		self.end = initial_end_point
		self.route = []
		self._set_route_to_straight_line()