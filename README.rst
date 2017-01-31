========
aglcheck
========

.. contents::

What is aglcheck?
-----------------
*aglcheck* is a python library for analyzing non-grammatical similaritites
between strings used in artificial grammar learning (AGL) experiments.

*aglcheck* was initially written to analyze string sets for unintentional
confounds based on acoustic similarity in a sample of 9 AGL studies in nonhuman
animals for the scientific paper:

Beckers, G.J.L., Berwick B.C., Okanoya, K. and Bolhuis, J.J. (2016) What do
animals learn in artificial grammar studies? Neuroscience & Biobehavioral
Reviews [http://dx.doi.org/10.1016/j.neubiorev.2016.12.021])

However, the wider objective is to provide visualization software that can be
used to analyze AGL string set design more generally.

An example of a visualization that shows a bias in shared chunk length and
corresponding duration is ('E' strings are exposure strings, 'CT' grammar
correct test strings, and 'VT' grammar violating test strings):

    .. image:: example_figures/example_fig_sharedchunklength_1.png
        :width: 100%

Quantifications and visualizations can be produced from a very simple text file
(yaml format) that lists the strings of interest, and, optionally, provides
token durations (see example_)
    .. _example: aglcheck/datafiles/wilsonetal_natcomm_2015.yaml

More details on matches at the level of individual strings can be scrutinized
in HTML tables (e.g., see table_)
    .. _table: https://rawgit.com/gjlbeckers-uu/aglcheck/master/example_figures/example_table.html



Development status
------------------
This is alpha software. It does what it was initially was designed for,
and should also be usable for other applications. The lack of documentation is
the biggest hurdle, but see below. Contributions in any form are very welcome.

The 0.1.x series is intended to remain compatible with the the jupyter
notebook that produces the supplementary information. The 0.2.x series should
be refactored so that functions and classes are more logically named and
organized for general use.


Documentation
-------------
There is no documentation yet, but for now the jupyter notebooks in the
tutorials folder show basic usage.


Installation
------------
The *aglcheck* library requires Python 2.7 or 3.5 or higher, and the packages
*numpy*, *matplotlib*, *yaml*, and *pandas*. I recommend the scientific Python
distribution Anaconda_ for easy installation, although it is not required.
    .. _Anaconda: https://www.continuum.io/downloads

Copyright and License
---------------------

:copyright: Copyright 2016 by Gabriel Beckers, Utrecht University.
:license: 3-Clause Revised BSD License, see LICENSE.txt for details.

Contact
-------
Gabriel Beckers, Utrecht University, https://www.gbeckers.nl