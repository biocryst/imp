/**
 *  \file internal/singleton_helpers.h
 *  \brief A container for particles.
 *
 *  This file is generated by a script (core/tools/make-container).
 *  Do not edit directly.
 *
 *  Copyright 2007-2010 IMP Inventors. All rights reserved.
 */

#ifndef IMPCORE_INTERNAL_SINGLETON_HELPERS_H
#define IMPCORE_INTERNAL_SINGLETON_HELPERS_H

#include "../core_config.h"
#include <IMP/SingletonContainer.h>
#include <IMP/SingletonModifier.h>
#include <IMP/internal/container_helpers.h>
#include <algorithm>

IMPCORE_BEGIN_INTERNAL_NAMESPACE

class IMPCOREEXPORT ListLikeSingletonContainer: public SingletonContainer {
private:
  void set_added_and_removed_containers(SingletonContainer *,
                                        SingletonContainer *){}
  ListLikeSingletonContainer *get_added() const {
    return dynamic_cast<ListLikeSingletonContainer*>
      (get_added_singletons_container());
  }
  ListLikeSingletonContainer *get_removed() const {
    return dynamic_cast<ListLikeSingletonContainer*>
      (get_removed_singletons_container());
  }
  Particles data_;
protected:
  ListLikeSingletonContainer(){}
  void update_list(ParticlesTemp &cur) {
    IMP_IF_CHECK(USAGE) {
      for (unsigned int i=0; i< cur.size(); ++i) {
        IMP_USAGE_CHECK(
         IMP::internal::is_valid(cur[i]),
         "Passed Particle cannot be NULL (or None)");
      }
    }
    std::sort(cur.begin(), cur.end());
    if (!get_is_added_or_removed_container()) {
      ParticlesTemp added, removed;
      std::set_difference(cur.begin(), cur.end(),
                          data_.begin(), data_.end(),
                          std::back_inserter(added));
      std::set_difference(data_.begin(), data_.end(),
                          cur.begin(), cur.end(),
                          std::back_inserter(removed));
      get_added()->data_=added;
      get_removed()->data_=removed;
    }
    swap(data_, cur);
  }
  void add_to_list(ParticlesTemp &cur) {
    std::sort(cur.begin(), cur.end());
    ParticlesTemp added;
    std::set_difference(cur.begin(), cur.end(),
                        data_.begin(), data_.end(),
                        std::back_inserter(added));
    unsigned int osz= data_.size();
    data_.insert(data_.end(), added.begin(), added.end());
    std::inplace_merge(data_.begin(), data_.begin()+osz, data_.end());
    if (!get_is_added_or_removed_container()) {
      ListLikeSingletonContainer* ac=get_added();
      ac->data_.insert(ac->data_.end(), added.begin(), added.end());
    }
  }
  void remove_from_list(ParticlesTemp &cur) {
    std::sort(cur.begin(), cur.end());
    ParticlesTemp newlist;
    std::set_difference(data_.begin(), data_.end(),
                        cur.begin(), cur.end(),
                        std::back_inserter(newlist));
    swap(data_, newlist);
    if (!get_is_added_or_removed_container()) {
      ListLikeSingletonContainer* ac=get_removed();
      ac->data_.insert(ac->data_.end(), cur.begin(), cur.end());
    }
  }
  void add_to_list(Particle* cur) {
    data_.insert(std::lower_bound(data_.begin(),
                                  data_.end(), cur), cur);
    if (!get_is_added_or_removed_container()) {
      ListLikeSingletonContainer* ac=get_added();
      ac->data_.push_back(cur);
    }
  }
  ListLikeSingletonContainer(Model *m, std::string name):
    SingletonContainer(m,name){
    SingletonContainer::
      set_added_and_removed_containers( new ListLikeSingletonContainer(),
                                        new ListLikeSingletonContainer());
  }
public:
  Particle* get_particle(unsigned int i) const;
  void apply(const SingletonModifier *sm);
  void apply(const SingletonModifier *sm,
             DerivativeAccumulator &da);
  double evaluate(const SingletonScore *s,
                  DerivativeAccumulator *da) const;
  double evaluate_subset(const SingletonScore *s,
                         DerivativeAccumulator *da) const;
  double evaluate_change(const SingletonScore *s,
                         DerivativeAccumulator *da) const;
  double evaluate_prechange(const SingletonScore *s,
                            DerivativeAccumulator *da) const;
  unsigned int get_number_of_particles() const;
  bool get_contains_particle(Particle* vt) const;
  typedef Particles::const_iterator ParticleIterator;
  ParticleIterator particles_begin() const {
    return data_.begin();
  }
  ParticleIterator particles_end() const {
    return data_.end();
  }
  ObjectsTemp get_input_objects() const;
  void do_after_evaluate() {
    get_added()->data_.clear();
    get_removed()->data_.clear();
  }
  void do_before_evaluate() {
    std::remove_if(data_.begin(), data_.end(),
         IMP::internal::IsInactive());
  }
  bool get_is_up_to_date() const {return true;}
  bool get_contained_particles_changed() const;
  ParticlesTemp get_contained_particles() const;
  bool get_provides_access() const {return true;}
  const ParticlesTemp& get_access() const {
    IMP_INTERNAL_CHECK(get_is_up_to_date(),
                       "Container is out of date");
    return data_;
  }
  IMP_OBJECT(ListLikeSingletonContainer);
};


IMPCORE_END_INTERNAL_NAMESPACE

#define IMP_LISTLIKE_SINGLETON_CONTAINER(Name)               \
  IMP_OBJECT(Name)


#endif  /* IMPCORE_INTERNAL_SINGLETON_HELPERS_H */
