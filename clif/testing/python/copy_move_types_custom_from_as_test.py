# Copyright 2023 Google LLC
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

from absl.testing import absltest

from clif.testing.python import copy_move_types_custom_from_as as tm
from clif.testing.python import copy_move_types_library


class CopyMoveTypesCustomFromAsTestCase(absltest.TestCase):

  def testFromCRAsPPCopyMoveType(self):
    class_obj = copy_move_types_library.CopyMoveType()
    cfa_obj = tm.MakeFromCRAsPPCopyMoveType(class_obj)
    trace = tm.GetTraceFromCRAsPPCopyMoveType(cfa_obj)
    self.assertEqual(trace, "DefaultCtor_CpCtor_CpCtor")


if __name__ == "__main__":
  absltest.main()