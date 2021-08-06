# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generates pybind11 type casters based on Clif_PyObjFrom and Clif_PyObjAs."""

import os
import re

from typing import Generator, List

from clif.protos import ast_pb2
from clif.pybind11 import utils


I = utils.I
_PYOBJFROM_ONLY = ', HasPyObjFromOnly'
_PYOBJAS_ONLY = ', HasPyObjAsOnly'
_CLIF_USE = re.compile(
    r'// *CLIF:? +use +`(?P<cpp_name>.+)` +as +(?P<py_name>[\w.]+)'
    f'({_PYOBJFROM_ONLY}|{_PYOBJAS_ONLY}|)')


def generate_from(ast: ast_pb2.AST,
                  include_paths: List[str]) -> Generator[str, None, None]:
  """Generates type casters based on Clif_PyObjFrom and Clif_PyObjAs.

  Args:
    ast: CLIF ast protobuf.
    include_paths: The directories that the code generator tries to find the
      header files.

  Yields:
    pybind11 type casters code.
  """
  includes = set(ast.pybind11_includes).union(set(ast.usertype_includes))

  for include in includes:
    # Not generating type casters for the builtin types.
    # Not scanning headers generated by pybind11 code generator because the
    # `// CLIF USE` in those headers do not have associated `Clif_PyObjFrom` or
    # `Clif_PyObjAs`.
    if (include.startswith('clif/python') or
        # Excluding absl::Status and absl::StatusOr
        include.startswith('util/task/python') or
        include.endswith('_pybind11_clif.h')):
      continue
    for root in include_paths:
      try:
        with open(os.path.join(root, include)) as include_file:
          lines = include_file.readlines()
          for line in lines:
            use = _CLIF_USE.match(line)
            if use:
              cpp_name = use.group('cpp_name')
              py_name = use.group('py_name')
              generate_load = _PYOBJFROM_ONLY not in use[0]
              generate_cast = _PYOBJAS_ONLY not in use[0]
              yield from _generate_type_caster(py_name, cpp_name,
                                               generate_load, generate_cast)
        break
      except IOError as e:
        # Failed to find the header file in one directory. Try other
        # directories.
        pass
      else:
        raise NameError('include "%s" not found' % include)


def _generate_type_caster(
    py_name: str, cpp_name: str, generate_load: bool,
    generate_cast: bool) -> Generator[str, None, None]:
  """Generates pybind11 type caster code."""
  yield 'namespace pybind11 {'
  yield 'namespace detail {'
  yield f'template <> struct type_caster<{cpp_name}> {{'
  yield ' public:'
  yield I + f'PYBIND11_TYPE_CASTER({cpp_name}, _("{py_name}"));'
  yield ''
  if generate_load:
    yield I + 'bool load(handle src, bool) {'
    yield I + I + 'using ::clif::Clif_PyObjAs;'
    yield I + I + 'return Clif_PyObjAs(src.ptr(), &value);'
    yield I + '}'
    yield ''
  if generate_cast:
    yield I + (f'static handle cast({cpp_name} src, return_value_policy, '
               'handle) {')
    yield I + I + 'using ::clif::Clif_PyObjFrom;'
    yield I + I + 'return Clif_PyObjFrom(src, {});'
    yield I + '}'
  yield '};'
  yield '}  // namespace detail'
  yield '}  // namespace pybind11'
  yield ''

