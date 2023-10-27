NiaARM documentation!
========================================

.. automodule:: niaarm

NiaARM is a minimalistic framework for numerical association rule mining.

* **Free software:** MIT license
* **Github repository:** https://github.com/firefly-cpp/NiaARM
* **Python versions:** 3.7.x, 3.8.x, 3.9.x, 3.10.x, 3.11.x

General outline of the framework
---------------------------------

NiaARM is a framework for Association Rule Mining based on nature-inspired algorithms for optimization. The framework is written fully in Python and runs on all platforms. NiaARM allows users to preprocess the data in a transaction database automatically, to search for association rules and provide a pretty output of the rules found. This framework also supports numerical and real-valued types of attributes besides the categorical ones. Mining the association rules is defined as an optimization problem, and solved using the nature-inspired algorithms that come from the related framework called NiaPy.

Detailed insights
-----------------------

The current version includes (but is not limited to) the following functions:

- loading datasets in CSV format,
- preprocessing of data,
- searching for association rules,
- providing output of mined association rules,
- generating statistics about mined association rules,
- visualization of association rules,
- association rule text mining (experimental).

Documentation
=============

The main documentation is organized into a couple of sections:

* :ref:`user-docs`
* :ref:`dev-docs`
* :ref:`api-reference`
* :ref:`about-docs`

.. _user-docs:

.. toctree::
   :maxdepth: 3
   :caption: User Documentation

   getting_started
   cli

.. _dev-docs:

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   installation
   testing
   documentation

.. _api-reference:

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index

.. _about-docs:

.. toctree::
   :maxdepth: 3
   :caption: About

   contributing
   code_of_conduct
   license

.. rubric:: References

.. bibliography::
   :all:
