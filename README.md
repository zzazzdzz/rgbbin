# rgbbin v1.0.0

RGBBIN is a simple linker for [RGBDS](https://github.com/rednex/rgbds) object files that generates raw binaries instead of ROMs. It is intended to be used in any GameBoy projects that don't compile to a standard ROM, like my recent [April Fools Event 2018](https://github.com/zzazzdzz/fools2018), for which this tool was explicitly created.

RGBBIN includes both:
- A Python 3 library containing the object file parser. It allows to load an object file and read raw contents of all sections within it, as well as get access to all defined symbols, their names and offsets. The library is to be used in custom build scripts. Note: Only Python 3 is supported.
- A simple command-line utility that dumps all sections contained in an object file to corresponding BIN files, and generates a SYM file containing all of the defined symbols. This is for use in Makefiles and other environments with a simple build process. To invoke this tool, run the rgbbin module as a script (`python3 -m rgbbin`).

Note that RGBBIN can't just take anything you throw at it; at the moment, it only supports a limited subset of the RGBDS object file format. The file format itself is also dynamically changing, so compatibility issues may apply. See the "Limitations" section below.

# Installation

It's just a vanilla Python library. Installation doesn't get any easier than dropping the module files wherever you want them to go.

However, you might want to install the library system-wide, so all of your scripts can use it:
```
sudo cp -R rgbbin "`python3 -c "import site; print(site.getsitepackages()[0])"`"
```
Support for `pip` or other package managers might be added in the future.

# Using the command-line utility

By default, the included command-line tool will just take an object file and dump all of its defined sections to BIN files in the current directory. Just invoke it with the object file as an argument: `python3 -m rgbbin main.obj`

Consult the help (`python3 -m rgbbin --help`) for more configuration options.

# Using the library

Here's a code example that loads an object file and prints the contents of the section 'Main':
```python
    import rgbbin.objfile
    with rgbbin.objfile.ObjectFile("main.obj") as obj:
        obj.parse_all()
        print(obj.section_by_name("Main")["data"])
```
A rather short documentation on the ObjectFile class:
- *sections* - An list of dict, each entry representing a single section within the loaded object file.
- *symbols* - An list of dict, each entry representing a single symbol within the loaded object file.
- *parse_header()*, *parse_symbols()*, *parse_sections()*, *parse_patches()* - Parse specific parts of the file. Note that the functions need to be called in this exact order.
- *parse_all()* - Parse the file completely. Equivalent to calling all of the four functions above. This is what you want to use in most of your scripts.
- *section_by_name(name)* - Given a section name, return a dictionary describing its properties. Return None if the section wasn't found.
- *section_by_id(id)* - Given a section ID, return a dictionary describing its properties. Return None if the section wasn't found.
- *symbol_by_name(name)* - Given a symbol name, return a dictionary describing its properties. Return None if the symbol wasn't found.
- *symbol_by_id(id)* - Given a symbol ID, return a dictionary describing its properties. Return None if the symbol wasn't found.
    
The dictionary format of section data:

- *name* - The name of the section, as defined in the source file.
- *origin* - The origin of the section (its starting address).
- *data* - The section contents, as a bytearray.
- *sectid* - The section's ID (its index within the table in the object file).

The dictionary format of symbol data:

- *name* - The name of the symbol. Local symbols are prefixed with the corresponding global symbol's name.
- *value* - The symbol's value. If the symbol was defined as an address (it was a label), the value will be its offset relative to the section's origin. So to calculate the symbol's effective address, add its value to the origin of the section it was defined in.
- *sectid* - Section ID this symbol was defined in.
- *symid* - The symbol's ID (its index within the table in the object file)

# Limitations
The library is designed to work with the version 5 of the object file format, which was used by rgbasm v0.3.3. Object files compiled with the newer versions will not work with this software - however, support for them might be added incrementally in the future.

Only ROM and ROMX sections are recognized by the parser, so any sections you want to extract should have this type. If you want to have a section origin in RAM (for example $DA80), creating a ROM0 section with that origin will still work:
```
SECTION "WRAM", ROM0[$DA80]
```
The RPN commands used to create linking-time patches are not yet supported completely. This essentially means you're restricted to only using addition and subtraction in symbol math. For example `ld hl, symbol+1337` or `ld hl, symbol-1337` will work fine, but `ld hl, symbol*2` will fail with an "unsupported RPN command error". Note that constant calculations are resolved by the compiler and unaffected by this error (`ld hl, $1234*2` or `ld a, 64/8` will work). Again, better support for RPN commands might be added in the future.

All sections must have their origins explicitly defined. Sections with dynamic origins are not supported.

If you wish to use the command-line utility included with the library, make sure your section names are also valid file names for the operating system you're on. For example, exporting a section named "*" will fail on Windows.

