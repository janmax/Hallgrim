# Hallgrim - an ILIAS task generator in Python

## Usage

Invoke the script with `python3 gen.py -h` in order to see usage. Very limited
until now.

Example scripts can be found in `scripts/`.

A first version of the tool that relied on autoilias is still in the repository
(see `generator.py`). It will be removed as soon as the necessary features are
implemented.

## TODO

* Add a good description / documentation.
* Add instruction to produce multiple (parametrized) instances of a single
question.
* Add more functionality (gap, alignment, etc.)
* Make parsers more robust.
* reverse ILIAS authentication mechanism for automated upload.
* Enable LaTeX through custom lexer in mistune.

### Notes

The final data is produced in three steps:

1. A python script file with predefined structure that has to export certain
variables in a specified format.
2. An intermediate representation (probably an array that contains relevant
data and assumes unknown properties)
3. The XML structure for one or multiple questions, readable by Ilias.
4. An Ilias object packed as .zip file, ready for upload.
