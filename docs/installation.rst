Installation
============

Setup development environment
-----------------------------

Requirements
~~~~~~~~~~~~

-  uv: https://docs.astral.sh/uv

After installing uv and cloning the project from GitHub, you should
run the following command from the root of the cloned project:

.. code:: sh

    uv sync

To also install the documentation dependencies run:

.. code:: sh

    uv sync --group docs

All of the project's dependencies should be installed and the project
ready for further development.

Dependencies
~~~~~~~~~~~~


+----------------+--------------+-------------+
| Package        | Version      | Platform    |
+================+==============+=============+
| niapy          | >=2.6.1      | All         |
+----------------+--------------+-------------+
| numpy          | >=2.3.5      | All         |
+----------------+--------------+-------------+
| pandas         | >=2.3.3      | All         |
+----------------+--------------+-------------+
| nltk           | >=3.9.2      | All         |
+----------------+--------------+-------------+
| scikit-learn   | >=1.8.0      | All         |
+----------------+--------------+-------------+
| plotly         | >=6.5.0      | All         |
+----------------+--------------+-------------+


Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------+-----------+------------+
| Package            | Version   | Platform   |
+====================+===========+============+
| pytest             | >=9.0.0   | All        |
+--------------------+-----------+------------+
| pytest-cov         | >=7.0.0   | All        |
+--------------------+-----------+------------+
| pytest-randomly    | >=4.0.1   | All        |
+--------------------+-----------+------------+
| pre-commit         | >=4.5.0   | All        |
+--------------------+-----------+------------+
| ruff               | >=0.14.9  | All        |
+--------------------+-----------+------------+

Documentation dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

+------------------------------+--------------+------------+
| Package                      | Version      | Platform   |
+==============================+==============+============+
| sphinx                       | >=8.2.3      | All        |
+------------------------------+--------------+------------+
| sphinx-rtd-theme             | >=3.0.2      | All        |
+------------------------------+--------------+------------+
| sphinxcontrib-bibtex         | >=2.6.5      | All        |
+------------------------------+--------------+------------+


Pre-commit hooks
~~~~~~~~~~~~~~~~

We use pre-commit hooks for formatting and linting. You can install the pre-commit hooks with:

.. code:: sh

    pre-commit install


Once the pre-commit hooks are installed and configured, they will automatically run before each git commit. If any hook fails, the commit will be aborted, and you'll need to address the issues raised by the hooks.

To manually run the pre-commit hooks on all files, use the following command:

.. code:: sh

    pre-commit run --all-files
