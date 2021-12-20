GGA cloud install role
======================

The gga_install role creates directory tree for organisms and deploys stacks for the input organisms as well as Traefik stacks.

The gga_install role :

* installs python requirements.
* clones the `gga_load_data <https://gitlab.sb-roscoff.fr/abims/e-infra/gga_load_data>`_ repository and install some python librairies required by GGA.
* generates a config.yml and input.yml required by gga_load_data scripts
* runs gga_init.py scripts that deploy GGA docker stacks.


Role variables
--------------

Not all variables are listed or explained in detail. For additional information about less commonly used variables, see the defaults file.

Required variables
^^^^^^^^^^^^^^^^^^

Host configuration file

* **hostname**: The hostname that will be used to access the application (https://hostname/sp/genus_species/), possibly with a reverse proxy redirecting the requests to the host machine with the right port (https_port).
	
* **proxy_ip**: IP of the upstream proxy (used by Traefik).

Input species variables

*The file consists in a "list" of species for which the script will have to create these stacks, load data into galaxy, run workflows*

* **genus_species**: Name of the organism for the directory tree structure

* **input_species**: *At least genus and species must be filled for gga_init.py script*

.. code-block:: bash

  - name : genus_species
    # Species description, leave blank if unknown or you don't want it to be used
    # These parameters are used to set up the various urls and adresses in different containers
    # The script requires at least the genus to be specified
    genus:
    species:
    sex:
    strain:
    common_name:
    origin:

    # Paths to the different datasets to copy and import into the galaxy container (as a shared library)
    # Must be absolute paths to the dataset
    genome_path:
    contig_prefix:
    transcripts_path:
    proteins_path:
    gff_path:
    interpro_path:
    orthofinder_path: 
    blastp_path: 
    blastx_path: