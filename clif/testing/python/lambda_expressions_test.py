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

from absl.testing import absltest

from clif.testing.python import lambda_expressions


class LambdaExpressionsTest(absltest.TestCase):

  def test_abstract_reference_parameter(self):
    obj = lambda_expressions.Derived(100)
    self.assertEqual(
        lambda_expressions.abstract_reference_param(obj), b'abstract_reference')

  def test_abstract_pointer_parameter(self):
    obj = lambda_expressions.Derived(10)
    self.assertEqual(
        lambda_expressions.abstract_pointer_param(obj), b'abstract_pointer')

  def test_nomove_reference_parameter(self):
    obj = lambda_expressions.NoCopyNoMove()
    self.assertEqual(lambda_expressions.nocopy_nomove_reference_param(obj),
                     b'nocopy_nomove_reference')

  def test_nomove_pointer_parameter(self):
    obj = lambda_expressions.NoCopyNoMove()
    self.assertEqual(lambda_expressions.nocopy_nomove_pointer_param(obj),
                     b'nocopy_nomove_pointer')

  def test_unique_pointer_parameter(self):
    obj = lambda_expressions.Derived(10)
    self.assertEqual(lambda_expressions.unique_pointer_param(obj),
                     b'unique_ptr')

  def test_ctor_unknown_default_parameter(self):
    obj = lambda_expressions.TestCtor()
    self.assertEqual(obj.value, 10)

  def test_extend_ctor_unknown_default_parameter(self):
    obj = lambda_expressions.TestExtendCtor(10)
    self.assertEqual(obj.value, 110)

  def test_no_default_ctor_return(self):
    obj = lambda_expressions.no_default_ctor_return(100)[0]
    self.assertEqual(obj.get(), 100)

  def test_multiple_returns_with_unique_ptr(self):
    obj = lambda_expressions.multiple_returns_with_unique_ptr()[0]
    self.assertEqual(obj.get(), 10)

  def test_multiple_returns_with_nocopy_object(self):
    obj = lambda_expressions.multiple_returns_with_nocopy_object()[0]
    self.assertEqual(obj.get(), '20')

  def test_ctor_takes_pyobject(self):
    obj = lambda_expressions.CtorTakesPyObj(1000)
    self.assertEqual(obj.value, 1000)
    obj = lambda_expressions.CtorTakesPyObj('123')
    self.assertEqual(obj.value, -1)

  def test_extended_ctor_takes_pyobject(self):
    obj = lambda_expressions.ExtendedCtorTakesPyObj(1001)
    self.assertEqual(obj.value, 1001)
    obj = lambda_expressions.ExtendedCtorTakesPyObj('123')
    self.assertEqual(obj.value, -1)

  def test_from_nocopy(self):
    nc = lambda_expressions.NoCopy('30')
    self.assertEqual(nc.get(), '30')
    obj = lambda_expressions.FromNoCopy.from_no_copy(nc)
    self.assertEqual(obj.get(), '30')

  def test_generate_operator_with_high_priority(self):
    v1 = lambda_expressions.Derived(10)
    v2 = lambda_expressions.Derived(20)
    self.assertEqual(v1, v1)
    self.assertNotEqual(v1, v2)


if __name__ == '__main__':
  absltest.main()