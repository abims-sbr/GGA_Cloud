######
tmpdir 
######
..  |travis.png| image:: https://travis-ci.org/mdklatt/ansible-tmpdir-role.svg?branch=master
    :alt: Travis CI build status
    :target: `travis`_
..  _travis: https://travis-ci.org/mdklatt/ansible-tmpdir-role
..  _Ansible role: http://docs.ansible.com/ansible/playbooks_roles.html#roles
..  _Ansible Galaxy: https://galaxy.ansible.com/mdklatt/tmpdir

|travis.png|

This `Ansible role`_ will create a temporary working directory that will be
automatically deleted at the end of the play. Only one directory is created
per play regardless of the number of times this role is included.

This role is also available on `Ansible Galaxy`_.


============
Requirements
============

The target machine must have the ``mktemp`` command.


==============
Role Variables
==============

- ``tmpdir_root``: root path (must exist); defaults to system tmp directory
- ``tmpdir_template``: used to create directory name; defaults to ``tmp.XXXXXX``
- ``tmpdir_path``: directory path; created at runtime
- ``tmpdir_force``: remove directory as privileged user; defaults to false

The ``root`` and ``template`` variables should only be set at the playbook
level. Once the temporary directory is created, changes to these variables will
have no effect. Thus, other roles that use this role should not depend on being
able to modify these values for their own use.

Setting ``force`` to true will allow the cleanup handler to remove any files
that were written by a privleged user.


================
Example Playbook
================
..  code::

    - hosts: all
      
      roles:
        - name: tmpdir
          tmpdir_root: /tmp
          tmpdir_template: tmp.XXXXXXXX
      
      tasks:
        - name: download tmpdir source
          unarchive:
            src: https://github.com/mdklatt/ansible-tmpdir-role/archive/master.zip
            dest: "{{ tmpdir_path }}"
            copy: false


=================
Molecule Workflow
=================

.. _Molecule: https://molecule.readthedocs.io/en/stable/getting-started.html#run-a-full-test-sequence

Use the `Molecule`_ framework for cross-platform testing:

.. code-block:: console

    $ python -m molecule test [--destroy=never]
