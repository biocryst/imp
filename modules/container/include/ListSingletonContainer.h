/**
 *  \file ListSingletonContainer.h    \brief Store a list of ParticlesTemp
 *
 *  This file is generated by a script (core/tools/make-container).
 *  Do not edit directly.
 *
 *  Copyright 2007-2010 IMP Inventors. All rights reserved.
 */

#ifndef IMPCONTAINER_LIST_SINGLETON_CONTAINER_H
#define IMPCONTAINER_LIST_SINGLETON_CONTAINER_H

#include "container_config.h"
#include <IMP/core/internal/CoreListSingletonContainer.h>

IMPCONTAINER_BEGIN_NAMESPACE

//! Store a list of ParticlesTemp
/** \note The indexes can change when particles are inserted
    as the list is maintained in sorted order.
 */
class IMPCONTAINEREXPORT ListSingletonContainer:
#if defined(IMP_DOXYGEN) || defined(SWIG)
public SingletonContainer
#else
public core::internal::CoreListSingletonContainer
#endif
{
  typedef core::internal::CoreListSingletonContainer P;
  // for the change versions
  ListSingletonContainer();
public:
  //! construct and pass an initial set of Singletons
  ListSingletonContainer(const ParticlesTemp &ps,
                         std::string name= "ListSingletonContainer %1%");

  ListSingletonContainer(Model *m,
                         std::string name= "ListSingletonContainer %1%");
  ListSingletonContainer(Model *m, const char *name);

#if defined(IMP_DOXYGEN) || defined(SWIG)
 /** @name Methods to control the contained objects

     This container stores a list of Singleton objects. To manipulate
     the list use these methods.
  */
  /**@{*/
  void add_particle(Particle* vt);
  void add_particles(const ParticlesTemp &c);
  void set_particles(ParticlesTemp c);
  IMP_NO_DOXYGEN(void add_particles(const Particles &c) {
      add_particles(static_cast<const ParticlesTemp&>(c));
    })
  IMP_NO_DOXYGEN(void set_particles(const Particles &c) {
      set_particles(static_cast<ParticlesTemp>(c));
    })
  void clear_particles();
  /**@}*/
  IMP_NO_DOXYGEN(bool get_is_up_to_date() const);
  IMP_SINGLETON_CONTAINER(ListSingletonContainer);
#else
  static ListSingletonContainer *create_untracked_container() {
    ListSingletonContainer *lsc = new ListSingletonContainer();
    return lsc;
  }
  IMP_OBJECT(ListSingletonContainer);
#endif
};

IMP_OBJECTS(ListSingletonContainer,ListSingletonContainers);

IMPCONTAINER_END_NAMESPACE

#endif  /* IMPCONTAINER_LIST_SINGLETON_CONTAINER_H */
