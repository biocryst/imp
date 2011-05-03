/**
 *  \file isd/MarginalNOERestraint.h
 *  \brief A lognormal restraint that uses the ISPA model to model NOE-derived
 *  distance fit.
 *
 *  Copyright 2007-2010 IMP Inventors. All rights reserved.
 *
 */

#ifndef IMPISD_MARGINAL_NOE_RESTRAINT_H
#define IMPISD_MARGINAL_NOE_RESTRAINT_H

#include "isd_config.h"
#include <IMP/isd/ISDRestraint.h>
#include <IMP/PairContainer.h>

IMPISD_BEGIN_NAMESPACE

//! Apply an NOE distance restraint between two particles. Marginal of the NOE
//lognormal model. Since restraint is complicated, pass individual particles to
//add_contribution() command. Supports ambiguous NOEs and derivatives.
//
/** 
   \f[p(D|X,I) = b^{-\frac{N-1}{2}} \quad
    b = \sum_{i=1}^N \log^2\left(\frac{V_i^{exp}}{d_i^{-6}(X) v}\right) \quad
    v = \left(\prod_{i=1}^N \frac{V_i^{exp}}{d_i^{-6}}\right)^{1/N}
    \f]

    The source code is as follows:
    \include MarginalNOERestraint.h
    \include MarginalNOERestraint.cpp
*/
class IMPISDEXPORT MarginalNOERestraint : public ISDRestraint
{
    PairContainers contribs_;
    std::vector<double> volumes_;

public:
  //! Create the restraint.
  /** Restraints should store the particles they are to act on,
      preferably in a Singleton or PairContainer as appropriate.
   */
  MarginalNOERestraint(){};


  // add a contribution: simple case
  void add_contribution(Particle *p1, Particle *p2, double Iexp);

  //add a contribution: general case
  void add_contribution(PairContainer *pc, double Iexp);

  /* call for probability */
  double get_probability() const
  {
    return exp(-unprotected_evaluate(NULL));
  }


  /** This macro declares the basic needed methods: evaluate and show
   */
  IMP_RESTRAINT(MarginalNOERestraint);

};

IMPISD_END_NAMESPACE

#endif  /* IMPISD_MARGINAL_NOE_RESTRAINT_H */
