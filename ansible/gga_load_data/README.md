# gga_load_data (WIP)

Automated integration of new organisms into GGA instances.

## Description:
This script is made for automatically integrating new organisms into GGA instances as part of the phaeexplorer project.
As input, the script either takes a tabulated file (xls, xlsx or csv) or a json file describing the organism for which it has to create/update instances. 
For each organism to be integrated, the script needs at least its genus and species (strain, sex, genome and annotation files versions are optional, but the two later will be set to the default version of 1.0, and the two former will be set as empty and will not being considered during the integration process). 
See example datasets (example.json and example.xlsx) for an example of what information can be described and the correct formatting of these input files. The script should then take of everything (for phaeoexplorer organisms), from generating the directory tree to running workflows and tools in the galaxy instance.

## TODO: 
- ready the script for production (add usage arguments): remove dev args for master merge
- metadata
- search and link source files to src_data
- call the scripts for formatting data, generate blast banks
- nginx conf editing (+ master key in docker-compose)
- set master key
- user password input + store hash

## Metadata files (WIP):
The script also generates a metadata file in the directory of the newly integrated species, summing up what actions were taken for this organism (see meta_toy.yaml for
the kind of information it can contain). It also creates another metadata files in the main directory (where you put all the organisms you have integrated), which contains the sum of all metadata files from all integrated organisms. These metadata files are also updated when updating an existing instance.

## nginx conf (WIP):
The default.conf will be automatically generated (automatic port affectation), APIs will be able to bypass authentication (for bioblend, a master key
is set at the creation of the docker-compose.yml of the organisms)

## Directory tree:
For every input organism, the script will create the following directories structure, or try to update it if it already exists.
It will update the files in the main directory to account for the new organisms that are getting integrated.

```
/main_directory
|
|---/genus1_species1
|   |
|   |---/blast
|   |   |---/links.yml
|   |   |---/banks.yml
|   |
|   |---/nginx
|   |   |---/conf
|   |       |---/default.conf
|	|
|	|---/src_data
|	|	|---/genome
|	| 	|	|---/genus1_species1_strain_sex                       
|	|   |    	|---/vX.X
|	|   |        	|---/genus_species_vX.X.fasta
|	|   |
|	|	|---/annotation
|	|	|	|---/genus1_species1_strain_sex                   
|	|	|		|---/OGSX.X
|	|	|           |---/OGSX.X.gff
|	|	|           |---/OGSX.X_pep.fasta
|	|	|           |---/OGSX.X_transcripts.fasta
|   |   |
|   |   |---/tracks
|   |    	|---/genus1_species1_strain_sex
|   |                    
|   |---/apollo	
|   |   |---/annotation_groups.tsv
|   |
|   |---/docker-compose.yml
|   |
|   |---/metada_genus1_species1.yml
|
|---/metadata.yml
|
|---/main_proxy
	|---/conf
		|---/default.conf

```

## Steps:
For each input organism:
1) create the json input file for the script
2) create the docker-compose.yml for the organism (+ default.conf and edit main_proxy nginx default.conf for docker-compose docker configuration)
3) create the directory tree structure (if it already exists, only create the required directories)
4) gather files in the "source data" directory tree, can recursively search the directory (by default, the source-data folder is fixed for phaeoexplorer data, this default fixed directory can be set in the attributes of the Autoload class in autoload.py.
5) link the source files to the organism correct src_data folders
6) modify headers in the transcripts and protein fasta files
7) generate blast banks (no commit)
8) start the containers
9) connect to the galaxy instance
10) run data integration galaxy steps (see @ http://gitlab.sb-roscoff.fr/abims/e-infra/gga)
11) generate and update metadata files

## Usage (production):
For organisms you want to integrate to GGA (not already integrated i.e no containers exists for the input organisms): 
```
python3 autoload.py input.xlsx --source-data <dir>
```

IN PROGRESS:
For integrated organisms you want to update with new data (the input shouldn't contain already integrated content):
```
python3 autoload.py input.xlsx --update
```
## Usage (development):

autoload.py example:
```
python3 autoload.py input.xlsx --init-instance --load-data --run-main
```

docker_compose_generator.py example:
```
python3 docker_compose_generator.py --genus genus --species species --mode compose --dir . --template compose_template.yml
```



## Requirements:
- bioblend (v0.13)
- PyYaml
- pandas (+ xlrd package)
