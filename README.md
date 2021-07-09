A class API written in python 3 which reads a csv output from the Machinelizer 
	to check for validity. as well as perform other functions and specified
	methods:

		read_machine(filename: str):
		performs the initial construction of the datastructure that holds the machine 
		information.

	validate() -> bool:
      will return True if the machine file is valid.False if invalid.

	summarize_to_JSON() -> str:
		returns a json.dumps of the machine file.

	return_row_py_mem(sample_id: str) -> list:
		returns a list of the row values

	return_row_json(sample_id: str) -> str:
		returns a json.dumps of the row requested from the machine file.

	return_row_csv(sample_id: str) -> str:
		returns a csv string of the row requested from the machine file.
