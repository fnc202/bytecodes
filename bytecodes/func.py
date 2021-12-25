"""修改Python方法、函数中的一切！
Change everything in a function/method!"""
import typing
import types
import opcode
from bytecodes.insn import Instr, FreeInstr, JabsInstr, JrelInstr
from bytecodes.insn import NameInstr, ConstInstr, LocalInstr, CompareInstr


class Func:
    """允许操作代码与其他东西
    Able to change code and others

    Attributes:
        consts (list): 常量列表
        names (list): 全局变量列表
        varnames (list): 局部变量表
        freevars (list): 自由（？）变量表
        argcount (int): 参数数量
        cellvars (list): ？
        filename (str): 文件名
        firstlineno (int): 第一行行号
        flags (int): 标志位，一般为67
        kwonlyargcount (int): 仅关键字参数量
        lnotab (bytes): 行号表
        name (str): 名称
        nlocals (int): 局部变量数
        posonlyargcount (int): 仅位置字参数量
        stacksize (int): 栈大小，一般为11
        ins (list): 指令表

    Args:
        func(FunctionType/NoneType): 如为None，调用emptyinit，否则调用fromfunction
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, func: typing.Optional[types.FunctionType] = None):
        if func is None:
            self.emptyinit()
        else:
            self.fromfunction(func)

    def fromfunction(self, func: types.FunctionType):
        """通过真正的函数、方法创建Func对象
        Create Func object by a real function/method.

        Args:
            func (FunctionType): 原函数
        """
        codeobj: types.CodeType = func.__code__
        self.globals = func.__globals__
        self.consts = list(codeobj.co_consts)
        self.names = list(codeobj.co_names)
        self.varnames = list(codeobj.co_varnames)
        self.freevars = list(codeobj.co_freevars)
        self.argcount = codeobj.co_argcount
        self.cellvars = list(codeobj.co_cellvars)
        self.filename = codeobj.co_filename
        self.firstlineno = codeobj.co_firstlineno
        self.flags = codeobj.co_flags
        self.kwonlyargcount = codeobj.co_kwonlyargcount
        self.lnotab = codeobj.co_lnotab
        self.name = codeobj.co_name
        self.nlocals = codeobj.co_nlocals
        self.posonlyargcount = codeobj.co_posonlyargcount
        self.stacksize = codeobj.co_stacksize
        ins = []
        code = codeobj.co_code
        for i in range(0, len(code), 2):
            opc = code[i]
            arg = code[i+1]
            if opc in opcode.hasconst:
                ins.append(ConstInstr(opc, arg, self))
            elif opc in opcode.haslocal:
                ins.append(LocalInstr(opc, arg, self))
            elif opc in opcode.hasname:
                ins.append(NameInstr(opc, arg, self))
            elif opc in opcode.hasjrel:
                ins.append(JrelInstr(opc, arg, self))
            elif opc in opcode.hasjabs:
                ins.append(JabsInstr(opc, arg, self))
            elif opc in opcode.hascompare:
                ins.append(CompareInstr(opc, arg, self))
            elif opc in opcode.hasfree:
                ins.append(FreeInstr(opc, arg, self))
            else:
                ins.append(Instr(opc, arg, self))
        self.ins = ins

    def emptyinit(self):
        """创建空Func对象
        Create a empty Func object"""
        self.globals = {}
        self.consts = []
        self.names = []
        self.varnames = []
        self.freevars = []
        self.argcount = 0
        self.cellvars = []
        self.filename = ""
        self.firstlineno = 1
        self.flags = 67
        self.kwonlyargcount = 0
        self.lnotab = b''
        self.name = ""
        self.nlocals = 0
        self.posonlyargcount = 0
        self.stacksize = 11
        self.ins = []

    def disasm(self):
        """显示反汇编结果
        Show disassembly result"""
        addr = 0
        for i in self.ins:
            print(addr, i.disasm())
            addr += 2

    def tobytes(self) -> bytes:
        """转换为字节码
        Convert Func object to bytecode

        Returns:
            bytes: 字节码
        """
        result = []
        for i in self.ins:
            result.append(i.tobytes())
        return b''.join(result)

    def tocode(self) -> types.CodeType:
        """转换为code对象
        Convert Func object to code object

        Returns:
            CodeType: code对象
        """
        code = self.tobytes()
        codeobj = types.CodeType(self.argcount, self.posonlyargcount,
                                 self.kwonlyargcount, self.nlocals,
                                 self.stacksize, self.flags, code,
                                 tuple(self.consts), tuple(self.names),
                                 tuple(self.varnames), self.filename,
                                 self.name, self.firstlineno, self.lnotab,
                                 tuple(self.freevars), tuple(self.cellvars))
        return codeobj

    def tofunc(self) -> types.FunctionType:
        """转换为真正的函数
        Convert Func object to real function

        Returns:
            FunctionType: 真正的函数（能调用的那种）
        """
        func = types.FunctionType(self.tocode(), self.globals)
        return func
