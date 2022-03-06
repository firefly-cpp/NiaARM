Installation
============

Setup development environment
-----------------------------

Requirements
~~~~~~~~~~~~

-  Poetry: https://python-poetry.org/docs/

After installing Poetry and cloning the project from GitHub, you should
run the following command from the root of the cloned project:

.. code:: sh

    $ poetry install

All of the project's dependencies should be installed and the project
ready for further development. **Note that Poetry creates a separate
virtual environment for your project.**

Dependencies
~~~~~~~~~~~~

+----------------+--------------+------------+
| Package        | Version      | Platform   |
+================+==============+============+
| niapy          | ^2.0.1       | All        |
+----------------+--------------+------------+
| pandas         | ^1.3.5       | All        |
+----------------+--------------+------------+
| numpy          | ^1.21.5      | All        |
+----------------+--------------+------------+

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------+-----------+------------+
| Package            | Version   | Platform   |
+====================+===========+============+
| Pytest             | ^7.0.1    | Any        |
+--------------------+-----------+------------+

Extras
~~~~~~

+------------------------------+--------------+------------+
| Package                      | Version      | Platform   |
+==============================+==============+============+
| Sphinx                       | ^4.4.0       | Any        |
+------------------------------+--------------+------------+
| sphinx-rtd-theme             | ^1.0.0       | Any        |
+------------------------------+--------------+------------+
| sphinxcontrib-bibtex         | ^2.4.1       | Any        |
+------------------------------+--------------+------------+
