/**
 *  \file Restraint.cpp   \brief Abstract base class for all restraints.
 *
 *  Copyright 2007-2015 IMP Inventors. All rights reserved.
 *
 */

#include "IMP/kernel/container_base.h"
#include "IMP/kernel/internal/utility.h"
#include "IMP/kernel/Particle.h"
#include "IMP/kernel/Model.h"
#include "IMP/kernel/internal/graph_utility.h"
#include "IMP/kernel/dependency_graph.h"

IMPKERNEL_BEGIN_NAMESPACE

Container::Container(kernel::Model *m, std::string name)
    : ModelObject(m, name) {
  IMP_USAGE_CHECK(m, "Must pass model to container constructor.");
#if IMP_HAS_CHECKS >= IMP_INTERNAL
  writeable_ = true;
  readable_ = true;
#endif
}

void Container::validate_readable() const {
#if IMP_HAS_CHECKS >= IMP_INTERNAL
  if (!readable_) {
    base::handle_error("bad container read");
    throw internal::InputOutputException(get_name(),
                                         internal::InputOutputException::GET);
  }
#endif
}
void Container::validate_writable() const {
#if IMP_HAS_CHECKS >= IMP_INTERNAL
  if (!writeable_) {
    base::handle_error("bad container written");
    throw internal::InputOutputException(get_name(),
                                         internal::InputOutputException::GET);
  }
#endif
}
void Container::set_is_readable(bool tf) {
#if IMP_HAS_CHECKS >= IMP_INTERNAL
  readable_ = tf;
#else
  IMP_UNUSED(tf);
#endif
}
void Container::set_is_writable(bool tf) {
#if IMP_HAS_CHECKS >= IMP_INTERNAL
  writeable_ = tf;
#else
  IMP_UNUSED(tf);
#endif
}

IMPKERNEL_END_NAMESPACE
