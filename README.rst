pysum: summarize pandas dataframes
---------------------------------------

.. image:: https://github.com/soodoku/pysum/workflows/test/badge.svg
    :target: https://github.com/soodoku/pysum/actions?query=workflow%3Atest
.. image:: https://img.shields.io/pypi/v/pysum.svg
    :target: https://pypi.python.org/pypi/pysum
.. image:: https://readthedocs.org/projects/pysum/badge/?version=latest
    :target: http://pysum.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://static.pepy.tech/badge/pysum
    :target: https://pepy.tech/project/pysum

``pysum`` takes a pandas dataframe (and a few others arguments to
customize the output) and creates a markdown, html, or xlsx report with
summary of each of variables in the dataframe.

The program iterates through each of the columns in the dataframe and
based on the datatype, creates summary statistics for each, and prints
them out to a table.

Inputs
~~~~~~

The function takes the following arguments:

1. ``dataframe``: pandas dataframe. No Default. The passed dataframe
   must also have an attribute ``name`` that carries the ``name`` of the
   dataframe. See examples for clarification.
2. ``round_digits``: Integer. Digits to which the numbers reported
   should be rounded. Default is 2.
3. ``var_numbers``: Boolean. Whether or not to add a column indicating
   the column number. Default is ``true``.
4. ``missing_col``: Boolean. Adds a column that reports proportion
   missing. Default in true.
5. ``max_distinct_values``: Numeric. The maximum number of values to
   display frequencies for. If variable has more distinct values than
   this number, the remaining frequencies will be reported as a whole,
   along with the number of additional distinct values. Defaults to 10.
6. ``max_string_width``: Integer. Limits the number of characters to
   display in the frequency tables. Default is 25.
7. ``output_type``: String. The file format of the output file.
   ``xlsx, html,  markdown``. Default is ``html``.
8. ``output_file``: String. The path and filename to which the script
   should output the results. Default is ``summary.html`` in the local
   directory
9. ``append``: Boolean. If there is an existing file, should we append
   the results or should we overwrite the file. Default is ``true``.
   When append is ``true``, the results are appended. When it is
   ``false``, the file is overwritten.

The ``html`` output also depends on `custom.css <custom.css>`__ in the
local folder.

Output
~~~~~~

The output is a xlsx, html, or markdown file. For numeric columns, it
reports mean, standard deviation, minimum, maximum, median, IQR, Number
of distinct values, Percentage that are valid, and Percentage missing,
by default.

**Definitions of Things in Output**

1. Valid = entries with non-missing values
2. mean (sd) = mean (standard deviation).
3. min = minimum
4. med = median
5. max = maximum
6. IQR = Interquartile range
7. CV = Coefficient of variation

For character vectors, it reports as many as ``max_distinct_values``,
reports the number of other values, and their percentage. It also
reports percentage of observations that are valid and that are missing
by default.

Limitations: Dates by default are parsed as characters. Dates are best
handled as numeric. But given the variety of formats in which dates
appear, no standard support is offered for now.

Running the Script
~~~~~~~~~~~~~~~~~~

Install the requirements:

::

    pip install -r requirements.txt

You also need ``pandoc`` to be installed on your machine.

Examples
~~~~~~~~

`Iris data <https://archive.ics.uci.edu/ml/datasets/iris>`__:

::

    import pandas
    import pysum

    # Load dataset
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = pandas.read_csv(url, names=names)

    # Pass name of the dataset; required
    dataset.name = 'iris'

    pysum.summarizeDF(dataset)
    pysum.summarizeDF(dataset, output_type = "xlsx", append = False)
    pysum.summarizeDF(dataset, output_type = "markdown", append = False)

`Markdown
Output <https://github.com/soodoku/pysum/blob/master/pysum/examples/summary.md>`__,
`HTML
Output <https://htmlpreview.github.io/?https://github.com/soodoku/pysum/blob/master/pysum/examples/summary.html>`__
and `XLSX
Output <https://github.com/soodoku/pysum/blob/master/pysum/examples/summary.xlsx>`__

Attribution
~~~~~~~~~~~

The package is based on https://github.com/dcomtois/summarytools
