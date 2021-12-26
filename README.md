BYTECODES
=========
这是一个纯Python的简单的Python字节码框架。
```python
from bytecodes.func import Func
from bytecodes.insn import Instr
def add(a, b):
    return a+b
func_object = Func(add)
func_object.ins[2] = Instr("BINARY_SUBTRACT", 0, func_object)
func_object.name = "subtract"
subtract = func_object.tofunc()
```
以上代码修改add函数字节码得到subtract函数。
