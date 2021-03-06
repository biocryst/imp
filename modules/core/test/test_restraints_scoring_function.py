import IMP
import IMP.test
import IMP.core


class Tests(IMP.test.TestCase):

    """Test RestraintSets"""

    def _make_stuff(self):
        m = IMP.Model()
        rs = IMP.RestraintSet(m, .5, "RS")
        r0 = IMP._ConstRestraint(m, [], 1)
        rs.add_restraint(r0)
        r1 = IMP._ConstRestraint(m, [], 1)
        rs.add_restraint(r1)
        r2 = IMP._ConstRestraint(m, [], 1)
        return (m, rs, r0, r1, r2)

    def test_weights2(self):
        """Test that sets can be weighted"""
        (m, rs, r0, r1, r2) = self._make_stuff()
        sf1 = IMP.core.RestraintsScoringFunction([rs, r2])
        self.assertEqual(sf1.evaluate(False), 2)
        rs.set_weight(1)
        self.assertEqual(sf1.evaluate(False), 3)

        sf = IMP.core.RestraintsScoringFunction([r0, r1, r2])
        self.assertEqual(sf.evaluate_if_good(False), 3)
        self.assertEqual(rs.evaluate(False), 2)

    def test_weights(self):
        """Test that restraints decompose ok"""
        m = IMP.Model()
        p = IMP.Particle(m)
        r = IMP._ConstRestraint(1, [p])
        rd = r.create_decomposition()
        self.assertEqual(r.evaluate(False), rd.evaluate(False))
        ra = IMP.get_restraints([r])
        rda = IMP.get_restraints([rd])
        sf = IMP.core.RestraintsScoringFunction(ra)
        sfda = IMP.core.RestraintsScoringFunction(rda)
        self.assertEqual(sf.evaluate(False), sfda.evaluate(False))

if __name__ == '__main__':
    IMP.test.main()
