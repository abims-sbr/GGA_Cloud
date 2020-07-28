import bioblend
import bioblend.galaxy.objects
from bioblend import galaxy
import argparse
import os
import subprocess
import logging
import sys
import json
import yaml
import re
import table_parser, docker_compose_generator, metadata_generator

"""
gga_auto_load main script
    
Scripted integration of new data into GGA instances. The input is either a table-like (csv, xls, ...) or a json (TODO: yaml) file
that describes what data is to be integrated (genus, species, sex, strain, data), see data_example.json for an example of the correct syntax.
The script will parse the input and take care of everything, from source files directory tree creation to running the gmod tools
inside the galaxy instances of organisms. 

TODO: By default, the script will do everything needed to have a functional instance from scratch. If you want to bypass this behavior, 
you have to specify --update as a parameter. The script can also be used to update an existing GGA instance with new data. For example, you have an instance "genus_species" 
with data for the male sex and want to add the female sex to the same GGA instance. To do this, create your configuration input file as you would normally, and add the "--update"
argument when invoking the script.


STEPS:
- init
- create dir_tree
- find and cp data
- change headers, etc..
- generate blast banks and links
- generate and edit nginx confs
- generate dc and start the containers
- connect to instance and launch tools>workflows
- generate and update metadata
- exit
"""


