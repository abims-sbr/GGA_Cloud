import os
import logging
import yaml

"""
Metadata generator for gga_auto_load

Creates a file that summarizes actions taken by the autoload script (e.g what was done in the dedicated galaxy instance)
This organism metadata file is located in the metadata directory of the organism directory (i.e /genus_species/metadata)
By default, will also create/update a general metadata file (located in the parent directory i.e where all the organisms
directories are located)

Metadata format: .yml
"""


class MetadataGenerator:

    def __init__(self, maindir):
        self.maindir = maindir
        self.genus = None
        self.species = None
        self.metadata = None
        self.do_update = False


    def read_metadata(self):
    	for label, content in metadata.items():
    		print("FOO")
    		


