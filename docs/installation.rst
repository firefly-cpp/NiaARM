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

To also install the documentation dependencies run:

.. code:: sh

    $ poetry install --with docs

All of the project's dependencies should be installed and the project
ready for further development. **Note that Poetry creates a separate
virtual environment for your project.**

Dependencies
~~~~~~~~~~~~

+----------------+--------------+------------+
| Package        | Version      | Platform   |
+================+==============+============+
| niapy          | ^2.0.5       | All        |
+----------------+--------------+------------+
| pandas         | ^2.1.1       | All        |
+----------------+--------------+------------+
| numpy          | ^1.26.1      | All        |
+----------------+--------------+------------+
| nltk           | ^3.8.1       | All        |
+----------------+--------------+------------+

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------+-----------+------------+
| Package            | Version   | Platform   |
+====================+===========+============+
| pre-commit         | ^3.5.0    | Any        |
+--------------------+-----------+------------+

Test Dependencies
~~~~~~~~~~~~~~~~~

+--------------------+-----------+------------+
| Package            | Version   | Platform   |
+====================+===========+============+
| pytest             | ^7.4.2    | Any        |
+--------------------+-----------+------------+
| pytest-cov         | ^7.4.2    | Any        |
+--------------------+-----------+------------+
| pytest-randomly    | ^7.4.2    | Any        |
+--------------------+-----------+------------+

Documentation dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------------------+--------------+------------+
| Package                      | Version      | Platform   |
+==============================+==============+============+
| sphinx                       | ^7.2.6       | Any        |
+------------------------------+--------------+------------+
| sphinx-rtd-theme             | ^1.0.0       | Any        |
+------------------------------+--------------+------------+
| sphinxcontrib-bibtex         | ^2.4.1       | Any        |
+------------------------------+--------------+------------+


Pre-commit hooks
~~~~~~~~~~~~~~~~

We use pre-commit hooks for formatting and linting. You can install the pre-commit hooks with:

.. code:: sh

    $ pre-commit install


Once the pre-commit hooks are installed and configured, they will automatically run before each git commit. If any hook fails, the commit will be aborted, and you'll need to address the issues raised by the hooks.

To manually run the pre-commit hooks on all files, use the following command:

.. code:: sh

    $ pre-commit run --all-files
