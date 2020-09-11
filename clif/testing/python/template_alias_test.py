# Copyright 2017 Google Inc.
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

"""Tests for clif.testing.python.template_alias."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unittest
from clif.testing.python import template_alias


class TemplateAliasTest(unittest.TestCase):

  def testTemplateAlias(self):
    # Calling the following functions should not blow up.
    template_alias.func_default_vector_input([])
    output = template_alias.func_default_vector_output()
    self.assertEqual(len(output), 1)
    self.assertEqual(output[0], 123)
    return_list = template_alias.func_default_vector_return()
    self.assertEqual(len(return_list), 1)
    self.assertEqual(return_list[0], 100)
    template_alias.func_clif_vector([1])


if __name__ == '__main__':
  unittest.main()
