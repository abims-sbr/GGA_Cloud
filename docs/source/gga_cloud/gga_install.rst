GGA install role
================

The gga_install role create directory tree for organisms and deploy stacks for the input organisms as well as Traefik stacks.

The gga_install role :

* installs python requirements.
* clones the gga_load_data repository and install some python librairies required by GGA.
* generates a config.yml and input.yml required by gga_load_data scripts and runs gga_init.py scripts that deploy GGA docker stacks.