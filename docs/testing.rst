Testing
=======

Before making a pull request, if possible provide tests for added features or bug fixes.

In case any of the test cases fails, those should be fixed before we merge your pull request to master branch.

For the purpose of checking if all test are passing localy you can run following command:

.. code:: sh

    $ poetry run python -m unittest discover
