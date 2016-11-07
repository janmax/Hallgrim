# Hallgrim - an ILIAS task generator in Python

## Usage

Invoke the script with `python3 grim.py -h` in order to see usage. Currently
many features are not yet implemented. Single and Multiple Chice questions
can be generated also in parametrized form.

Example scripts can be found in `scripts/`.

A first version of the tool that relied on autoilias is still in the repository
(see `generator.py`). It will be removed as soon as the necessary features are
implemented.

## TODO

* Add a good description / documentation.
* Add more functionality (gap, alignment, etc.)
* Make parsers more robust.
* reverse ILIAS authentication mechanism for automated upload.

### Notes

The final data is produced in three steps:

1. A python script file with predefined structure that has to export certain
variables in a specified format.
2. An intermediate representation (probably an array that contains relevant
data and assumes unknown properties)
3. The XML structure for one or multiple questions, readable by Ilias.
4. An Ilias object packed as .zip file, ready for upload.
