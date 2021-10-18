# *****************************************************************************
#
#   Part of the py5generator project; generator of the py5 library
#   Copyright (C) 2020-2021 Jim Schmitz
#
#   This project is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the
#   Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   This project is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
#   Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program. If not, see <https://www.gnu.org/licenses/>.
#
# *****************************************************************************
from pathlib import Path
import re
from typing import Union
import string

from . import util


CONSTANT_CHARACTERS = string.ascii_uppercase + string.digits + '_'

PY5_CLASS_LOOKUP = {
    'PApplet': 'Sketch',
    'PFont': 'Py5Font',
    'PGraphics': 'Py5Graphics',
    'PImage': 'Py5Image',
    'PShader': 'Py5Shader',
    'PShape': 'Py5Shape',
    'PSurface': 'Py5Surface',
}

SNAKE_CASE_OVERRIDE = {
    'None': 'None',
    'True': 'True',
    'False': 'False',
    'println': 'print',
}


def translate_token(token):
    if all([c in CONSTANT_CHARACTERS for c in list(token)]):
        return token
    if re.match(r'0x[\da-fA-F]{2,}', token):
        return token
    elif (stem := token.replace('()', '')) in PY5_CLASS_LOOKUP:
        return token.replace(stem, PY5_CLASS_LOOKUP[stem])
    elif token in SNAKE_CASE_OVERRIDE:
        return SNAKE_CASE_OVERRIDE[token]
    else:
        token = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', token)
        token = re.sub('([a-z0-9])([A-Z])', r'\1_\2', token)
        return token.lower()


def translate_code(code):
    util.translate_code(translate_token, code)


def translate_file(src: Union[str, Path], dest: Union[str, Path]):
    util.translate_file(translate_token, src, dest)


def translate_dir(src: Union[str, Path], dest: Union[str, Path], ext='.pyde'):
    util.translate_dir(translate_token, src, dest, ext)


__ALL__ = ['translate_token', 'translate_code', 'translate_file', 'translate_dir']

def __dir__():
    return __ALL__