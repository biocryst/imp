/**
 *  \file IMP/CLASSNAMEScore.h
 *  \brief Define CLASSNAMEScore.
 *
 *  BLURB
 *
 *  Copyright 2007-2012 IMP Inventors. All rights reserved.
 */

#ifndef IMPKERNEL_HEADERNAME_SCORE_H
#define IMPKERNEL_HEADERNAME_SCORE_H

#include "kernel_config.h"
#include "base_types.h"
#include "ParticleTuple.h"
#include "DerivativeAccumulator.h"
#include "internal/container_helpers.h"
#include "input_output_macros.h"

IMP_BEGIN_NAMESPACE

//! Abstract score function
/** CLASSNAMEScores will evaluate the score and derivatives
    for the passed particles. Use in conjunction with various
    restraints such as IMP::core::CLASSNAMEsRestraint or
    IMP::core::CLASSNAMERestraint.

    Implementers should check out IMP_HEADERNAME_SCORE().
*/
class IMPEXPORT CLASSNAMEScore : public base::Object
{
 public:
  typedef VARIABLETYPE Argument;
  typedef INDEXTYPE IndexArgument;
  typedef ARGUMENTTYPE PassArgument;
  typedef PASSINDEXTYPE PassIndexArgument;
  typedef CLASSNAMEModifier Modifier;
  CLASSNAMEScore(std::string name="CLASSNAMEScore %1%");
  //! Compute the score and the derivative if needed.
  IMP_DEPRECATED_WARN
      virtual double evaluate(ARGUMENTTYPE vt,
                          DerivativeAccumulator *da) const =0;

  //! Compute the score and the derivative if needed.
  virtual double evaluate_index(Model *m, PASSINDEXTYPE vt,
                                DerivativeAccumulator *da) const {
    return evaluate(internal::get_particle(m, vt), da);
  }

  /** Implementations
      for these are provided by the IMP_HEADERNAME_SCORE()
      macro.
  */
  virtual double evaluate_indexes(Model *m,
                                  const PLURALINDEXTYPE &o,
                                  DerivativeAccumulator *da,
                                  unsigned int lower_bound,
                                  unsigned int upper_bound) const {
    double ret=0;
    for (unsigned int i=lower_bound; i< upper_bound; ++i) {
      ret+= evaluate_index(m, o[i], da);
    }
    return ret;
  }


  //! Compute the score and the derivative if needed.
  virtual double evaluate_if_good_index(Model *m,
                                        PASSINDEXTYPE vt,
                                        DerivativeAccumulator *da,
                                        double max)
      const {
    IMP_UNUSED(max);
    return evaluate_index(m, vt, da);
  }

  /** Implementations
      for these are provided by the IMP_HEADERNAME_SCORE()
      macro.
  */
  virtual double evaluate_if_good_indexes(Model *m,
                                          const PLURALINDEXTYPE &o,
                                          DerivativeAccumulator *da,
                                          double max,
                                          unsigned int lower_bound,
                                          unsigned int upper_bound)
      const {
    double ret=0;
    for (unsigned int i=lower_bound; i< upper_bound; ++i) {
      double cur= evaluate_if_good_index(m, o[i], da, max-ret);
      max-=cur;
      ret+=cur;
      if (max<0) break;
    }
    return ret;
  }

  /** Decompose this pair score acting on the pair into a set of
      restraints. The scoring function and derivatives should
      be equal to the current score. The defualt implementation
      just returns this object bound to the pair.*/
  Restraints create_current_decomposition(Model *m,
                                          PASSINDEXTYPE vt) const;

  IMP_INPUTS_DECL(CLASSNAMEScore);

  IMP_REF_COUNTED_DESTRUCTOR(CLASSNAMEScore);
};

IMP_END_NAMESPACE

#endif  /* IMPKERNEL_HEADERNAME_SCORE_H */
