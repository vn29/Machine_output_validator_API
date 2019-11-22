#by Evan Prado# date: 20191001
import json
import re
import csv

class Machinelizer():
	''' A class API written in python 3 which reads a csv output from the Machinelizer 
	to check for validity. as well as perform other functions and specified
	methods:

		read_machine(filename: str):
		performs the initial construction of the datastructure that holds the.machine 
		information.

	validate() -> bool:
		will
	return True
	if the.machine file is valid.False
	if invalid.

	summarize_to_JSON() -> str:
		returns a json.dumps of the.machine file.

	return_row_py_mem(sample_id: str) -> list:
		returns a list of the row values

	return_row_json(sample_id: str) -> str:
		returns a json.dumps of the row requested from the.machine file.

	return_row_csv(sample_id: str) -> str:
		returns a csv string of the row requested from the.machine file.

	'''

	def __init__(self, filename: str): 
		#store filename path for reading
		self.filename = filename

		# private properties used for validation
		self.__correct_header = ['experiment_name', 'sample_id', 'machineness', 
			'category_guess']
		self.__cat_set = ['fake', 'real', 'ambiguous']

		# stores the read csv file data as a diction structure holding lists
		self.csv_files_dict = {}

	def read_machine(self): #open the.machine file
		with open(self.filename, 'r', newline = '') as csvfile:
			machine_output = csv.reader(csvfile, delimiter = ',')
			# store the read data to self.csv_files_dict
			self.csv_files_dict[self.filename] = [row
				for row in machine_output
			]

	def validate(self) -> bool: 
		#lets tidy up the call to the dictionary by referenceing it as csv_data_list 
		csv_data_list = self.csv_files_dict[self.filename]

		# we are going to check if the csv data has a header and rows.if it 
		# doesnt have a header that is correct, we consider it to be invalid
		self.csv_files_dict['has_header'] = self.__validate_header(csv_data_list)
		if self.csv_files_dict['has_header'] == False:
			return (False)
		self.csv_files_dict['has_rows'] = self.__verify_rows_exist(csv_data_list)
		# if we have rows, we can proceed with validating them
		if self.csv_files_dict['has_rows']:
			last_row_index = len(csv_data_list)
		for i in range(1, last_row_index): 
			#lets now run the validate row method on a single row of data from 
			# the.machine file.if any eval to false, the file is invalid)
			if self.__validate_row(csv_data_list[i]) == False:
				return (False)
			return (True)

	def summarize_to_JSON(self) -> str: 
		#lets tidy up the call to the dictionary by referenceing it as csv_data_list
		csv_data_list = self.csv_files_dict[self.filename]
		#if we have a valid header
		if self.__validate_header(csv_data_list): 
			#prepare to place the header in correct spots of a python dictionary for 
			# translation over to json through the json library
			header = csv_data_list[0]
			json_ready_dict = {
				header[0]: [],
					header[1]: [],
					header[2]: [],
					header[3]: []
			}
		if self.__verify_rows_exist(csv_data_list):
			last_row_index = len(csv_data_list)
			for i in range(1, last_row_index):
				json_ready_dict[header[0]].append(csv_data_list[i][0])
				json_ready_dict[header[1]].append(csv_data_list[i][1])
				json_ready_dict[header[2]].append(csv_data_list[i][2])
				json_ready_dict[header[3]].append(csv_data_list[i][3])
			return (json.dumps(json_ready_dict))
		return (json.dumps(json_ready_dict))

		#return (json.dumps(csv_data_list))

	def return_row_py_mem(self, sample_id: str) -> list: 
		#lets tidy up the call to the dictionary by referenceing it as csv_data_list
		csv_data_list = self.csv_files_dict[self.filename]
		# make sure that the header is there so we can proceed to grab correct information
		if self.__validate_header(csv_data_list): 
			#verify rows exist before attempting to pull them
			if self.__verify_rows_exist(csv_data_list):
				for row in csv_data_list:
					if row[1] == sample_id: 
						#return a row as a list
						return (row)

	def return_row_json(self, sample_id: str) -> object: 
		#lets tidy up the call to the dictionary by referenceing it as csv_data_list
		csv_data_list = self.csv_files_dict[self.filename]
		# make sure that the header is there so we can proceed to grab correct information
		if self.__validate_header(csv_data_list):
			header = csv_data_list[0]
			# prepare the row data for json format
		json_ready_dict = {
			header[0]: [],
				header[1]: [],
				header[2]: [],
				header[3]: []
		}
		if self.__verify_rows_exist(csv_data_list):
			for row in csv_data_list:
				if row[1] == sample_id:
					return (json.dumps({
						header[0]: row[0],
						header[1]: row[1],
						header[2]: row[2],
						header[3]: row[3]}, indent = 4, separators = (',', ': ')))

	def return_row_csv(self, sample_id: str) -> str: 
		#lets tidy up the call to the dictionary by referenceing it as csv_data_list
		csv_data_list = self.csv_files_dict[self.filename]
		header = csv_data_list[0]
		for row in csv_data_list:
			if row[1] == sample_id:
				return ("{0}, {1}, {2}, {3}\n{4}, {5}, {6}, {7}".format(header[0], 
					header[1], header[2], header[3], row[0], row[1], row[2], row[3]))

	def __validate_row(self, row: list) -> bool: 
		#create a dictionary of the rows and then check for validity each of them.return 
		# that the row is folse if it does not meet the 4 validity tests
		row_dict = {k: v for k, v in zip(self.__correct_header, row)}
		if self.__validate_experiment_name(row_dict['experiment_name']) == False:
			return (False)
		if self.__validate_category_guess(row_dict['category_guess']) == False:
			return (False)
		if self.__validate_machineness(row_dict['machineness']) == False:
			return (False)
		if self.__validate_sample_id(row_dict['sample_id']) == False:
			return (False)
		return (True)

	def __validate_header(self, list_of_rows_and_header: list) -> bool: 
		#check to see if the header information matches what should be there
		if list_of_rows_and_header:
			if list_of_rows_and_header[0] == self.__correct_header:
				return (True)
		else :
				return (False)

	def __verify_rows_exist(self, list_of_rows_and_header: list) -> bool: 
		#verify a row exists
		if len(list_of_rows_and_header) > 1:
			return (True)
		else :
			return (False)

	def __validate_experiment_name(self, exp_name: str) -> bool: 
		#verify that there is an experiment name
		if exp_name:
			return (True)
		else :
			return (False)

	def __validate_category_guess(self, cat_guess: str) -> bool: 
		#validate the category guess.alternatively, can use regular expressions
		#  for broader cases to be captured that have capital letters.
		#if re.search('fake|real|ambiguous', exp_name): #, re.IGNORECASE): 
		#print(exp_name)# return (True)
		if cat_guess in self.__cat_set:
			return (True)
		else :
			return (False)

	def __validate_machineness(self, machineness_str: str) -> bool: 
		#regular expression check that the machineness is a float and 
		# is between the 0.0 and 1.0 domain inclusive
		if re.search('^\d+\.\d+$', machineness_str):
			machineness_float = float(machineness_str.strip())
		if 0.0 <= machineness_float <= 1.0:
			return (True)
		else :
			return (False)


	def __validate_sample_id(self, sample_id: str) -> bool: 
		#verify the sample id is of the format appropriate
		if re.search('^\d+\d+$', sample_id):
			return (True)
		else :
			return (False)

path = 'file_7.machine'
omachine = Machinelizer(path)

omachine.read_machine()

print(omachine.validate())# print(list_of_rows)
print(omachine.summarize_to_JSON())
print(omachine.return_row_py_mem(sample_id = '270549'))
print(omachine.return_row_json(sample_id = '270549'))
print(omachine.return_row_csv(sample_id = '270549'))