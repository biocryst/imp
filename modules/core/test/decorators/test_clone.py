import unittest
import IMP
import IMP.test
import IMP.core
import IMP.atom
import IMP.helper

class DecoratorTests(IMP.test.TestCase):
    def test_bonded(self):
        """Check clone MHD """
        m = IMP.Model()
        mh= IMP.atom.read_pdb(self.get_input_file_name("input.pdb"),
                              m)
        IMP.atom.show_molecular_hierarchy(mh)
        mhc= IMP.atom.clone(mh)
        bds=IMP.atom.get_internal_bonds(mh)
        print bds
        print IMP.atom.Bonds()
        nb= bds.size()
        nnb= IMP.atom.get_internal_bonds(mhc).size()
        self.assertEqual(nb, nnb)
        IMP.atom.show_molecular_hierarchy(mhc)


if __name__ == '__main__':
    unittest.main()
