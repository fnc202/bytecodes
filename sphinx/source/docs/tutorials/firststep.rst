First step
==========
You will learn how to use :py:class:`bytecodes.func.Func` and :py:class:`bytecodes.insn.Instr` in this passage.

Task
----
Here is a python function:
::
    def add(a, b):
        return a+b

Now we want to create a new function named "subtract" by editing the bytecode of the function "add", which will perform subtraction. How to do that?

How to do that?
---------------
We can make a function editable by :py:class:`bytecodes.func.Func`.
So we should create a :py:class:`bytecodes.func.Func` object.::
    func_object = Func(add)

What happens?

Func.\__init\__ reads the function \"add\"\'s bytecode. We can edit it now. Let's look at its bytecode.

>>> func_object.disasm()
0 LOAD_FAST a
2 LOAD_FAST b
4 BINARY_ADD
6 RETURN_VALUE

Look at the instuction \"BINARY_ADD\". It performs an addition operation.
It takes two numbers from the top of the stack and puts the result back on the stack.
The instruction \"BINARY_SUBTRACT\" performs a subtraction operation. We can change BINARY_ADD to BINARY_SUBTRACT to slove the problem.
::
    func_object.ins[2] = Instr("BINARY_SUBTRACT", 0, func_object)

Change the name.
::
    func_object.name = "subtract"

Finally, we have to convert the :py:class:`bytecodes.func.Func` object into a function to run.
::
    subtract = func_object.tofunc()

Let's test it!

>>> subtract(1, 1) 
0
>>> subtract(1, 2) 
-1
>>> subtract(1, 10) 
-9
>>> subtract(0, 10) 
-10
>>> subtract(5, 10) 
-5

Full code:
::
    from bytecodes.func import Func
    from bytecodes.insn import Instr
    def add(a, b):
        return a+b
    func_object = Func(add)
    func_object.ins[2] = Instr("BINARY_SUBTRACT", 0, func_object)
    func_object.name = "subtract"
    subtract = func_object.tofunc()
