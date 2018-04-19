import struct

def parse(objfile, x):
    pos = 0
    stack = []
    while pos < len(x):
        code = x[pos]
        pos += 1
        if code == 0x00:
            arg2 = stack.pop()
            arg1 = stack.pop()
            stack.append(arg1 + arg2)
        elif code == 0x01:
            arg2 = stack.pop()
            arg1 = stack.pop()
            stack.append(arg1 - arg2)
        elif code == 0x80:
            stack.append(struct.unpack("<I", x[pos:pos+4])[0])
            pos += 4
        elif code == 0x81:
            sid = struct.unpack("<I", x[pos:pos+4])[0]
            pos += 4
            section = objfile.sections[objfile.symbols[sid]['sectid']]
            origin = section['origin']
            offset = objfile.symbols[sid]['value']
            stack.append(origin + offset)
        else:
            raise NotImplementedError("unsupported RPN command %.2x" % code)
    return stack.pop()
