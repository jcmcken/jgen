# JGen

A command-line utility for generating simple JSON documents without having to worry about escaping or quoting
the inputs.

## Examples

Without any inputs, ``jgen`` generates a blank JSON document:

```bash
[jcmcken@localhost]$ jgen
{}
```

Creating a simple document:

```bash
[jcmcken@localhost]$ jgen foo=bar
{"foo": "bar"}
```

Creating a nested document:

```bash
[jcmcken@localhost]$ jgen foo.bar=baz
{"foo": {"bar": "baz"}}
```

Creating a more complex nested document:

```bash
[jcmcken@localhost]$ jgen foo.bar=baz foo.foo=bar
{"foo": {"foo": "bar", "bar": "baz"}}
```

Working with arrays:

```bash
[jcmcken@localhost]$ jgen foo.bar=a,b,c
{"foo": {"bar": ["a", "b", "c"]}}
```

Use non-strinrg data types (see section below for details):

```bash
[jcmcken@localhost]$ jgen foo=true bar=null baz=3.141
{"baz": 3.141, "foo": true, "bar": null}
```

## Command-line Options

Some additional command-line options exist for ``jgen``.

* ``-p``/``--pretty-print`` : "Pretty-print" the resulting document
* ``-y``/``--yaml`` : If **PyYAML** library is available, print the document as YAML instead of JSON
* ``--prefix`` : Prepend a prefix to each top-level key in the resulting data

## Data Types

Currently, ``jgen`` does the following type conversions on data values (but **not** keys!):

* If a value is either of the strings ``"true"`` or ``"false"``, the resulting value will be the boolean 
  ``true`` or ``false`` (respectively).
* If a value is the string ``"null"``, the resulting value will be the JSON ``null`` type.
* If a value is "integer-like" (that is if the mapping ``lambda x: str(int(x))`` is the identity mapping),
  the ``int`` function will be applied to the value.
* If a value is "float-like" (that is if the mapping ``lambda x: str(float(x.rstrip("0")))`` is the identity
  mapping), the ``float`` function will be applied to the value.

Note that the JSON specification does **not** allow data keys to be anything except the string type.

## Data Merging

Because ``jgen`` relies on recursive hash merges to build up the JSON document, you need to be careful about
how you specify the data.

For example, if the input string is ``foo.bar=baz foo=baz``, ``jgen`` will take ``foo.bar=baz`` and generate
the document ``{"foo": {"bar": "baz"}}``. Next it will take the string ``foo=baz`` and generate the document
``{"foo": "baz"}``. Since the recursive merge of these two documents is ``{"foo": "baz"}``, some of the data
you specified at the command line is lost.
