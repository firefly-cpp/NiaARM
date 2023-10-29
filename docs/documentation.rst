Documentation
=============

To locally generate and preview documentation run the following commands in the project root folder:

.. code:: sh

    poetry install --extras docs
    poetry run sphinx-build ./docs ./docs/_build

If the build of the documentation is successful, you can preview the documentation in the docs/_build folder by clicking the ``index.html`` file.
