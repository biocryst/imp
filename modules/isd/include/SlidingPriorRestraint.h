/**
 *  \file IMP/isd/SlidingPriorRestraint.h
 *  \brief A restraint on a scale parameter.
 *
 *  Copyright 2007-2013 IMP Inventors. All rights reserved.
 *
 */

#ifndef IMPISD_SLIDING_PRIOR_RESTRAINT_H
#define IMPISD_SLIDING_PRIOR_RESTRAINT_H

#include <IMP/isd/isd_config.h>
#include <IMP/SingletonScore.h>
#include <IMP/isd/ISDRestraint.h>
#include <IMP/restraint_macros.h>

IMPISD_BEGIN_NAMESPACE

//! Score a Scale particle with unnormalized probability.
/** \f[\frac{1}{\sigma_{q}} \exp\left(+\frac{(q-qmin)^2}{2 \sigma_q^2}\right)
    \f]
    where q is between qmin and qmax.
 */
class IMPISDEXPORT SlidingPriorRestraint : public ISDRestraint
{
  base::Pointer<kernel::Particle> p_;
  double qmin_, qmax_, sq_;

public:
  //! Create the restraint.
  SlidingPriorRestraint(kernel::Particle *p, double qmin, double qmax, double sq);

  /** This macro declares the basic needed methods: evaluate and show
   */
  virtual double
  unprotected_evaluate(IMP::kernel::DerivativeAccumulator *accum)
     const IMP_OVERRIDE;
  virtual IMP::kernel::ModelObjectsTemp do_get_inputs() const IMP_OVERRIDE;
  IMP_OBJECT_METHODS(SlidingPriorRestraint);

  //! Call for probability
  virtual double get_probability() const
  {
    return exp(-unprotected_evaluate(nullptr));
  }

};

IMPISD_END_NAMESPACE

#endif  /* IMPISD_SLIDING_PRIOR_RESTRAINT_H */
