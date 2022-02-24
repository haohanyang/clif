/*
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef THIRD_PARTY_CLIF_TESTING_PYTHON_TYPE_CASTER_CLIF_AUX_H_
#define THIRD_PARTY_CLIF_TESTING_PYTHON_TYPE_CASTER_CLIF_AUX_H_

#include <memory>

#include <Python.h>

#include "clif/testing/type_caster.h"
#include "clif/testing/python/lambda_expressions_clif.h"


namespace clif_testing {

inline int get_refcount_from_raw_ptr() {
  auto arg = Arg();
  PyObject* obj = Clif_PyObjFrom(&arg, {});
  int result = static_cast<int>(Py_REFCNT(obj));
  Py_XDECREF(obj);
  return result;
}

inline int get_refcount_from_unique_ptr() {
  auto arg = std::unique_ptr<Arg>(new Arg());
  PyObject* obj = Clif_PyObjFrom(std::move(arg), {});
  int result = static_cast<int>(Py_REFCNT(obj));
  Py_XDECREF(obj);
  return result;
}

inline int get_refcount_from_rvalue() {
  auto arg = Arg();
  PyObject* obj = Clif_PyObjFrom(std::move(arg), {});
  int result = static_cast<int>(Py_REFCNT(obj));
  Py_XDECREF(obj);
  return result;
}

inline int get_refcount_from_const_ref() {
  auto arg = Arg();
  const Arg& arg_ref = arg;
  PyObject* obj = Clif_PyObjFrom(arg_ref, {});
  int result = static_cast<int>(Py_REFCNT(obj));
  Py_XDECREF(obj);
  return result;
}

inline int get_refcount_from_const_ptr() {
  auto arg = Arg();
  const Arg* arg_ptr = &arg;
  PyObject* obj = Clif_PyObjFrom(arg_ptr, {});
  int result = static_cast<int>(Py_REFCNT(obj));
  Py_XDECREF(obj);
  return result;
}

}  // namespace clif_testing

#endif  // THIRD_PARTY_CLIF_TESTING_PYTHON_TYPE_CASTER_CLIF_AUX_H_