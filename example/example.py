import rgbbin.objfile

obj = rgbbin.objfile.ObjectFile("example.obj")
obj.parse_all()

for section in obj.sections:
    print("Section '%s':" % section["name"])
    print("Contents:")
    print(" ".join(["%.2X" % i for i in section["data"]]))

print("Symbols:")
for symbol in obj.symbols:
    origin = obj.section_by_id(symbol['sectid'])['origin']
    print("%s - address $%.4X" % (symbol['name'], symbol['value'] + origin))
