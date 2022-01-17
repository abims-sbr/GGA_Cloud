GGA cloud load data role
========================

The gga_load_data role, first, generates the directory tree into the organism src_data subfolders and then copies data files into the src_data directory tree.

In a second time, the role creates a "Project Data" library in the Galaxy instance, mirroring the "src_data" folder of the current organism directory tree.


Role variables
--------------

Not all variables are listed or explained in detail. For additional information about less commonly used variables, see the defaults file.

Check also the github repository at https://github.com/abims-sbr/GGA_Cloud/tree/master/roles/abims-sbr.gga_load_data


Required variables
^^^^^^^^^^^^^^^^^^

* **repo_folder**: Path where to clone the `gga_load_data <https://gitlab.sb-roscoff.fr/abims/e-infra/gga_load_data>`_ repository.

Optional variables
^^^^^^^^^^^^^^^^^^

To import data from remote server :

* **data_folder**: Path where to copy data files
* **data_url**: URL of the data


Usage
-----

Dry mode
^^^^^^^^

.. code-block:: bash

  ansible-playbook playbook_gga_load_data.yml --check


Real mode
^^^^^^^^^

.. code-block:: bash

  ansible-playbook playbook_gga_load_data.yml