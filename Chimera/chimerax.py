import argparse
import os
import sys
import xml.etree.ElementTree as ET


def argument_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-i', '--input', dest='input', type=str, required=True,
        help='Required; Specify an input file (.chimerax)')
    arg_parser.add_argument(
        '-o', '--output', dest='output', type=str, required=False,
        default=None, help='Optional; Specify an output path')
    return arg_parser.parse_args()


def name_outfile(infile):
    if infile.endswith('.chimerax'):
        return f'{infile[:-9]}.cxc'
    else:
        return f'{infile}.cxc'


def convert_chimerax2cxc(infile, outfile):
    myTree = ET.parse(infile)
    ChimeraPuppet = myTree.getroot()
    pdb = ChimeraPuppet[0][0].attrib['id']
    lines = [f'open {pdb}']
    commands = ChimeraPuppet[1]
    for command in commands:
        new_cmd = convert_command(command.text)
        if new_cmd:
            lines.append(new_cmd)
    with open(outfile, 'w') as f:
        f.write('\n'.join(lines))


def convert_command(command):
    elements = command.split(' ')
    cmd = ''
    if elements[0] == 'setattr':
        level = elements[1]
        if elements[2] == 'label':
            cmd = 'label'
    elif elements[0] == 'color':
        cmd = 'color'
    elif elements[0] == 'surface':
        cmd = 'surface'
    elif elements[0] == 'surftrans':
        cmd = 'transparency'

    if cmd == 'label':
        value = elements[3]
        specifier = elements[4]
        specifier = _convert_specifier(specifier)
        level = _convert_level(level)
        return f'label {specifier} {level} text {value}'
    elif cmd == 'color':
        colorname = elements[1]
        specifier = elements[2]
        specifier = _convert_specifier(specifier)
        return f'color {specifier} {colorname}'
    elif cmd == 'surface':
        return 'surface'
    elif cmd == 'transparency':
        percent = elements[1]
        return f'transparency {percent}'


def _convert_specifier(specifier):
    # Assumes a format like ":88.A@OG"
    index = specifier.find('.')
    if index < 0:
        return specifier
    residues = specifier[:index]
    chain = specifier[index+1]
    atoms = specifier[index+2:]
    return f'/{chain}{residues}{atoms}'


def _convert_level(level):
    # a | r | m | b | p | g
    if level == 'a':
        return 'atoms'
    elif level == 'r':
        return 'residues'
    elif level == 'b':
        return 'bonds'
    elif level == 'p':
        return 'pseudobonds'
    else:  # m or g
        print(f'Unable to process "{level}"')
        return level


def main():
    args = argument_parser()
    infile = args.input
    outfile = args.output
    if not os.path.exists(infile):
        sys.exit('Error: Failed to find "{infile}". ')
    if outfile is None:
        outfile = name_outfile(infile)
    convert_chimerax2cxc(infile, outfile)


if __name__ == '__main__':
    main()
