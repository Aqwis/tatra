import random
import pickle
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial

class City:
	def _smooth_population(self):
		pass

	def _calculate_population_from_number(self, ratio):
		number_of_locations = float(self.width*self.height)
		return ratio*(self._target_size/number_of_locations)*np.random.exponential(1, None)

	def _calculate_industry_concentration(self, ratio, population):
		number_of_locations = float(self.width*self.height)
		difference_expected_actual = ratio*(self._target_size/number_of_locations) - population # The difference between the expected and actual populations
		industry_concentration = difference_expected_actual*np.random.exponential(1, None)

		if industry_concentration <= 0:
			return 0
		else:
			return industry_concentration

	def _create_location(self, x, y):
		distance = abs(spatial.distance.euclidean([x, y], [self.center_x, self.center_y]))
		max_distance = abs(spatial.distance.euclidean([-1, -1], [self.center_x, self.center_y]))

		ratio = 1-distance/max_distance
		population = self._calculate_population_from_number(ratio)
		industry_concentration = self._calculate_industry_concentration(ratio, population)

		return Location(population, industry_concentration)

	@property
	def population(self):
		population = 0
		for w in range(self.width):
			for h in range(self.height):
				population += self.locations[w][h].population
		return population

	@property
	def maximum_location_population(self):
		maximum_location_population = 0
		for w in range(self.width):
			for h in range(self.height):
				if self.locations[w][h].population > maximum_location_population:
					maximum_location_population = self.locations[w][h].population
		return maximum_location_population

	def plot_population(self):
		num_matrix = np.zeros(shape=(self.width, self.height))
		maximum_location_population = self.maximum_location_population
		for k in range(self.width):
			for l in range(self.height):
				if self.locations[k][l].population > maximum_location_population*0.75:
					num_matrix[k][l] = 1;
				elif self.locations[k][l].population > maximum_location_population*0.25:
					num_matrix[k][l] = 0;
				elif self.locations[k][l].population >= 0:
					num_matrix[k][l] = -1;
				else:
					print(self.locations[k][l].population)
					raise Exception('Position (%s, %s) contained invalid element!' % (k, l,))

		plt.matshow(num_matrix)
		plt.savefig('output.png')

	def pickle(self, filename):
		with open(filename, 'wb') as f:
			pickle.dump(self, f, 3)

	@classmethod
	def depickle(cls, filename):
		with open(filename, 'rb') as f:
			return pickle.load(f)

	def __init__(self, width, height, target_size):
		self._target_size = target_size
		self.locations = defaultdict(dict)
		self.width = width
		self.height = height

		self.center_x = width//2
		self.center_y = height//2

		for w in range(width):
			for h in range(height):
				self.locations[w][h] = self._create_location(w, h)

class Location:
	def __init__(self, population, industry_concentration):
		self.population = population
		self.industry_concentration = industry_concentration