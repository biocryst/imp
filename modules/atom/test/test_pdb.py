from __future__ import print_function
import io
import IMP
import IMP.test
import IMP.atom


class Tests(IMP.test.TestCase):

    def _test_round_trip(self, name, selector):
        m = IMP.Model()
        p = IMP.atom.read_pdb(self.get_input_file_name(name),
                              m, selector)
        n1 = len(IMP.atom.get_by_type(p, IMP.atom.ATOM_TYPE))
        sout = io.BytesIO()
        IMP.atom.write_pdb(p, sout)
        sin = io.BytesIO(sout.getvalue())
        p2 = IMP.atom.read_pdb(sin, m, selector)
        n2 = len(IMP.atom.get_by_type(p2, IMP.atom.ATOM_TYPE))
        self.assertEqual(n1, n2)
        self.assertGreater(n1, 0)

    def test_bad_read(self):
        """Check that read_pdb behaves OK on invalid files"""
        m = IMP.Model()
        self.assertRaises(IMP.IOException,
                          IMP.atom.read_pdb, "notafile.pdb",
                          m)
        # we don't actually check if a file is a pdb or not
        # and can't conclude it is not due to not reading any atoms
        # as the selector may filter them all.
        self.assertRaises(IMP.ValueException,
                          IMP.atom.read_pdb,
                          self.open_input_file("notapdb.pdb"),
                          m)

    def test_cast_selectors(self):
        """Check cast of selectors"""
        self.check_get_from(IMP.atom.NonWaterPDBSelector())
        self.check_get_from(IMP.atom.NPDBSelector())

    def test_read(self):
        """Check reading a pdb with one protein"""
        m = IMP.Model()

        #! read PDB
        mp = IMP.atom.read_pdb(self.open_input_file("input.pdb"),
                               m, IMP.atom.NonWaterPDBSelector())
        self.assertEqual(len(m.get_particle_indexes()), 1132)
        # IMP.atom.show_molecular_hierarchy(mp)
        IMP.atom.show(mp)
        IMP.atom.add_bonds(mp)
        bds = IMP.atom.get_internal_bonds(mp)
        self.assertEqual(len(bds), 1020)
        IMP.atom.add_radii(mp)
        IMP.atom.show_molecular_hierarchy(mp)

        m2 = IMP.Model()
        mp = IMP.atom.read_pdb(self.open_input_file("input.pdb"),
                               m2, IMP.atom.CAlphaPDBSelector())
        self.assertEqual(len(m2.get_particle_indexes()), 260)
        ps = IMP.atom.get_by_type(mp, IMP.atom.ATOM_TYPE)
        self.assertEqual(len(ps), 129)
        IMP.atom.add_bonds(mp)
        bds = IMP.atom.get_internal_bonds(mp)
        self.assertEqual(len(bds), 0)

        # more selector testing
        mp = IMP.atom.read_pdb(self.open_input_file("input.pdb"),
                               m, IMP.atom.BackbonePDBSelector())
        ps = IMP.atom.get_by_type(mp, IMP.atom.ATOM_TYPE)
        self.assertEqual(len(ps), 516)

        mp = IMP.atom.read_pdb(self.open_input_file("input.pdb"),
                               m, IMP.atom.NPDBSelector())
        ps = IMP.atom.get_by_type(mp, IMP.atom.ATOM_TYPE)
        self.assertEqual(len(ps), 129)

        # one more test for DNA
        mp = IMP.atom.read_pdb(self.open_input_file("single_dna.pdb"),
                               m, IMP.atom.NonWaterPDBSelector())
        ps = IMP.atom.get_by_type(mp, IMP.atom.ATOM_TYPE)
        self.assertEqual(len(ps), 3011)

    def test_read_non_water(self):
        """Check that the default pdb reader skips waters"""
        IMP.set_log_level(IMP.VERBOSE)
        m = IMP.Model()
        mp = IMP.atom.read_pdb(self.open_input_file("protein_water.pdb"),
                               m)
        a = IMP.atom.get_leaves(mp)
        IMP.atom.write_pdb(mp, self.get_tmp_file_name("water_write.pdb"))
        self.assertEqual(len(a), 320)

    def test_read_non_hydrogen(self):
        """Check that the Hydrogen selector can identify all hydrogens"""
        IMP.set_log_level(IMP.VERBOSE)
        m = IMP.Model()
        mp = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"),
                               m, IMP.atom.HydrogenPDBSelector())
        a = IMP.atom.get_leaves(mp)
        self.assertEqual(len(a), 22)

    def test_atom_type(self):
        """Test AtomTypePDBSelector"""
        m = IMP.Model()
        mp = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"),
                               m, IMP.atom.AtomTypePDBSelector(["HA", "3HE"]))
        self.assertEqual(len(IMP.atom.get_leaves(mp)), 3)

    def test_residue_type(self):
        """Test ResidueTypePDBSelector"""
        m = IMP.Model()
        mp = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"),
                               m, IMP.atom.ResidueTypePDBSelector(["MET"]))
        self.assertEqual(len(IMP.atom.get_leaves(mp)), 22)

    def test_sel_logic(self):
        """Test boolean logic selectors"""
        m = IMP.Model()
        mp = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"),
                               m, IMP.atom.HydrogenPDBSelector())
        a = IMP.atom.get_leaves(mp)
        mpn = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"),
                                m, IMP.atom.NotPDBSelector(IMP.atom.HydrogenPDBSelector()))
        an = IMP.atom.get_leaves(mpn)
        for s in (IMP.atom.OrPDBSelector(IMP.atom.NotPDBSelector(IMP.atom.HydrogenPDBSelector()), IMP.atom.HydrogenPDBSelector()),
              ~IMP.atom.HydrogenPDBSelector() | IMP.atom.HydrogenPDBSelector()):
            mpb = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"), m, s)
            ab = IMP.atom.get_leaves(mpb)
            self.assertEqual(len(ab), len(an) + len(a))
        for s in (IMP.atom.AndPDBSelector(IMP.atom.HydrogenPDBSelector(),
                                          IMP.atom.ChainPDBSelector('L')),
                  IMP.atom.HydrogenPDBSelector()
                        & IMP.atom.ChainPDBSelector('L')):
            mpb = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"), m, s)
            ab = IMP.atom.get_leaves(mpb)
            self.assertEqual(len(ab), 9)
        for s in (IMP.atom.XorPDBSelector(IMP.atom.HydrogenPDBSelector(),
                                          IMP.atom.ChainPDBSelector('L')),
                  IMP.atom.HydrogenPDBSelector()
                        ^ IMP.atom.ChainPDBSelector('L')):
            mpb = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"), m, s)
            ab = IMP.atom.get_leaves(mpb)
            self.assertEqual(len(ab), 14)
        for s in (IMP.atom.AndPDBSelector(IMP.atom.HydrogenPDBSelector(),
                      IMP.atom.NotPDBSelector(IMP.atom.ChainPDBSelector('L'))),
                  IMP.atom.HydrogenPDBSelector()
                        - IMP.atom.ChainPDBSelector('L')):
            mpb = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"), m, s)
            ab = IMP.atom.get_leaves(mpb)
            self.assertEqual(len(ab), 13)

    def test_pyimpl(self):
        """Test PDBSelectors implemented in Python"""
        class my_selector(IMP.atom.PDBSelector):

            def __init__(self):
                IMP.atom.PDBSelector.__init__(self, "my selector")

            def get_is_selected(self, ln):
                return ln.startswith("ATOM")

        m = IMP.Model()
        mp = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"),
                               m, IMP.atom.ATOMPDBSelector())
        mp_py = IMP.atom.read_pdb(self.open_input_file("hydrogen.pdb"),
                                  m, my_selector())

        l = IMP.atom.get_leaves(mp)
        self.assertEqual(len(l), 25)
        l_py = IMP.atom.get_leaves(mp_py)
        self.assertEqual(len(l), len(l_py))

    def test_read_non_prob(self):
        """Check that problem lines are read properly"""
        IMP.set_log_level(IMP.VERBOSE)
        m = IMP.Model()
        mp = IMP.atom.read_pdb(self.open_input_file("problem_lines.pdb"), m)
        a = IMP.atom.get_leaves(mp)
        self.assertEqual(len(a), 1)

    def test_read_one_model(self):
        """Check that only the first model is read"""
        m = IMP.Model()
        h = IMP.atom.read_pdb(self.open_input_file("multimodel.pdb"), m,
                              IMP.atom.AllPDBSelector(), True)
        # print m.number
        ln = IMP.atom.get_leaves(h)
        print(len(ln))
        self.assertLess(len(ln), 1000)

    def test_one_atom(self):
        """Test reading a PDB containing a single atom"""
        m = IMP.Model()
        h = IMP.atom.read_pdb(self.open_input_file("single_atom.pdb"), m,
                              IMP.atom.AllPDBSelector(), True)
        # print m.number
        ln = IMP.atom.get_leaves(h)
        print(len(ln))
        self.assertLess(len(ln), 1000)

    def test_indexes(self):
        m = IMP.Model()
        h = IMP.atom.read_pdb(self.open_input_file("dna.pdb"), m)
        tn = self.get_tmp_file_name("out_dna.pdb")
        IMP.atom.write_pdb(h, tn)
        hp = IMP.atom.read_pdb(tn, m)
        lvs = IMP.atom.get_leaves(hp)
        self.assertEqual(IMP.atom.Atom(lvs[2]).get_input_index(), 3)

if __name__ == '__main__':
    IMP.test.main()
