#!/usr/bin/env python3

import random
import sys

import numpy as np
import scipy as sp

from city import City

def main():
	a = City(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
	a.pickle('new_city.pcl')

if __name__ == "__main__":
	main()