/**
 *  \file AttributeTable.h    \brief Keys to cache lookup of attribute strings.
 *
 *  Copyright 2007-2011 IMP Inventors. All rights reserved.
 *
 */

#ifndef IMPKERNEL_ATTRIBUTE_TABLE_H
#define IMPKERNEL_ATTRIBUTE_TABLE_H

#include "../base_types.h"
#include "../utility.h"
#include <IMP/base/log.h>
#include "../Pointer.h"
#include <boost/dynamic_bitset.hpp>

#include <limits>

IMP_BEGIN_NAMESPACE

class Particle;

IMP_END_NAMESPACE


IMP_BEGIN_INTERNAL_NAMESPACE

template <class T, class K >
struct DefaultTraits
{
  typedef compatibility::checked_vector<T> Container;
  typedef T Value;
  typedef T PassValue;
  typedef K Key;
  static const T &max(const T &a, const T &b) {
    return std::max(a,b);
  }
  static const T &min(const T &a, const T &b) {
    return std::min(a,b);
  }
};

template <class T, class K >
struct ArrayTraits
{
  typedef IMP::compatibility::checked_vector<T> Value;
  typedef IMP::compatibility::checked_vector<Value> Container;
  typedef const Value& PassValue;
  typedef K Key;
  static Value get_invalid() {
    return Value();
  }
  static bool get_is_valid(const Value &v) {
    return !v.empty();
  }
  static const Value &max(const Value &a, const Value &) {
    return a;
  }
  static const Value &min(const Value &, const Value &b) {
    return b;
  }
};


struct FloatAttributeTableTraits: public DefaultTraits<double, FloatKey>
{
  static double get_invalid() {
    /* do not use NaN as sometimes GCC will optimize things incorrectly.*/
    /*if (std::numeric_limits<float>::has_quiet_NaN) {
      return std::numeric_limits<float>::quiet_NaN();
      } else*/ if (std::numeric_limits<double>::has_infinity) {
      return std::numeric_limits<double>::infinity();
    } else {
      return std::numeric_limits<double>::max();
    }
  }
  static bool get_is_valid(double f) {
    /*if (std::numeric_limits<float>::has_quiet_NaN) {
      return !is_nan(f);
      } else*/
    return f< std::numeric_limits<double>::max();
  }
};


struct ParticleAttributeTableTraits:
  public DefaultTraits<int, ParticleKey>
{
  static Value get_invalid() {
    return -1;
  }
  static bool get_is_valid(const Value& f) {
    return f >=0;
  }
};

struct ParticlesAttributeTableTraits:
  public ArrayTraits<int, ParticlesKey>
{
};

struct ObjectAttributeTableTraits
{
  typedef Object* Value;
  typedef Object* PassValue;
  typedef ObjectKey Key;
  typedef Objects Container;
  static Value get_invalid() {
    return nullptr;
  }
  static bool get_is_valid(const Value& f) {
    return f;
  }
  static Value min(Value a, Value b) {
    return std::min(a,b);
  }
  static Value max(Value a, Value b) {
    return std::max(a,b);
  }
};

struct ObjectsAttributeTableTraits
{
  typedef Objects Value;
  typedef const Objects& PassValue;
  typedef ObjectsKey Key;
  typedef compatibility::checked_vector<Objects> Container;
  static Value get_invalid() {
    return Value();
  }
  static bool get_is_valid(const Value& f) {
    return !f.empty();
  }
  static Value min(Value a, Value b) {
    IMP_UNUSED(b);
    return a;
  }
  static Value max(Value a, Value b) {
    IMP_UNUSED(a);
    return b;
  }
};


struct IntsAttributeTableTraits:
  ArrayTraits<int, IntsKey>
{
};

struct IntAttributeTableTraits: public DefaultTraits<Int, IntKey>
{
  static Int get_invalid() {
    return std::numeric_limits<Int>::max();
  }
  static bool get_is_valid(Int f) {
    return f!= get_invalid();
  }
};

struct BoolAttributeTableTraits: public DefaultTraits<bool, FloatKey>
{
  typedef boost::dynamic_bitset<> Container;
  static bool get_invalid() {
    return false;
  }
  static bool get_is_valid(bool f) {
    return f;
  }
};

struct StringAttributeTableTraits: public DefaultTraits<String, StringKey>
{
  static Value get_invalid() {
    return "This is an invalid string in IMP";
  }
  static bool get_is_valid(String f) {
    return f!= get_invalid();
  }
};



// The traits for the particle class are declared in the Particle.h

/** \internal
    If memory becomes a problem then either use a char table to look up
    actual entries or use perfect hashing.
    http://burtleburtle.net/bob/hash/perfect.html

    Actuall Cuckoo hashing is probably a better bet as that gets
    high occupancy without large tables for the hash function.

    \note This version of the table uses certain values of the data
    to singal that the entry is invalid. Setting an entry to these
    values is a checked error. The values are specified by the
    Traits::invalid entry.
 */


namespace {
  static const FloatKey xyzr_keys[]={FloatKey(0U), FloatKey(1U),
                                     FloatKey(2U), FloatKey(3U)};

#ifndef __clang__
  // just to disable a warning
  inline int use_xyz_to_disable_warning() {
    if (xyzr_keys[0] != FloatKey(0U)) {
      return 1;
    } else return 0;
  }
#endif
}

IMP_END_INTERNAL_NAMESPACE

#endif  /* IMPKERNEL_ATTRIBUTE_TABLE_H */
