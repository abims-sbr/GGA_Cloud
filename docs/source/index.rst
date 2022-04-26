GGA cloud documentation
***********************

Galaxy is an open, web-based platform for accessible, reproducible, and transparent computational biomedical research.

For more information on the Galaxy Project, please visit the https://galaxyproject.org

The Galaxy Genome Annotation (GGA) Project is focused on supporting genome annotation inside Galaxy. It consists of several teams, projects, and tool suites that are working closely together to deliver a comprehensive, scalable and easy to use Genome Annotation experience.

For more information on the Galaxy Genome Annotation project, please visit the https://galaxy-genome-annotation.github.io/

GGA cloud is a project initiated by the `ABiMS platform <http://abims.sb-roscoff.fr/>`_ as part of the european project `EOSC Life <https://www.eosc-life.eu/>`_ which aims to automate the deployment of the GGA environment in a cloud-type infrastructure.

Find the github repository at https://github.com/abims-sbr/GGA_Cloud


.. toctree::
   :maxdepth: 2

   Installation <installation/index>

.. toctree::
   :maxdepth: 2

   Ansible roles <gga_cloud/index>

.. toctree::
   :maxdepth: 2

   Galaxy Genome Annotation usage <gga/index>


.. figure:: https://raw.githubusercontent.com/abims-sbr/GGA_Cloud/master/static/images/gga_cloud.png

   *Cuboids represent Docker containers. Hexagon represent a set of Docker container for a species. Black arrows represent HTTP traffic. Blue arrows represent data exchange performed using Galaxy tools. White arrows represent data exchange inherent in applications. Grey arrows represent data/workflow import using Galaxy API.*

.. image:: https://github.com/abims-sbr/GGA_Cloud/blob/master/static/images/eosclogo.png
   :align: left

This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 824087.

.. image:: https://github.com/abims-sbr/GGA_Cloud/blob/master/static/images/eu_flag.jpg
   :align: right