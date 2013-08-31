/**
 *  \file IMP/isd/GaussianRestraint.h
 *  \brief A lognormal restraint that uses the ISPA model to model NOE-derived
 *  distance fit.
 *
 *  Copyright 2007-2013 IMP Inventors. All rights reserved.
 *
 */

#ifndef IMPISD_GAUSSIAN_RESTRAINT_H
#define IMPISD_GAUSSIAN_RESTRAINT_H

#include <IMP/restraint_macros.h>
#include <IMP/isd/isd_config.h>
#include <IMP/kernel/Particle.h>
#include <IMP/isd/ISDRestraint.h>

IMPISD_BEGIN_NAMESPACE

//! Normal probability distribution as a restraint
class IMPISDEXPORT GaussianRestraint : public ISDRestraint
{
private:
  base::Pointer<kernel::Particle> px_;
  double x_;
  base::Pointer<kernel::Particle> pmu_;
  double mu_;
  base::Pointer<kernel::Particle> psigma_;
  double sigma_;
  bool isx_, ismu_, issigma_; // true if it's a particle
  double chi_;

private:
  void set_chi(double chi) { chi_ = chi; }
  void check_particles();

public:
  //! Gaussian restraint
  /** The restraint is a 3-particle restraint, linking together the mean,
   * observed value and variance, which can all be either Nuisances or doubles.
   * If F is the identity function, this is a gaussian (e.g. harmonic)
   * restraint.
   */
  GaussianRestraint(kernel::Particle *x, kernel::Particle *mu, kernel::Particle *sigma);
  GaussianRestraint(double x, kernel::Particle *mu, kernel::Particle *sigma);
  GaussianRestraint(kernel::Particle *x, double mu, kernel::Particle *sigma);
  GaussianRestraint(kernel::Particle *x, kernel::Particle *mu, double sigma);
  GaussianRestraint(double x, double mu, kernel::Particle *sigma);
  GaussianRestraint(kernel::Particle *x, double mu, double sigma);
  GaussianRestraint(double x, kernel::Particle *mu, double sigma);

  /* call for probability */
  double get_probability() const
  {
    return exp(-unprotected_evaluate(nullptr));
  }

  double get_chi() const
  {return chi_; }


  virtual double
  unprotected_evaluate(IMP::kernel::DerivativeAccumulator *accum)
     const IMP_OVERRIDE;
  virtual IMP::kernel::ModelObjectsTemp do_get_inputs() const IMP_OVERRIDE;
  IMP_OBJECT_METHODS(GaussianRestraint);

};

IMPISD_END_NAMESPACE

#endif  /* IMPISD_GAUSSIAN_RESTRAINT_H */
