/**
 *  \file ClosePairsPairScore.h
 *  \brief Apply a PairScore to close pairs.
 *
 *  Copyright 2007-8 Sali Lab. All rights reserved.
 */

#ifndef IMPCORE_CLOSE_PAIRS_PAIR_SCORE_H
#define IMPCORE_CLOSE_PAIRS_PAIR_SCORE_H

#include "config.h"

#include "XYZRDecorator.h"

#include <IMP/PairScore.h>
#include <IMP/UnaryFunction.h>
#include <IMP/Pointer.h>
#include <IMP/ParticleRefiner.h>

IMPCORE_BEGIN_NAMESPACE

//! Traverse the ParticleRefiner hierarchy to find all pairs which are close
/** The ParticleRefiner implicitly defines a tree rooted at each particle.
    This PairScore applies another PairScore to all pairs of leaves, one
    taken from each tree such that the leaves are closer than the threshold.
    \note All particles in the tree must be XYZRDecorator particles for the
    passed radius. In addition, the ball defined by a particle must contain
    the balls of all its leaves.
 */
class IMPCOREEXPORT ClosePairsPairScore : public PairScore
{
  Pointer<ParticleRefiner> r_;
  Pointer<PairScore> f_;
  Float th_;
  FloatKey rk_;
public:
  /** \param[in] r The ParticleRefiner to call on each particle
      \param[in] f The pair score to apply to the generated pairs
   */
  ClosePairsPairScore(ParticleRefiner *r, PairScore *f,
                      Float max_distance,
                      FloatKey rk= XYZRDecorator::get_default_radius_key());
  virtual ~ClosePairsPairScore(){}
  virtual Float evaluate(Particle *a, Particle *b,
                         DerivativeAccumulator *da) const;
  virtual void show(std::ostream &out=std::cout) const;
};

IMPCORE_END_NAMESPACE

#endif  /* IMPCORE_CLOSE_PAIRS_PAIR_SCORE_H */
