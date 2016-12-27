How to implement different question types
*****************************************

All scripts have to be valid Python 3 scripts and the file name should therefore
end in ``.py``. In order to parse them with hallgrim you further have to export
at least the fields ``meta``, ``task`` and ``feedback``. They all follow a
different syntax that is used by the the parser.

The ``meta`` field contains information about the author and the name of the
task and most important the question type. It can further set options on how the
script should be processed. An example would be

.. code-block:: python

    meta = {
        'author': 'John Doe',
        'title': 'A very difficult task',
        'type': 'gap',
        'points': 3000,
    }

Scripts can be easily generated with default values (or those specified in
``config.ini``). Just invoke on the commandline:

.. code-block:: bash

    hallgrim new <script name>

The full usage is

.. code-block:: bash

    hallgrim new [-h] [-t TYPE] [-a AUTHOR] [-p POINTS] NAME


Choice questions
================

The fields ``task`` and ``feedback`` can have arbitrary content. The number
of choices is specified in the ``choices`` field, which has to be exported. The
syntax is very straight forward for both types of question.

The answers are shuffled by ILIAS by default. To disable this behaviour add this
to the meta field.

.. code-block:: python

    'shuffle': False,


Single choice
-------------

Only one answer can be selected by the student but it is possible to give
varying points for different answers. The syntax can look like this:

.. code-block:: text

    choices = """
        [ ] a very wrong answer
        [ ] not correct
        [2] this is half correct
        [4] this is the best solution
    """

If the number of points is given in the meta field it is possible to just use an
``X`` instead of the number of points.

.. code-block:: text

    [ ] not correct
    [ ] not correct
    [X] the only correct answer

Multiple choice
---------------

Works just like :ref:`Single Choice` but Multiple Choice allows multiple answers
by the user later. A syntax example:

.. code-block:: text

    choices = """
        [0.5] still a valid answer
        [ ] not correct
        [1] correct
        [ ] not correct
    """

It is also possible to make correct answers with an ``X`` then the number of
points specified in ``meta['points']`` is given. In contrast to other question
types, that field should not contain the total amount of points but rather the
amount of points rewarded per question.

Gap questions
=============

It is possible to mix all the gap types, so any task can contain regular
text gaps along with numeric gaps and selection gaps. The question type for all
of these subtypes is therefore ``gap``.

The general syntax is always an opening bracket ``[gap_type(0.0P)]`` that states
how many points will be given for this question type. The gap is than closed
by [/gap_type] with content following the gap syntax in between.

All gaps can be placed into code sections.

Text gap
--------

A text gap as the following syntax (also used by ILIAS):

.. code-block:: text

    [gap(0.0P)]Answer 1, Answer 2, Answer 3[/gap]

All these answers will be accepted as correct and the number of points in
the opening bracket will be rewarded. No line break should occur within the gap.

Numeric gap
-----------

A numeric gap can either be

.. code-block:: text

     [numeric(4P)]<value>,<min>,<max>[/numeric]

or

.. code-block:: text

    [numeric(4P)]<value>[/numeric]

In the latter case ``min == max == value`` will be assumed. Value should be
of type ``int`` of ``float``.

Selection gap
-------------

Only the selection gap follows a slightly different syntax, that instead is
similar to the syntax of :ref:`Choice questions`:

.. code-block:: text

    [select]
    [1] int n_ze = m.length;
    [ ] int n_ze = m[0].length;
    [ ] int n_ze = m.length();
    [ ] int n_ze = m[0].length();
    [/select]

It is considered good practise to define these gaps outside of the main task and
include them via string formatting if the gap is part of source code that
should remain readable within the task.

It is possible to write a selection gap within one line by using escaped
newlines:

.. code-block:: text

    [select][1] int n_ze = m.length;\n[ ] int n_ze = m[0].length;\n[ ] int n_ze = m.length();\n[ ] int n_ze = m[0].length();\n[/select]


Order questions
===============

Ordering questions follow a very simple syntax and can be written like this

.. code-block:: text

    order = """
    -- Answer A
    -- Answer B
    -- Answer C
    -- Answer D
    """

or alternatively like this

.. code-block:: text

    order = "Answer A -- Answer B -- Answer C -- Answer D"

If a question should be ordered horizontally, just put this in the ``meta``
field (Not implemented).

.. code-block:: python

    'alignment': 'horizontal',

Custom Markdown in Hallgrim
***************************

Hallgrim script do not need any HTML formatting. Thanks to `mistune`_,
everything works with Markdown. To find out how markdown works take a look
`here`_.

There are some customizations to the markdown Hallgrim uses.

LaTeX
=====

Hallgrim supports the native LaTeX approach by ILIAS. To typeset a formula just
put it in brackets like this:

.. code-block:: text

    [[\\sum_{i=1}^n i = \\frac{n(n+1)}{2}]]

Special caretakers (mostly ``\``) have to be escaped unless you use raw strings
(``r'a raw string'``).

Syntax highlighting
===================

Code highlighting works out-of-the-box with Hallgrim. For syntax highlighting
the `pygments`_ name of a language (often intuitive) has to be put on the first
line of the code block. By default it is not possible to copy code. It can be
enabled for each code block individually by appending ``_copy`` to the language
name.

.. code-block:: text

    ```java_copy
    class Car {
        private float price;
        private String manufacturer;
        public void cheeseCake(int withCream) {
            return () -> ();
        }
    }
    ```

.. code-block:: java

    class Car {
        private float price;
        private String manufacturer;
        public void cheeseCake(int withCream) {
            return () -> ();
        }
    }


How to parametrize questions
****************************

You are using Python! So you have access to all the libraries in your
environment to create tasks that will have different values every time they are
used to convert a Hallgrim script into a ILIAS XML task.

By default Hallgrim creates only one instance of a script. In order to create
a question pool, the meta field as to contain a key-value pair for the number
of instances:

.. code-block:: python

    meta = {
        'author': 'John Doe',
        'title': 'A very simple task, but 80 of them',
        'type': 'gap',
        'instances': 80,
    }

If you set the ``-p`` option for the generator, it will produce the specified
number of tasks. It could look like this:

.. code-block:: bash

    hallgrim gen -p parametrized_gap_task.py

Hallgrim will output the file to ``output/A very simple task, but 80 of
them.xml`` as usual.

A very simple complete example could look like this:

.. code-block:: python

    from random import randint, sample

    meta = {
        'author': 'John Doe',
        'title': 'Parameter example',
        'type': 'single choice',
        'instances': 30,
        'points': 4,
    }

    a = randint(-50, 49)
    b = randint(-50, 49)


    def get_answers(right, count=4):
        possible = sample(range(-100, a+b), count//2) + \
            sample(range(a+b+1, 100), count//2-1) + [a+b]
        return [('X' if answer == right else ' ', answer) for answer in possible]


    task = """ What is the answer to the question {} + {}?""".format(a, b)

    choices = '\n'.join('[%s] a + b = %d' % c for c in get_answers(a+b))

    feedback = "[[a + b = {}]]".format(a + b)

.. _mistune: https://github.com/lepture/mistune
.. _here: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
.. _pygments: http://pygments.org/docs/lexers/ language
