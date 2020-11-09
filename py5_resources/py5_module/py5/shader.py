# -*- coding: utf-8 -*-
# *** FORMAT PARAMS ***
import functools
from typing import overload, List, Any  # noqa
from nptyping import NDArray, Float  # noqa

import numpy as np  # noqa

from .base import Py5Base
from .image import Py5Image  # noqa
from jpype.types import JException, JArray, JBoolean, JInt, JFloat  # noqa
from .pmath import _numpy_to_pvector, _numpy_to_pmatrix2d, _numpy_to_pmatrix3d  # noqa


py5shader_class_members_code = None  # DELETE


def _return_py5shader(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        return Py5Shader(f(self_, *args))
    return decorated


def _load_py5shader(f):
    @functools.wraps(f)
    def decorated(self_, *args):
        try:
            return Py5Shader(f(self_, *args))
        except JException as e:
            msg = e.message()
            if msg == 'None':
                msg = 'shader file cannot be found'
        raise RuntimeError('cannot load shader file ' + str(args[0]) + '. error message: ' + msg)
    return decorated


def _py5shader_set_wrapper(f):
    @functools.wraps(f)
    def decorated(self_, name, *args):
        args = list(args)
        if isinstance(args[0], np.ndarray):
            array = args[0]
            if array.shape in [(2,), (3,)]:
                args[0] = _numpy_to_pvector(array)
            elif array.shape == (2, 3):
                args[0] = _numpy_to_pmatrix2d(array)
            elif array.shape == (4, 4):
                args[0] = _numpy_to_pmatrix3d(array)
        else:
            def fix_type(arg):
                if isinstance(arg, bool):
                    return JBoolean(arg)
                elif isinstance(arg, int):
                    return JInt(arg)
                elif isinstance(arg, float):
                    return JFloat(arg)
                else:
                    return arg
            args = [fix_type(a) for a in args]
        return f(self_, name, *tuple(args))
    return decorated


class Py5Shader(Py5Base):
    """$classdoc_Py5Shader"""

    def __init__(self, pshader):
        self._instance = pshader
        super().__init__(instance=pshader)


{py5shader_class_members_code}
