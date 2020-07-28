import os
import sys
import pandas  # xlrd required for excel files reading
import numpy
import json
import argparse
import logging
from datetime import datetime

"""
Table parser for phaeoexplorer data. Tested with xlsand xlsx input format, should work with csv format as well
Does not work for ods spreadsheets (save as xls or xlsx instead) --> need to handle with pandas_ods_reader (requires ezodf, lxml)
Does not support multiple sheets (TODO: "integration" and "update" sheets (1 and 2))
See example toy table (toy_table.xls)

standalone usage: python3 table_parser.py <tabulated_file> -d <directory_to_write_json_to (default: cwd)>
"""

class TableParser:

	def __init__(self, table_file, dir):
		self.dir = os.path.abspath(args.dir)
		self.table_file = table_file
		self.method = None  # TODO: instant launch or just parse (standalone)
		self.extension = None
		self.meta = dict()
		self.json_file = None	

	def parse_table(self, extension):
		if extension == "xls":
			pandas_table = pandas.DataFrame(pandas.read_excel(self.table_file))
		elif extension == "csv":
			pandas_table = pandas.DataFrame(pandas.read_csv(self.table_file))
		else:
			logging.info("wrong format: input tabulated file cannot be read (supported formats: xls, xlsx, csv)")
			sys.exit()
		pandas_table = pandas_table.replace(numpy.nan, "", regex=True)
		
		for char in " ,.()-/":
			pandas_table = pandas_table.replace("\\" + char, "_", regex=True)
		pandas_table = pandas_table.replace("\\__", "_", regex=True)
		pandas_table.loc[pandas_table["genome version"] == "", "genome version"] = "1.0"
		pandas_table.loc[pandas_table["ogs version"] == "", "ogs version"] = "1.0"
		pandas_table.loc[pandas_table["version"] == "", "version"] = "1.0"
		pandas_table.loc[pandas_table["date"] == "", "date"] = datetime.today().strftime("%Y-%m-%d")
		with open(os.path.join(self.dir, self.json_file), 'w') as json_file:
			json_file.truncate(0)
			json_content = list()
			for organism in range(0, len(pandas_table.index)):
				organism_dict = pandas_table.iloc[organism].to_dict()
				for k, v in organism_dict.items():
					v = str(v).split(" ")
					v = "_".join(v)
					v = v.replace("__", "_")
					if v.endswith("_"):
						v = v[:-1]
				json_content.append(organism_dict)
			json.dump(json_content, json_file, indent=4)

		

	def write_json(self, data, filename):
		with open(filename, 'w') as f:
			json.dump(data, f, indent=4)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Table parser for phaeoexplorer data")
	parser.add_argument("input", type=str, help="input table")
	parser.add_argument("-d", "--dir", type=str, help="Where to write the output json file that is be used for integration", default = os.getcwd())
	args = parser.parse_args()

	if args.input.endswith("xlsx") or args.input.endswith("xls"):
		tp = TableParser(table_file=args.input, dir=args.dir)
		tp.extension = args.input.split(".")[1]
		tp.json_file = tp.dir + "/dataloader_" + datetime.today().strftime("%Y%m%d") + ".json"
		tp.parse_table(extension="xls")