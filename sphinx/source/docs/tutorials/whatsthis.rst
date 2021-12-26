Preparatory knowledge
=====================

Python's bytecode
-----------------
Python looks like an interpretation execution language,
but it needs to be compiled into Python bytecode, just like Java.

All the python's bytecodes are here: :ref:`the dis module <bytecodes>`.

They are included in code objects together with variables, constant tables, etc.,
and then included in functions, modules, generators, etc.

Code objects
------------
Python's bytecodes are packaged in code objects. They have many attributes, but they are not editable.
CodeType.co_code is just a bytes object. It's not verbose at all. That why we make this module.
