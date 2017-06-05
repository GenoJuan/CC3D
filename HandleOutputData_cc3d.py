
from PySteppables import *
import CompuCell
import CompuCellSetup
import sys
from PySteppables import *
from PlayerPython import *

import random
import os.path
import time

class HandleOutputDataClass(SteppableBasePy):
	def __init__(self,_simulator,_frequency = 1):
		SteppableBasePy.__init__(self,_simulator,_frequency)
	def start(self):
		### Initialize file information...
		file_name = "output_data_"+ str(time.time()) + ".txt"
		path_to_file = "/home/jarias/Dropbox/" + file_name
		self.output_data = open(path_to_file, "w")
		
		### Cell attributes to extract
		self.attributes_to_extract = ['id']
		### Cell attributes to extract from dict
		self.attributes_to_extract_from_dict = ['A'] 
                
                ### Internal cellular network
                self.internal_network = True
                
		### Cell neighbordhood
		### This variable is True is you want to print the cell-to-cell neighbors. It is false otherwise.
		self.cell_neighborhood = False

		### Fields to extract
		### Note that this list may be an empty list.
		self.fields_to_extract = []
	def step(self, mcs):
		### Cell atributes
		for attribute in self.attributes_to_extract:
			self.output_data.write("MCS" + str(mcs)+ "\tCELL_ATTRIBUTE\t" + attribute + ":\t")
			for cell in self.cellList:
				cellattr = getattr(cell, attribute)
				self.output_data.write(" " + str(cellattr))
			self.output_data.write("\n")

		for attribute in self.attributes_to_extract_from_dict:
			self.output_data.write("MCS" + str(mcs)+ "\tCELL_ATTRIBUTE\t" + attribute + ":\t")
			for cell in self.cellList:
				self.output_data.write(" " + str(cell.dict[attribute]))
			self.output_data.write("\n")
		
                ### Internal network
                if(self.internal_network):
                    self.output_data.write("MCS" + str(mcs)+ "\tCELL_ATTRIBUTE\tBOOLNETWORK:\t")
                    for cell in self.cellList:
                        self.output_data.write(" " + str(cell.dict['BoolNetwork'].state()))
                    self.output_data.write("\n")
                    
		### Cell interactions
		if(self.cell_neighborhood):
                        self.output_data.write("MCS" + str(mcs)+ "\tCELL_INTERACTION\tCELL_NEIGHBORS:\t")
			for cell in self.cellList:
				for neighbor , commonSurfaceArea in self.getCellNeighborDataList(cell):
					if neighbor:
                                            if neighbor.id > cell.id:
						self.output_data.write(" " + str(cell.id) + "-" + str(neighbor.id))
			self.output_data.write("\n")

		### Fields
		### WARNING: Consider the large number of possible coordinates (dimX*dim)
		### 	     This might generate a large file size.
		### WARNING: Do not apply for cell-associated fields (Only chemical fields).
		for F in self.fields_to_extract:
			f = self.getConcentrationField(F)
			self.output_data.write("MCS" + str(mcs)+ "\tFIELD\t" + F + ":\t")
			for xdim in range(self.dim.x):
		    		for ydim in range(self.dim.y):
					self.output_data.write(" ")
					self.output_data.write(" " + str(f[xdim, ydim, 0]))
			self.output_data.write("\n")

		# End each step with this flag
		self.output_data.write("MCS" + str(mcs)+ "\tREPORT\n")
	def finish(self):
		self.output_data.close()

