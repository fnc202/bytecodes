"""Testing."""

from bytecodes.func import Func
from bytecodes.insn import LocalInstr, ConstInstr, Instr

TEST_D = 0
TEST_E = 1


def test(num):
    """Just a testing tool."""
    print(TEST_D, TEST_E)
    num_and_two = 2+num
    if num_and_two > 0:
        return 1+num+num_and_two
    print(-1)
    return -1-num-num_and_two


# pylint: disable=not-callable
fo = Func(test)
print(fo.consts)
fo.varnames.append("z")
fo.consts.append(114514)
fo.ins[28] = LocalInstr("STORE_FAST", "z", fo, True)
fo.ins.append(LocalInstr("LOAD_FAST", "z", fo, True))
fo.ins.append(ConstInstr("LOAD_CONST", 114514, fo, True))
fo.ins.append(Instr("BINARY_ADD", 0, fo))
fo.ins.append(Instr("RETURN_VALUE", 0, fo))
fo.disasm()
print(fo.tofunc()(-5))
