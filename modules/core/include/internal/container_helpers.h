/**
 *  \file internal/particle_helpers.h
 *  \brief A container for Singletons.
 *
 *  This file is generated by a script (core/tools/make-container).
 *  Do not edit directly.
 *
 *  Copyright 2007-2013 IMP Inventors. All rights reserved.
 */

#ifndef IMPCORE_INTERNAL_CONTAINER_HELPERS_H
#define IMPCORE_INTERNAL_CONTAINER_HELPERS_H

#include <IMP/core/core_config.h>
#include "../Typed.h"
#include <algorithm>
#include <IMP/particle_index.h>

IMPCORE_BEGIN_INTERNAL_NAMESPACE

inline int get_ordered_type_hash(const ParticleTypes &rets) {
  int max = ParticleType::get_number_unique();
  int pow = 1;
  int ret = 0;
  for (unsigned int i = 0; i < rets.size(); ++i) {
    ret += pow * rets[i].get_index();
    pow *= max;
  }
  return ret;
}

inline int get_ordered_type_hash(Model *m, kernel::ParticleIndex pi) {
  Typed td(m, pi);
  return td.get_type().get_index();
}

template <unsigned int D>
inline int get_ordered_type_hash(Model *m,
                                 const base::Array<D, kernel::ParticleIndex> &pi) {
  ParticleTypes rets(D);
  for (unsigned int i = 0; i < D; ++i) {
    Typed td(m, pi[i]);
    rets[i] = td.get_type();
  }
  return get_ordered_type_hash(rets);
}

inline int get_all_same(Model *, kernel::ParticleIndex) { return true; }

template <unsigned int D>
inline int get_all_same(Model *, const base::Array<D, kernel::ParticleIndex> &pi) {
  for (unsigned int i = 1; i < D; ++i) {
    if (pi[i - 1] != pi[i]) return false;
  }
  return true;
}

inline int get_type_hash(Model *m, kernel::ParticleIndex pi) {
  return get_ordered_type_hash(m, pi);
}

template <unsigned int D>
inline int get_type_hash(Model *m, const base::Array<D, kernel::ParticleIndex> &pi) {
  int max = ParticleType::get_number_unique();
  Ints rets(D);
  for (unsigned int i = 0; i < D; ++i) {
    Typed td(m, pi[i]);
    rets[i] = td.get_type().get_index();
  }
  std::sort(rets.begin(), rets.end());
  int pow = 1;
  int ret = 0;
  for (unsigned int i = 0; i < D; ++i) {
    ret += pow * rets[i];
    pow *= max;
  }
  return ret;
}

IMPCORE_END_INTERNAL_NAMESPACE

#endif /* IMPCORE_INTERNAL_CONTAINER_HELPERS_H */