class Autoload:
    """
    Autoload class contains attributes and functions to interact with GGA

    """

    def __init__(self, species_parameters_dictionary, args):
        self.species_parameters_dictionary = species_parameters_dictionary
        self.args = args
        self.species = species_parameters_dictionary["species"]
        self.genus = species_parameters_dictionary["genus"]
        self.strain = species_parameters_dictionary["strain"]
        self.sex = species_parameters_dictionary["sex"]
        self.common = species_parameters_dictionary["common"]
        self.date = species_parameters_dictionary["date"]
        self.origin = species_parameters_dictionary["origin"]
        self.performed = species_parameters_dictionary["performed by"]
        self.genome_version = species_parameters_dictionary["genome version"]
        self.ogs_version = species_parameters_dictionary["ogs version"]
        self.genus_lowercase = self.genus[0].lower() + self.genus[1:]
        self.full_name = " ".join([self.genus_lowercase, self.species, self.strain, self.sex])
        self.abbreviation = " ".join([self.genus_lowercase[0], self.species, self.strain, self.sex])
        self.genus_species = self.genus_lowercase + "_" + self.species
        self.instance_url = "http://localhost/sp/" + self.genus_lowercase + "_" + self.species + "/galaxy/"  # testing!
        self.instance = None
        self.history_id = None
        self.library_id = None
        self.main_dir = None
        self.species_dir = None
        self.org_id = None
        self.genome_analysis_id = None
        self.ogs_analysis_id = None
        self.tool_panel = None
        self.datasets = dict()
        self.source_files = dict()
        self.workflow_name = None
        self.docker_compose_generator = None
        self.metadata = dict()
        self.source_data_dir = "/projet/sbr/phaeoexplorer"  # directory/subdirectories where source data files are located
        self.do_update = False


    def connect_to_instance(self):
        """
        test the connection to the galaxy instance for the current organism
        the script will crash if it cannot connect to the instance (it won't connect to any other neither)
        # TODO: auth issues with nginx
        """
        self.instance = galaxy.GalaxyInstance(url=self.instance_url,
                                              key="ec601ea5005766e1bc106e69ad8b9eaa",
                                              email="alebars@sb-roscoff.fr",
                                              password="pouet",
                                              verify=True)
        logging.info("connection to the galaxy instance ...")
        try:
            self.instance.histories.get_histories()
            self.tool_panel = self.instance.tools.get_tool_panel()
        except bioblend.ConnectionError:
            logging.info("cannot connect to galaxy instance @ " + self.instance_url)
            sys.exit()
        else:
            logging.info("successfully connected to galaxy instance @ " + self.instance_url)

        
    def get_source_data(self, max_depth):
        """
        NOT PRODUCTION READY

        find and copy source data files to src_data directory tree
        - recursively search for the correct files (within a fixed max depth)
        - requires the organism src_data directory tree to already be properly created for the organism (run generate_dir_tree)
        - the source files must have "transcripts", "proteins"/"pep", "genome" in their name, and a gff extension for the ogs file

        """
        src_data_dir = os.path.join(self.species_dir, "/src_data")

        sp_regex = "(?=\w*V)(?=\w*A)(?=\w*R)(?=\w*I)(?=\w*A)(?=\w*B)(?=\w*L)(?=\w*E)\w+" # TODO: improve regex
        for dirpath, dirnames, files in os.walk(self.source_data_dir):
            for name in files:
                print("foo")
    
    def regex_generator(self, organism_name_pattern):
        """

        """
        re_dict = dict()
        re_dict["gff"] = None
        re_dict["transcripts"] = None
        re_dict["proteins"] = None
        re_dict["genome"] = None

        for char in organism_name_pattern:
            pass

    def generate_dir_tree(self):
        """
        generate the directory tree for an organism, preparing the next steps
        """
        
        os.chdir(self.main_dir)
        self.main_dir = os.getcwd() + "/"
        self.species_dir = os.path.join(self.main_dir, self.genus_species) + "/"
        try:
            os.mkdir(self.species_dir)
        except FileExistsError:
            logging.debug("directory " + self.species_dir + " already exists")
        try:
            os.chdir(self.species_dir)
            working_dir = os.getcwd()
        except OSError:
            logging.info("cannot access " + self.species_dir + ", run with higher privileges")
            sys.exit()

        src_data_folders = ["annotation", "genome"]
        species_folder_name = "_".join([self.genus_lowercase, self.species, self.strain, self.sex])
        try:
            os.mkdir("./src_data")
            os.mkdir("./src_data/annotation")
            os.mkdir("./src_data/genome")
            os.mkdir("./src_data/tracks")
            os.mkdir("./src_data/annotation/" + species_folder_name)
            os.mkdir("./src_data/genome/" + species_folder_name)
            os.mkdir("./src_data/annotation/" + species_folder_name + "/OGS" + self.ogs_version)
            os.mkdir("./src_data/genome/" + species_folder_name + "/v" + self.genome_version)
        except FileExistsError:
            if self.do_update:
                logging.info("updating src_data directory tree")
            else:
                logging.info("src_data directory tree already exists")
        except PermissionError:
            logging.info("insufficient permission to create src_data directory tree")


    def modify_fasta_headers(self):
        """
        """

        try:
            os.chdir(self.species_dir)
            working_dir = os.getcwd()
        except OSError:
            logging.info("cannot access " + self.species_dir + ", run with higher privileges")
            sys.exit()
        self.source_files = dict()
        annotation_dir, genome_dir = None, None
        for d in [i[0] for i in os.walk(os.getcwd() + "/src_data")]:
            if "annotation/" in d:
                annotation_dir = d
                for f in os.listdir(d):
                    if f.endswith("proteins.fasta"):
                        self.source_files["proteins_file"] = os.path.join(d, f)
                    elif f.endswith("transcripts-gff.fa"):
                        self.source_files["transcripts_file"] = os.path.join(d, f)
                    elif f.endswith(".gff"):
                        self.source_files["gff_file"] = os.path.join(d, f)
            elif "genome/" in d:
                genome_dir = d
                for f in os.listdir(d):
                    if f.endswith(".fa"):
                        self.source_files["genome_file"] = os.path.join(d, f)
                logging.debug("source files found:")
        for k, v in self.source_files.items():
            logging.debug("\t" + k + "\t" + v)

        # Changing headers in the *proteins.fasta file from >mRNA* to >protein*
        # production version
        modify_pep_headers = [str(self.main_dir) + "/gga_load_data/ext_scripts/phaeoexplorer-change_pep_fasta_header.sh",
                              self.source_files["proteins_file"]]
        # test version
        # modify_pep_headers = ["/home/alebars/gga/phaeoexplorer-change_pep_fasta_header.sh",
                              # self.source_files["proteins_file"]]
        logging.info("changing fasta headers in " + self.source_files["proteins_file"])
        subprocess.run(modify_pep_headers, stdout=subprocess.PIPE, cwd=annotation_dir)
        # production version
        modify_pep_headers = [str(self.main_dir) + "/gga_load_data/ext_scripts/phaeoexplorer-change_transcript_fasta_header.sh",
                              self.source_files["proteins_file"]]
        # test version
        # modify_pep_headers = ["/home/alebars/gga/phaeoexplorer-change_transcript_fasta_header.sh",
        #                       self.source_files["proteins_file"]]
        logging.info("changing fasta headers in " + self.source_files["transcripts_file"])
        subprocess.run(modify_pep_headers, stdout=subprocess.PIPE, cwd=annotation_dir)

        # src_data cleaning
        if os.path.exists(annotation_dir + "outfile"):
            subprocess.run(["mv", annotation_dir + "/outfile", self.source_files["proteins_file"]],
                           stdout=subprocess.PIPE,
                           cwd=annotation_dir)
        if os.path.exists(annotation_dir + "gmon.out"):
            subprocess.run(["rm", annotation_dir + "/gmon.out"],
                           stdout=subprocess.PIPE,
                           cwd=annotation_dir)

    def generate_blast_banks(self):
        return None

    def goto_working_dir(self):
        return None

    def setup_data_libraries(self):
        """
        - generate blast banks and docker-compose (TODO: separate function)
        - load data into the galaxy container with the galaxy_data_libs_SI.py script

        :return:
        """


        setup_data_libraries = "docker-compose exec galaxy /tool_deps/_conda/bin/python /opt/setup_data_libraries.py"
        try:
            logging.info("loading data into the galaxy container")
            subprocess.run(setup_data_libraries,
                           stdout=subprocess.PIPE,
                           shell=True)
        except subprocess.CalledProcessError:
            logging.info("cannot load data into container for " + self.full_name)
            pass
        else:
            logging.info("data successfully loaded into docker container for " + self.full_name)

        self.get_instance_attributes()
        # self.history_id = self.instance.histories.get_current_history()["id"]

        # import all datasets into current history
        self.instance.histories.upload_dataset_from_library(history_id=self.history_id, lib_dataset_id=self.datasets["genome_file"])
        self.instance.histories.upload_dataset_from_library(history_id=self.history_id, lib_dataset_id=self.datasets["gff_file"])
        self.instance.histories.upload_dataset_from_library(history_id=self.history_id, lib_dataset_id=self.datasets["transcripts_file"])
        self.instance.histories.upload_dataset_from_library(history_id=self.history_id, lib_dataset_id=self.datasets["proteins_file"])

    def get_instance_attributes(self):
        """
        retrieves instance attributes:
        - working history ID
        - libraries ID (there should only be one library!)
        - datasets IDs

        :return:
        """
        histories = self.instance.histories.get_histories(name=str(self.full_name))
        self.history_id = histories[0]["id"]
        logging.debug("history ID: " + self.history_id)
        libraries = self.instance.libraries.get_libraries()  # normally only one library
        self.library_id = self.instance.libraries.get_libraries()[0]["id"]  # project data folder/library
        logging.debug("library ID: " + self.history_id)
        instance_source_data_folders = self.instance.libraries.get_folders(library_id=self.library_id)

        folders_ids = {}
        current_folder_name = ""
        for i in instance_source_data_folders:
            for k, v in i.items():
                if k == "name":
                    folders_ids[v] = 0
                    current_folder_name = v
                if k == "id":
                    folders_ids[current_folder_name] = v
        logging.debug("folders and datasets IDs: ")
        self.datasets = dict()
        for k, v in folders_ids.items():
            logging.info("\t" + k + ": " + v)
            if k == "/genome":
                sub_folder_content = self.instance.folders.show_folder(folder_id=v, contents=True)
                for k2, v2 in sub_folder_content.items():
                    for e in v2:
                        if type(e) == dict:
                            if e["name"].endswith(".fa"):
                                self.datasets["genome_file"] = e["ldda_id"]
                                logging.debug("\t\t" + e["name"] + ": " + e["ldda_id"])
            elif k == "/annotation/" + self.genus_species:
                sub_folder_content = self.instance.folders.show_folder(folder_id=v, contents=True)
                for k2, v2 in sub_folder_content.items():
                    for e in v2:
                        if type(e) == dict:
                            # TODO: manage several files of the same type and manage versions
                            if e["name"].endswith("transcripts-gff.fa"):
                                self.datasets["transcripts_file"] = e["ldda_id"]
                                logging.debug("\t\t" + e["name"] + ": " + e["ldda_id"])
                            elif e["name"].endswith("proteins.fasta"):
                                self.datasets["proteins_file"] = e["ldda_id"]
                                logging.debug("\t\t" + e["name"] + ": " + e["ldda_id"])
                            elif e["name"].endswith(".gff"):
                                self.datasets["gff_file"] = e["ldda_id"]
                                logging.debug("\t\t" + e["name"] + ": " + e["ldda_id"])
                            elif e["name"].endswith("MALE"):
                                self.datasets["gff_file"] = e["ldda_id"]
                                logging.debug("\t\t" + e["name"] + ": " + e["ldda_id"])

    def run_workflow(self, workflow_name, workflow_parameters, datamap):
        """
        Run the "main" workflow in the galaxy instance
        - import data to library
        - load fasta and gff
        - sync with tripal
        - add jbrowse + organism
        - fill in the tripal views

        TODO: map tool name to step id
        :param workflow_name:
        :param workflow_parameters:
        :param datamap:
        :return:
        """

        logging.debug("running workflow: " + str(workflow_name))
        workflow_ga_file = self.main_dir + "Galaxy-Workflow-" + workflow_name + ".ga"
        if self.strain != "":
            custom_ga_file = "_".join([self.genus, self.species, self.strain]) + "_workflow.ga"
            custom_ga_file_path = os.path.abspath(custom_ga_file)
        else:
            custom_ga_file = "_".join([self.genus, self.species]) + "_workflow.ga"
            custom_ga_file_path = os.path.abspath(custom_ga_file)
        with open(workflow_ga_file, 'r') as ga_in_file:
            workflow = str(ga_in_file.readlines())
            # ugly fix for the jbrowse parameters
            workflow = workflow.replace('{\\\\\\\\\\\\"unique_id\\\\\\\\\\\\": \\\\\\\\\\\\"UNIQUE_ID\\\\\\\\\\\\"}',
                                        str('{\\\\\\\\\\\\"unique_id\\\\\\\\\\\\": \\\\\\\\\\\\"' + self.genus + " " + self.species) + '\\\\\\\\\\\\"')
            workflow = workflow.replace('\\\\\\\\\\\\"name\\\\\\\\\\\\": \\\\\\\\\\\\"NAME\\\\\\\\\\\\"',
                                        str('\\\\\\\\\\\\"name\\\\\\\\\\\\": \\\\\\\\\\\\"' + self.genus.lower()[0] + self.species) + '\\\\\\\\\\\\"')
            workflow = workflow.replace("\\\\", "\\")  # to restore the correct amount of backslashes in the workflow string before import
            # test
            workflow = workflow.replace('http://localhost/sp/genus_species/feature/Genus/species/mRNA/{id}',
                                        "http://localhost/sp/" + self.genus_lowercase+ "_" + self.species + "/feature/" + self.genus + "/mRNA/{id}")
            # production
            # workflow = workflow.replace('http://localhost/sp/genus_species/feature/Genus/species/mRNA/{id}',
            #                             "http://abims--gga.sb-roscoff.fr/sp/" + self.genus_lowercase + "_" + self.species + "/feature/" + self.genus + "/mRNA/{id}")
            workflow = workflow[2:-2]  # if the line under doesn't output a correct json
            # workflow = workflow[:-2]  # if the line above doesn't output a correct json

            workflow_dict = json.loads(workflow)

            self.instance.workflows.import_workflow_dict(workflow_dict=workflow_dict)
            self.workflow_name = workflow_name
            workflow_attributes = self.instance.workflows.get_workflows(name=self.workflow_name)
            workflow_id = workflow_attributes[0]["id"]
            show_workflow = self.instance.workflows.show_workflow(workflow_id=workflow_id)
            logging.debug("workflow ID: " + workflow_id)

            logging.debug("inputs:")
            logging.debug(show_workflow["inputs"])
            self.instance.workflows.invoke_workflow(workflow_id=workflow_id,
                                                    history_id=self.history_id,
                                                    params=workflow_parameters,
                                                    inputs=datamap,
                                                    inputs_by="")
            self.instance.workflows.delete_workflow(workflow_id=workflow_id)

    def init_instance(self):
        """
        Galaxy instance startup in preparation for running workflows
        - remove Homo sapiens from the chado database.
        - add organism and analyses into the chado database
        - get any other existing organisms IDs (mainly used for testing)

        :return:
        """

        self.instance.histories.create_history(name=str(self.full_name))
        histories = self.instance.histories.get_histories(name=str(self.full_name))
        self.history_id = histories[0]["id"]
        logging.debug("history ID: " + self.history_id)
        libraries = self.instance.libraries.get_libraries()  # routine check: one library
        self.library_id = self.instance.libraries.get_libraries()[0]["id"]  # project data folder/library
        logging.debug("library ID: " + self.history_id)
        instance_source_data_folders = self.instance.libraries.get_folders(library_id=self.library_id)
        
        # Delete Homo sapiens from Chado database
        logging.info("getting sapiens ID in instance's chado database")
        get_sapiens_id_job = self.instance.tools.run_tool(tool_id="toolshed.g2.bx.psu.edu/repos/gga/chado_organism_get_organisms/organism_get_organisms/2.3.2",
                                                          history_id=self.history_id,
                                                          tool_inputs={"genus": "Homo", "species": "sapiens"})
        get_sapiens_id_job_output = get_sapiens_id_job["outputs"][0]["id"]
        get_sapiens_id_json_output = self.instance.datasets.download_dataset(dataset_id=get_sapiens_id_job_output)
        try:
            logging.info("deleting Homo sapiens in the instance's chado database")
            get_sapiens_id_final_output = json.loads(get_sapiens_id_json_output)[0]
            sapiens_id = str(get_sapiens_id_final_output["organism_id"])  # needs to be str to be recognized by the chado tool
            self.instance.tools.run_tool(tool_id="toolshed.g2.bx.psu.edu/repos/gga/chado_organism_delete_organisms/organism_delete_organisms/2.3.2",
                                         history_id=self.history_id,
                                         tool_inputs={"organism": str(sapiens_id)})
        except bioblend.ConnectionError:
            logging.debug("Homo sapiens isn't in the instance's chado database")
        except IndexError:
            logging.debug("Homo sapiens isn't in the instance's chado database")
            pass

        # Add organism (species) to chado
        logging.info("adding organism to the instance's chado database")
        self.instance.tools.run_tool(tool_id="toolshed.g2.bx.psu.edu/repos/gga/chado_organism_add_organism/organism_add_organism/2.3.2",
                                     history_id=self.history_id,
                                     tool_inputs={"abbr": self.abbreviation,
                                                  "genus": self.genus,
                                                  "species": self.species,
                                                  "common": self.common})
        # Add OGS analysis to chado
        logging.info("adding OGS analysis to the instance's chado database")
        self.instance.tools.run_tool(tool_id="toolshed.g2.bx.psu.edu/repos/gga/chado_analysis_add_analysis/analysis_add_analysis/2.3.2",
                                     history_id=self.history_id,
                                     tool_inputs={"name": self.genus + " " + self.species + " OGS" + self.ogs_version,
                                                  "program": "Performed by Genoscope",
                                                  "programversion": str("OGS" + self.ogs_version),
                                                  "sourcename": "Genoscope",
                                                  "date_executed": self.date})

        # Add genome analysis to chado
        logging.info("adding genome analysis to the instance's chado database")
        self.instance.tools.run_tool(tool_id="toolshed.g2.bx.psu.edu/repos/gga/chado_analysis_add_analysis/analysis_add_analysis/2.3.2",
                                     history_id=self.history_id,
                                     tool_inputs={"name": self.genus + " " + self.species + " genome v" + self.genome_version,
                                                  "program": "Performed by Genoscope",
                                                  "programversion": str("genome v" + self.genome_version),
                                                  "sourcename": "Genoscope",
                                                  "date_executed": self.date})

        self.get_organism_and_analyses_ids()
        logging.info("finished initializing instance")

    def get_organism_and_analyses_ids(self):
        """
        Retrieve current organism ID and OGS and genome chado analyses IDs (needed to run some tools as Tripal/Chado
        doesn't accept organism/analyses names as valid inputs

        :return:
        """
        # Get the ID for the current organism in chado
        org = self.instance.tools.run_tool(
            tool_id="toolshed.g2.bx.psu.edu/repos/gga/chado_organism_get_organisms/organism_get_organisms/2.3.2",
            history_id=self.history_id,
            tool_inputs={"genus": self.genus, "species": self.species})
        org_job_out = org["outputs"][0]["id"]
        org_json_output = self.instance.datasets.download_dataset(dataset_id=org_job_out)
        try:
            org_output = json.loads(org_json_output)[0]
            self.org_id = str(org_output["organism_id"])  # id needs to be a str to be recognized by chado tools
        except IndexError:
            logging.debug("no organism matching " + self.full_name + " exists in the instance's chado database")

        # Get the ID for the OGS analysis in chado
        ogs_analysis = self.instance.tools.run_tool(
            tool_id="toolshed.g2.bx.psu.edu/repos/gga/chado_analysis_get_analyses/analysis_get_analyses/2.3.2",
            history_id=self.history_id,
            tool_inputs={"name": self.genus + " " + self.species + " OGS" + self.ogs_version})
        ogs_analysis_job_out = ogs_analysis["outputs"][0]["id"]
        ogs_analysis_json_output = self.instance.datasets.download_dataset(dataset_id=ogs_analysis_job_out)
        try:
            ogs_analysis_output = json.loads(ogs_analysis_json_output)[0]
            self.ogs_analysis_id = str(ogs_analysis_output["analysis_id"])
        except IndexError:
            logging.debug("no matching OGS analysis exists in the instance's chado database")

        # Get the ID for the genome analysis in chado
        genome_analysis = self.instance.tools.run_tool(
            tool_id="toolshed.g2.bx.psu.edu/repos/gga/chado_analysis_get_analyses/analysis_get_analyses/2.3.2",
            history_id=self.history_id,
            tool_inputs={"name": self.genus + " " + self.species + " genome v" + self.genome_version})
        genome_analysis_job_out = genome_analysis["outputs"][0]["id"]
        genome_analysis_json_output = self.instance.datasets.download_dataset(dataset_id=genome_analysis_job_out)
        try:
            genome_analysis_output = json.loads(genome_analysis_json_output)[0]
            self.genome_analysis_id = str(genome_analysis_output["analysis_id"])
        except IndexError:
            logging.debug("no matching genome analysis exists in the instance's chado database")

    def clean_instance(self):
        """
        TODO: function to purge the instance from analyses and organisms
        :return:
        """
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatic data loading in containers and interaction with galaxy instances for GGA"
                                                 ", following the protocol @ "
                                                 "http://gitlab.sb-roscoff.fr/abims/e-infra/gga")
    # Dev arguments, TODO: remove in production branch!
    parser.add_argument("--full",
                        help="Run everything, from src_data dir tree creation, moving data files (abims) into src_data,"
                        " modify headers (abims), generate blast banks (doesn't commit them: TODO), initialize GGA instance, load the data and run,"
                        " the main workflow. To update/add data to container, use --update in conjunction to --full (TODO)")
    parser.add_argument("--init-instance",
                        help="Initialization of galaxy instance. Run first in an empty instance",
                        action="store_true")
    parser.add_argument("--load-data",
                        help="Create src_data directory tree and load its data into the instance")
    parser.add_argument("--run-main",
                        help="Run main workflow (load data into chado, sync all with tripal, "
                             "index tripal data, populate materialized view, "
                             "create a jbrowse for the current genus_species_strain_sex and add organism to jbrowse")
    parser.add_argument("--generate-docker-compose",
                        help="Generate docker-compose.yml for current species")
    parser.add_argument("--link-source",
                        help="Find source files in source data dir and copy them to src_data",
                        action="store_true")

    # Production arguments
    parser.add_argument("input", type=str, help="Input table (tabulated file that describes all data) or json file")
    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity",
                        action="store_false")
    parser.add_argument("--update",
    					help="Update an already integrated organisms with new data from input file, docker-compose.yml will not be re-generated"
    					", assuming the instances for the organisms are already generated and initialized",
                        action="store_false")
    parser.add_argument("--dir",
    					help="Path of the main directory, either absolute or relative, defaults to current directory",
                        default=os.getcwd())

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if str(args.input).endswith(".json"):
        print("JSON")
        input_json = args.input
    else:
        tp = table_parser.TableParser()
        logging.info("parsing input table")
        tp.table = args.input
        input_json = tp.parse_table(mode="simple", method="table_to_json")
    sp_dict_list = list()
    with open(input_json, 'r') as infile:
        json_sp_dict = json.load(infile)
        json_sp_dump = json.dumps(json_sp_dict, indent=4, sort_keys=True)
        for json_sp in json_sp_dict:
            sp_dict_list.append(json_sp)

    metadata = {}
    for sp_dict in sp_dict_list:
        al = Autoload(species_parameters_dictionary=sp_dict, args=args)
        al.main_dir = os.path.abspath(args.dir)
        if args.init_instance:
            logging.info("initializing the galaxy instance")
            al.init_instance()
            al.get_instance_attributes()
            metadata[genus_species_strain_sex]["initialized"] = True
        if args.load_data:
            logging.info("loading data into galaxy")
            # al.load_data()
            metadata[genus_species_strain_sex]["data_loaded_in_instance"] = True
        if args.run_main:
            logging.info("running main workflow")
            al.get_organism_and_analyses_ids()
            workflow_parameters = dict()
            workflow_parameters["0"] = {}
            workflow_parameters["1"] = {}
            workflow_parameters["2"] = {}
            workflow_parameters["3"] = {}
            workflow_parameters["4"] = {"organism": al.org_id,
                                        "analysis_id": al.genome_analysis_id,
                                        "do_update": "true"}
            workflow_parameters["5"] = {"organism": al.org_id,
                                        "analysis_id": al.ogs_analysis_id}
            workflow_parameters["6"] = {"organism_id": al.org_id}
            workflow_parameters["7"] = {"analysis_id": al.ogs_analysis_id}
            workflow_parameters["8"] = {"analysis_id": al.genome_analysis_id}
            workflow_parameters["9"] = {"organism_id": al.org_id}
            workflow_parameters["10"] = {}
            workflow_parameters["11"] = {}

            al.datamap = dict()
            al.datamap["0"] = {"src": "hda", "id": al.datasets["genome_file"]}
            al.datamap["1"] = {"src": "hda", "id": al.datasets["gff_file"]}
            al.datamap["2"] = {"src": "hda", "id": al.datasets["proteins_file"]}
            al.datamap["3"] = {"src": "hda", "id": al.datasets["transcripts_file"]}

            al.run_workflow(workflow_name="main", workflow_parameters=workflow_parameters, datamap=al.datamap)
            metadata[genus_species_strain_sex]["workflows_run"] = metadata[genus_species_strain_sex]["workflows_run"].append("main")

        if args.link_source:
            print('SOURCE DATA HANDLE')
            al.generate_dir_tree()
            print(al.main_dir)
            print(al.species_dir)
