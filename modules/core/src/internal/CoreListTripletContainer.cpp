/**
 *  \file ListTripletContainer.cpp   \brief A list of ParticleTriplets.
 *
 *  This file is generated by a script (core/tools/make-container).
 *  Do not edit directly.
 *
 *  Copyright 2007-2010 IMP Inventors. All rights reserved.
 *
 */

#include "IMP/core/internal/CoreListTripletContainer.h"
#include "IMP/TripletModifier.h"
#include "IMP/TripletScore.h"
#include <IMP/core/internal/triplet_helpers.h>
#include <algorithm>


IMPCORE_BEGIN_INTERNAL_NAMESPACE

namespace {
  CoreListTripletContainer* get_list(TripletContainer *g) {
    return dynamic_cast<CoreListTripletContainer*>(g);
  }
}

IMP_ACTIVE_CONTAINER_DEF(CoreListTripletContainer);

CoreListTripletContainer
::CoreListTripletContainer():
  internal::ListLikeTripletContainer(){}


CoreListTripletContainer
::CoreListTripletContainer(Model *m, std::string name):
  internal::ListLikeTripletContainer(m, name){
  initialize_active_container(m);
}


CoreListTripletContainer
::CoreListTripletContainer(Model *m, const char *name):
  internal::ListLikeTripletContainer(m, name){
  initialize_active_container(m);
}


void CoreListTripletContainer::do_show(std::ostream &out) const {
  IMP_CHECK_OBJECT(this);
  out << get_number_of_particle_triplets()
      << " particle_triplets." << std::endl;
}



void CoreListTripletContainer::set_particle_triplets(ParticleTripletsTemp sc) {
  update_list(sc);
}


void CoreListTripletContainer::clear_particle_triplets() {
  ParticleTripletsTemp t;
  update_list(t);
}


void CoreListTripletContainer::add_particle_triplet(const ParticleTriplet& vt) {
  IMP_USAGE_CHECK(IMP::internal::is_valid(vt),
                  "Passed ParticleTriplet cannot be NULL (or None)");
  add_to_list(vt);
  IMP_USAGE_CHECK(!get_has_added_and_removed_containers()
                  || !get_removed_container()
                  ->get_contains(vt),
                  "You cannot remove and add the same item in one time step.");
}

void
CoreListTripletContainer::add_particle_triplets(const ParticleTripletsTemp &c) {
  if (c.empty()) return;
  ParticleTripletsTemp cp= c;
  add_to_list(cp);
  IMP_IF_CHECK(USAGE) {
    for (unsigned int i=0; i< c.size(); ++i) {
      IMP_USAGE_CHECK(IMP::internal::is_valid(c[i]),
                    "Passed ParticleTriplet cannot be NULL (or None)");
      IMP_USAGE_CHECK(!get_has_added_and_removed_containers()
                      || !get_removed_container()
                      ->get_contains(c[i]),
            "You cannot remove and add the same item in one time step.");

    }
  }
}

void CoreListTripletContainer
::remove_particle_triplets(const ParticleTripletsTemp &c) {
  if (c.empty()) return;
  ParticleTripletsTemp cp= c;
  remove_from_list(cp);
  IMP_IF_CHECK(USAGE) {
    for (unsigned int i=0; i< c.size(); ++i) {
      IMP_USAGE_CHECK(IMP::internal::is_valid(c[i]),
                    "Passed ParticleTriplet cannot be NULL (or None)");
    }
  }
}


void CoreListTripletContainer::do_before_evaluate() {
  internal::ListLikeTripletContainer::do_before_evaluate();
}

void CoreListTripletContainer::do_after_evaluate() {
  internal::ListLikeTripletContainer::do_after_evaluate();
}

ParticlesTemp CoreListTripletContainer::get_state_input_particles() const {
  return ParticlesTemp();
}

ContainersTemp CoreListTripletContainer::get_state_input_containers() const {
  return ContainersTemp();
}

bool CoreListTripletContainer::get_contained_particles_changed() const {
  return !get_added()->get_access().empty()
    || !get_removed()->get_access().empty();
}
ParticlesTemp CoreListTripletContainer::get_contained_particles() const {
  return IMP::internal::flatten(get_access());
}


IMPCORE_END_INTERNAL_NAMESPACE
