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

from clif.testing.python import alt_bytes


class AltBytesTest(absltest.TestCase):

  def testPassAltBytes(self):
    back_via_std_string = alt_bytes.PassAltBytes(b'A\x80c')
    self.assertEqual(back_via_std_string, b'PassAltBytes:A\x80c')

  def testReturnAltBytes(self):
    back_via_alt_bytes = alt_bytes.ReturnAltBytes(b'x\x80Z')
    self.assertEqual(back_via_alt_bytes, b'ReturnAltBytes:x\x80Z')


if __name__ == '__main__':
  absltest.main()
