========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/libpycontainerize/badge/?style=flat
    :target: https://readthedocs.org/projects/libpycontainerize
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/tooringanalytics/libpycontainerize.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/tooringanalytics/libpycontainerize

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/tooringanalytics/libpycontainerize?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/tooringanalytics/libpycontainerize

.. |requires| image:: https://requires.io/github/tooringanalytics/libpycontainerize/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/tooringanalytics/libpycontainerize/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/tooringanalytics/libpycontainerize/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/tooringanalytics/libpycontainerize

.. |version| image:: https://img.shields.io/pypi/v/pycontainerize.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/pycontainerize

.. |commits-since| image:: https://img.shields.io/github/commits-since/tooringanalytics/libpycontainerize/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/tooringanalytics/libpycontainerize/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/pycontainerize.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/pycontainerize

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pycontainerize.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/pycontainerize
WARNING: WORK IN PROGRESS
=========================

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/pycontainerize.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/pycontainerize


.. end-badges

A containerization and deployment tool for python applications and services

* Free software: BSD license

Installation
============

::

    pip install pycontainerize

Documentation
=============

https://libpycontainerize.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
