========
aglcheck
========

.. contents::

What is aglcheck?
-----------------
*aglcheck* is a python library for analyzing fragment-based, non-grammatical 
similaritites between strings used in artificial grammar learning (AGL) 
experiments. It has lower-level functions to analyze and compare individual
strings, but probably even more useful is its functionality to easily compare
sets of strings and visualize the results in image plots, or in tables that
highlight matching string fragments in color. Further, similarity values
between sets of strings sets are available as data frames for statistical
analyses, for example to test for association with behavioral responses, in
the Python library Pandas_.

.. _Pandas: http://pandas.pydata.org

The goal of *aglcheck* is to enable the fast identification of potential
problems in experimental designs. It can be useful for those who design an
AGL experiment, but also for those who review an AGL manuscript for a
scientific journal or want to evaluate the likelihood of alternative
explanations in published work in which the possibility of fragment-based
similarity may not have been (sufficiently) considered by authors and
reviewers.

*aglcheck* is already useful from this point of view, but it is still being
developed. A future goal is to make it trivially easy to use, perhaps even
without installing a Python environment (i.e. through a Jupyter Notebook
webserver). For now you need a Python environment, though (see below).

Another explicit goal is to make the software very reliable. Users should have
high confidence that the results are correct, given that they are designing
scientific experiments or checking the experimental design or results of
others. A testing framework is in place, and test cases for the most important
algorithms are included. In addition, everything is programmed in Python, and
the code is open source, so it is easy to inspect what is going on under the
hood.

Lastly, *aglcheck*, is easy to extend. With a few lines of Python you can
contribute your own algorithm, which can then be used within a framework that
does string reading and visualization for you.

Example
-------
An example of how visualization can be useful, consider the following strings,
used in Wilson et al. (2015) Nat. Commun. [http://dx.doi.org/10.1038/ncomms9901]:

+-----------+-------+---------+
| type      | label | string  |
+===========+=======+=========+
|           | E1    |  acf    |
|           +-------+---------+
|           | E2    |  acfc   |
|           +-------+---------+
|           | E3    |  acgf   |
|           +-------+---------+
|           | E4    |  acgfc  |
|           +-------+---------+
| Exposure  | E5    |  adcf   |
| strings   +-------+---------+
|           | E6    |  adcfc  |
|           +-------+---------+
|           | E7    |  adcfcg |
|           +-------+---------+
|           | E8    |  adcgf  |
|           +-------+---------+
|           | E9    |  acgfcg |
+-----------+-------+---------+
|           | CT1   |  acgfc  |
| Grammar   +-------+---------+
| Cosistent | CT2   |  adcfcg |
| Test      +-------+---------+
| strings   | CT3   |  acfcg  |
|           +-------+---------+
|           | CT4   |  adcgfc |
+-----------+-------+---------+
|           | VT1   |  afgcd  |
| Grammar   +-------+---------+
| Violating | VT2   |  afcdgc |
| Test      +-------+---------+
| strings   | VT3   |  fadgc  |
|           +-------+---------+
|           | VT4   |  dcafgc |
+-----------+-------+---------+

In this string design, there is a bias in shared maximum fragment length (A)
and corresponding duration (B), which is much more easily seen in an image plot
than in the table above:

.. image:: example_figures/example_fig_sharedchunklength_1.png
    :width: 100%

Quantifications and visualizations can be produced based on a very simple,
human readable and writable text file (yaml format) that lists the strings of
interest, and, optionally, defines categories to be compared and other
information (see example_)

.. _example: https://github.com/gjlbeckers-uu/aglcheck/blob/master/aglcheck/datafiles/wilsonetal_natcomm_2015.yaml

aglcheck can produce HTML tables that highlight in color the specific
similarities between individual strings (e.g., see table_)

.. _table: https://rawgit.com/gjlbeckers-uu/aglcheck/master/example_figures/example_table.html

*aglcheck* was initially written to analyze string sets for potential confounds
based on acoustic similarity in a sample of 9 AGL studies in nonhuman animals
for the scientific paper:

Beckers, G.J.L., Berwick B.C., Okanoya, K. and Bolhuis, J.J. (2016) What do
animals learn in artificial grammar studies? *Neuroscience & Biobehavioral
Reviews* [http://dx.doi.org/10.1016/j.neubiorev.2016.12.021]

See the supplementary information of this paper to see the results of such
analyses: here_.

.. _here: https://rawgit.com/gjlbeckers-uu/aglcheck/master/stimulussets_analyzed/suppl_info_beckers_etal_2016_jneurobiorev_revision2.html

These were produced with version 0.1.0, which is saved as a separate branch on
github. However, the current wider objective is to provide visualization
software that can be used to analyze AGL string set design more generally.


Development status
------------------
This is beta software. It does what it was initially was designed for, and
should also be usable for other applications. The lack of formal documentation
is the biggest hurdle, but there is a tutorial jupyter notebook that should be
sufficient as an example of how to use aglcheck.

A testing framework is in place and test cases for the most important
algorithms are included. To run the test, use 'aglcheck.test()'.

The 0.1.x series is intended to remain compatible with the the jupyter
notebook that produces the supplementary information. The 0.2.x series should
be refactored so that functions and classes are more logically named and
organized for general use.

Contributions in any form are very welcome.

Documentation
-------------
There is no formal documentation yet, but for now the jupyter notebook in the
tutorials_ folder show basic usage.

.. _tutorials: https://github.com/gjlbeckers-uu/aglcheck/tree/master/tutorials


Installation
------------
The *aglcheck* library requires Python 2.7 or 3.5 or higher, and the packages
*numpy*, *matplotlib*, *yaml*, and *pandas*. I recommend the scientific Python
distribution Anaconda_ for easy installation, although it is not required.

.. _Anaconda: https://www.continuum.io/downloads

I also recommend using Jupyter_ Notebook for interactive data science and
reproducible and documented analyses.

.. _Jupyter: https://jupyter.org/index.html


Copyright and License
---------------------
:copyright: Copyright 2016-2017 by Gabriel Beckers, Utrecht University.
:license: 3-Clause Revised BSD License, see LICENSE.txt for details.

Contact
-------
Gabriel Beckers, Utrecht University, https://www.gbeckers.nl
