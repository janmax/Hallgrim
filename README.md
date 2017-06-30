# Hallgrim - an ILIAS task generator in Python

### Installation

```
pip install hallgrim
```

### Usage

After the install just invoke `hallgrim -h` to see usage. The directory hallgrim
is invoked in, should contain a `config.ini`.

Example scripts can be found
[in a seperate repository](https://gitlab.gwdg.de/j.michal/ilias-scripts).

### Documentation

Please see the documentation. All the functionality is explained there among
with some code documentation. It was generated with Sphinx. Its output can be found
[here](http://user.informatik.uni-goettingen.de/~j.michal/hallgrim/index.html).


### Notes

The final data is produced in three steps:

1. A python script file with predefined structure that has to export certain
   variables in a specified format.
2. An intermediate representation (probably an array that contains relevant
   data and assumes unknown properties)
3. The XML structure for one or multiple questions, readable by Ilias.
4. An Ilias object packed as .zip file, ready for upload.

### Testing

The tool will ship with a VirtualBox containing Ilias Versions used in
production. With `hallgrim upload <xml script>` it is possible to upload these
scripts quickly and see a how they look like in a working Ilias system.

The upload script does not work with the university hosted servers.

