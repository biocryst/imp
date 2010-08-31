/**
 *  \file atom/BrownianDynamics.h
 *  \brief Simple molecular dynamics optimizer.
 *
 *  Copyright 2007-2010 IMP Inventors. All rights reserved.
 *
 */

#ifndef IMPATOM_BROWNIAN_DYNAMICS_H
#define IMPATOM_BROWNIAN_DYNAMICS_H

#include "atom_config.h"
#include "Diffusion.h"
#include "SimulationParameters.h"

#include <IMP/Particle.h>
#include <IMP/Optimizer.h>
#include <IMP/internal/units.h>
#include <IMP/algebra/Vector3D.h>

IMPATOM_BEGIN_NAMESPACE

// for swig
class SimulationParameters;

//! Simple Brownian dynamics optimizer.
/** The particles to be optimized must have optimizable x,y,z attributes
    and a non-optimizable "Stokes radius"; this optimizer assumes
    the score to be energy in kcal/mol, the xyz coordinates to be in
    angstroms and the diffusion coefficent be in cm^2/s

    Particles without optimized x,y,z and nonoptimized D are skipped.

    Currently, rigid bodies are not supported. The necessary information
    can be found at \external{en.wikipedia.org/wiki/Rotational_diffusion,
    the wikipedia}.

    BrownianDynamics uses a SimulationParameters particle to store the
    parameters of the simulation. Such a particle must be passed on
    creation. The BrownianDynamics object will at least see updates
    to the SimulationParamters particle which occur before the
    call to BrownianDynamics::optimize() or BrownianDynamics::simulate(),
    changing the the parameters during optimization has undefined
    results.

    The optimizer can either automatically determine which particles
    to use from the model or be passed a SingletonContainer for the
    particles. If such a container is passed, particles added to it
    during optimization state updates are handled properly.

    \see Diffusion
  */
class IMPATOMEXPORT BrownianDynamics : public Optimizer
{
public:
  //! Create the optimizer
  /** If sc is not null, that container will be used to find particles
      to move, otherwise the model will be searched.*/
  BrownianDynamics(SimulationParameters si,
                   SingletonContainer *sc=NULL);

  //! Simulate until the given time in fs
  double simulate(float time_in_fs);


  //! Define the feature size of the system
  /** The time step will be scaled so that particles do not move further than
      this in a single step. This ensures that objects cannot pass through
      one another or miss important features of the force field. */
  void set_minimum_feature_size(double df) {
    IMP_USAGE_CHECK(df > 0, "The max change must be positive");
    feature_size_2_=unit::SquareAngstrom(square(df));
  }
#if !defined(SWIG) && !defined(IMP_DOXYGEN)
  void set_minimum_feature_size(unit::Angstrom f) {
    set_minimum_feature_size(unit::strip_units(f));
  }
#endif

 SimulationParameters get_simulation_parameters() const{
    return si_;
  }

  void set_adjust_step_size(bool tf);

  /** If the score exceeds this, an error handler is kicked in which
      attempts to relax the model before proceeding. A warning is
      printed.
  */
  void set_maximum_score(double s);

  SingletonContainer *get_diffusing_particles() const;

  IMP_OPTIMIZER(BrownianDynamics);
private:
  void copy_coordinates(SingletonContainer *sc,
                        std::vector<algebra::VectorD<3> > &v) const;
  void revert_coordinates(SingletonContainer *sc,
                          std::vector<algebra::VectorD<3> > &v);

  void take_step(SingletonContainer *sc, unit::Femtosecond dt);

  SingletonContainer* setup_particles() const;

  /* unit::KilocaloriePerAngstromPerMol
     get_force_scale_from_D(unit::SquareCentimeterPerSecond D) const;*/


  unit::SquareAngstrom feature_size_2_;
  RefCountingDecorator<SimulationParameters> si_;
  IMP::internal::OwnerPointer<SingletonContainer> sc_;
  unsigned int failed_steps_;
  unsigned int successful_steps_;
  bool dynamic_steps_;
  double maximum_score_;
};


IMPATOMEXPORT double get_maximum_time_step_estimate(BrownianDynamics *bd);

IMPATOM_END_NAMESPACE

#endif  /* IMPATOM_BROWNIAN_DYNAMICS_H */
