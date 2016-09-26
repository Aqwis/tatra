import random
import pickle
import math
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

		return Location(population, industry_concentration)

	###

	def _initialize_city_centre(self):
		previous_coordinates = None
		for r in range(0, self.width//2):
			for angle in np.arange(0, 2*math.pi, 0.001):
				x = round(r*math.cos(angle)+self.center_x)
				y = round(r*math.sin(angle)+self.center_y)

				assert x in range(0, self.width)
				assert y in range(0, self.height)

				if (x,y) == previous_coordinates:
					continue

				#exponent = 0.5
				coefficient = math.log(4)/(self.width//2)
				population_variation_range = 0.4
				industry_variation_range = 0.8
				self.locations[x][y].population = (1 + random.uniform(-population_variation_range, population_variation_range))*math.exp(-coefficient*r) - math.exp(-coefficient*self.width//2)
				self.locations[x][y].industry = (0.5 + random.uniform(-industry_variation_range, industry_variation_range))*math.exp(-coefficient*r) - 0.5*math.exp(-coefficient*self.width//2)

				#print(self.locations[x][y].population)
				#print(self.locations[x][y].industry)
				#print()

				if self.locations[x][y].population < 0:
					self.locations[x][y].population = 0
				if self.locations[x][y].industry < 0:
					self.locations[x][y].industry = 0
				previous_coordinates = (x,y)

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
				self.locations[w][h] = Location(0, 0)

		self._initialize_city_centre()
		self.plot_population()

		self.pickle(str(width) + "x" + str(height) + "-" + str(target_size) + ".pickle")

class Location:
	def __init__(self, population, industry):
		self.population = population
		self.industry = industry