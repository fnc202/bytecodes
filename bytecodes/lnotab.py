"""Parse and create the line No. table."""


def parse_lnotab(lnotab, firstline, bytecode_len):
    """Parse the line No. table.

    Args:
        lnotab (bytes): the line No. table
        firstline (int): the first line of the code
        bytecode_len (int): the length of the bytecode

    Yields:
        tuple: address of the bytecode, line number of the source code
    """
    byte_increments = lnotab[0::2]
    source_increments = lnotab[1::2]
    srcline = firstline
    byteaddr = 0
    last_srcline = None
    for byte_inc, src_inc in zip(byte_increments, source_increments):
        if byte_inc:
            if srcline != last_srcline:
                yield (byteaddr, srcline)
                last_srcline = srcline
            byteaddr += byte_inc
            if byteaddr >= bytecode_len:
                return
        if src_inc >= 0x80:
            src_inc -= 0x100
        srcline += src_inc
    if srcline != last_srcline:
        yield (byteaddr, srcline)
