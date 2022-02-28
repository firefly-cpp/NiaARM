NiaARM documentation!
========================================

.. automodule:: niaarm

NiaARM is a minimalistic framework for numerical association rule mining.

* **Free software:** MIT license
* **Github repository:** https://github.com/firefly-cpp/NiaARM
* **Python versions:** 3.6.x, 3.7.x, 3.8.x

General outline of the framework
---------------------------------

NiaARM is a framework for Association Rule Mining based on nature-inspired algorithms for optimization. The framework is written fully in Python and runs on all platforms. NiaARM allows users to preprocess the data in a transaction database automatically, to search for association rules and provide a pretty output of the rules found. This framework also supports numerical and real-valued types of attributes besides the categorical ones. Mining the association rules is defined as an optimization problem, and solved using the nature-inspired algorithms that come from the related framework called NiaPy.

Detailed insights
-----------------------

The current version witholds (but is not limited to) the following functions:

- loading datasets in CSV format,
- preprocessing of data,
- searching for association rules,
- providing output of mined association rules,
- generating statistics about mined association rules.


Documentation
=============

The main documentation is organized into a couple of sections:

* :ref:`user-docs`
* :ref:`dev-docs`
* :ref:`about-docs`

.. _user-docs:

.. toctree::
   :maxdepth: 3
   :caption: User Documentation

   getting_started

.. _dev-docs:

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   installation
   testing
   documentation
   api/index

.. _about-docs:

.. toctree::
   :maxdepth: 3
   :caption: About

   contributing
   code_of_conduct
   license

.. bibliography::
   :all:
