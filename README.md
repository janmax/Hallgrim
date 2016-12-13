# Hallgrim - an ILIAS task generator in Python

## Installation

```
git clone https://gitlab.gwdg.de/j.michal/ilias-generator.git
cd ilias-generator
pip install -e .
```

## Usage

After the install just invoke `hallgrim -h` to see usage. The directory hallgrim
is invoked in, should contain a `config.ini`.

Example scripts can be found [in a seperate repository](https://gitlab.gwdg.de/j.michal/ilias-scripts).

### Dependencies

`pip` will try to install them automatically. If you can figure out how to
replace requests with the native urllib3 - you are welcome to help.

- `mistune`
- `pygments`
- `requests`
- `requests_toolbelt`

### TODO

* Add a more description / documentation.
* Add more functionality (numeric gap, multiple answers per gap, alignment)
* Make parsers more robust.
* Create whole test object with questions for direct import. Create two
versions (one for internal use and one for the test.)
* add zip support

### Notes

The final data is produced in three steps:

1. A python script file with predefined structure that has to export certain
variables in a specified format.
2. An intermediate representation (probably an array that contains relevant
data and assumes unknown properties)
3. The XML structure for one or multiple questions, readable by Ilias.
4. An Ilias object packed as .zip file, ready for upload.

### Testing

The tool will ship with a VirtualBox contaning Ilias Versions used in
production. With `grim.py upload` it is possible to upload these scripts quickly
and see a how they look like in a working ilias system.

The upload script does not work with the university hosted servers.

### LaTeX Support

Hallgrim supports the native latex approach by ILIAS. To typeset a formula just
put it in brackets like this `[[\\sum_{i=1}^n i = \\frac{n(n+1)}{2}]]`. Special
caretakers (mostly `\`) have to be escaped unless you use raw strings (`r'a raw string'`).

### Code Highlighting

Hallgrim uses pygments and the customized mistune parser to highlight different
programming language syntaxes. To highlight a code block just put the language
name right after the delimiters

    ```java
    class Car {
        private float price;
        private String manufacturer;
        public void cheeseCake(int withCream) {
            return () -> ();
        }
    }
    ```

```java
class Car {
    private float price;
    private String manufacturer;
    public void cheeseCake(int withCream) {
        return () -> ();
    }
}
```

It is not possible to copy code by default, but `_copy` can be appended to the
language's name if copyable code is desired.

    ```java_copy
    class Car {
        private float price;
        private String manufacturer;
        public void cheeseCake(int withCream) {
            return () -> ();
        }
    }
    ```

It is possible to include gaps withing code blocks.

