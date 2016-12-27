.. Hallgrim documentation master file, created by
   sphinx-quickstart on Thu Dec 22 20:30:29 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Hallgrim's documentation!
====================================

Hallgrim converts readable scripts into ILIAS XML questions that can be imported
into question pools. The scripts follow Python syntax and provide a way of
parametrizing tasks.

.. note:: Hallgrim is still under active development. Syntax and behaviour are open to change. Please report any errors or issues to the `gitlab repository`_.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 3

   tasks
   modules


Installation and Configuration
------------------------------

To install Hallgrim just use pip (**Note:** Hallgrim *does not* work with Python 2):

.. code-block:: bash

    pip install hallgrim

You should get the help section if you invoke ``hallgrim without arguments``:

.. code-block:: text

    usage: hallgrim [-h] {new,gen,upload} ...

    positional arguments:
      {new,gen,upload}
        new             The utility the generate new scripts.
        gen             Subcommand to convert from script to xml.
        upload          Subcommand to upload created xml instances.

    optional arguments:
      -h, --help        show this help message and exit

To use Hallgrim with you own scripts a ``config.ini`` has to be in the directory
where you intend to use hallgrim. If not it will assume ugly default values or
just fail to execute. Your ``config.ini`` should have the following syntax:

.. code-block:: ini

    [META]
    author = <your name>


    [UPLAODER]
    user = root
    pass = homer
    host = http://localhost:8000/
    rtoken = c13456ec3d71dc657e19fb826750f676

If you use your own ILIAS installation for testing purposes you need to update
these default values. If not you can ignore or delete them. Though the uploader
will fail, if it can not find anything here.

That's it! Go use ``hallgrim new`` to create your first script.

.. _gitlab repository: https://gitlab.gwdg.de/j.michal/ilias-generator
