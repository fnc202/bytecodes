"""指令
Instructions"""

import typing
import opcode


class Instr:
    """其他指令
    Other opcodes."""
    def __init__(self, opc: typing.Union[int, str], arg, func):
        """初始化指令

        Args:
            opc(int): 操作码
            arg(int): 操作参数
            func(Func): Func对象
        """
        if type(opc) == str:
            opc = self._opc = opcode.opmap[opc]
            self.nopc = opcode.opname[opc]
        else:
            self._opc = opc
            self.nopc = opcode.opname[opc]
        self.arg = arg
        self.func = func
        if not self.check():
            raise ValueError("Check failed.")

    def check(self):
        """检查操作码和其他东西
        Checking Opcode and others

        Returns:
            bool: 检查结果
        """
        opc = self.opc
        return not(opc in opcode.hasconst or
                   opc in opcode.hascompare or
                   opc in opcode.hasfree or
                   opc in opcode.hasjabs or
                   opc in opcode.hasjrel or
                   opc in opcode.haslocal or
                   opc in opcode.hasname)

    @property
    def opc(self):
        """操作码
        opcode
        """
        return self._opc

    @opc.setter
    def opc(self, val):
        """设置操作码
        Sets opcode
        Args:
            val(int): 操作码
            val(str): 操作指令（如LOAD_FAST）
        """
        if isinstance(val, int):
            self.nopc = opcode.opname[val]
            self._opc = val
        else:
            self.nopc = val
            self._opc = opcode.opmap[val]

    def tobytes(self):
        """转为字节码
        To bytecode.

        Returns:
            bytes: 字节码
        """
        return bytes((self._opc, self.arg))

    def disasm(self):
        """返回反编译结果
        Returns disassembly result.

        Returns:
            str: 反汇编结果
        """
        return "%s" % self.nopc


class VarInstr(Instr):
    """仅超类。操作变量、常量的指令。
    Superclass only.Instructions for operating variables and constants."""
    table = []

    def __init__(self, opc, arg, func, val: bool = False):
        """初始化指令
        Args:
            opc(int): 操作码
            arg(int): 操作参数
            func(Func): Func对象
            val(bool): arg是值（True）还是co_xxx的索引（False）
        """
        if val:
            arg = self.table.index(arg)
            self._var = arg
        else:
            self._var = self.table[arg]
        super().__init__(opc, arg, func)

    def check(self):
        return self.arg < len(self.table)

    @property
    def var(self):
        """操作目标
        operating target"""
        return self._var

    @var.setter
    def var(self, val):
        """获取操作目标
        Setter for operating variable"""
        self.arg = self.table.index(val)
        self._var = val

    def disasm(self):
        return "%s %s" % (self.nopc, self._var)


class LocalInstr(VarInstr):
    """opcode.haslocal中的操作码
    Opcodes in opcode.haslocal"""
    def __init__(self, opc, arg, func, val: bool = False):
        self.table = func.varnames
        super().__init__(opc, arg, func, val)

    def check(self):
        return self.opc in opcode.haslocal and super().check()


class ConstInstr(VarInstr):
    """opcode.hasconst中的操作码
    Opcodes in opcode.hasconst"""
    def __init__(self, opc, arg, func, val: bool = False):
        self.table = func.consts
        super().__init__(opc, arg, func, val)

    def check(self):
        return self.opc in opcode.hasconst and super().check()


class NameInstr(VarInstr):
    """opcode.hasname中的操作码
    Opcodes in opcode.hasname"""
    def __init__(self, opc, arg, func, val: bool = False):
        self.table = func.names
        super().__init__(opc, arg, func, val)

    def check(self):
        return self.opc in opcode.hasname and super().check()


class FreeInstr(VarInstr):
    """opcode.hasfree中的操作码
    Opcodes in opcode.hasfree"""
    def __init__(self, opc, arg, func, val: bool = False):
        self.table = func.freevars
        super().__init__(opc, arg, func, val)

    def check(self):
        return self.opc in opcode.hasfree and super().check()


class JrelInstr(Instr):
    """opcode.hasjrel中的操作码
    Opcodes in opcode.hasjrel"""
    def disasm(self):
        return "%s +%s" % (self.nopc, self.arg)

    def check(self):
        return self.opc in opcode.hasjrel


class JabsInstr(Instr):
    """opcode.hasjabs中的操作码
    Opcodes in opcode.hasjabs"""
    def disasm(self):
        return "%s %s" % (self.nopc, self.arg)

    def check(self):
        return self.opc in opcode.hasjabs


class CompareInstr(Instr):
    """opcode.hascompare中的操作码
    Opcodes in opcode.hascompare"""
    def __init__(self, opc, arg, func):
        super().__init__(opc, arg, func)
        self._op = opcode.cmp_op[arg]

    def check(self):
        return self.arg < len(opcode.cmp_op) and self.opc in opcode.hascompare

    @property
    def cmp_op(self):
        """比较操作码
        Comparing op"""
        return self._op

    @cmp_op.setter
    def cmp_op(self, val):
        """设置比较操作码
        Setter for compare op."""
        self.arg = opcode.cmp_op.index(val)
        self._op = val

    def disasm(self):
        return "%s %s" % (self.nopc, self._op)
