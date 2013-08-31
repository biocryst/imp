import IMP
import IMP.test
import IMP.core
import IMP.atom
import IMP.isd
import random

nkey = IMP.FloatKey("nuisance")
vnkey = IMP.FloatKey("vel")
xkey = IMP.FloatKey('x')
ykey = IMP.FloatKey('y')
zkey = IMP.FloatKey('z')
masskey = IMP.FloatKey('mass')
vxkey = IMP.FloatKey('vx')

# Conversion from derivatives (in kcal/mol/A) to acceleration (A/fs/fs)
kcal2mod = 4.1868e-4
# Mass of Carbon-12 (g/mol)
cmass = 12.011

class XTransRestraint(IMP.kernel.Restraint):
    """Attempt to move the whole system along the x axis"""
    def __init__(self, strength):
        IMP.kernel.Restraint.__init__(self, "XTransRestraint %1%")
        self.strength = strength

    def unprotected_evaluate(self, accum):
        e = 0.
        for p in self.get_model().get_particles():
            if IMP.isd.Nuisance.get_is_setup(p):
                e += p.get_value(nkey) * self.strength
            else:
                e += p.get_value(xkey) * self.strength
        if accum:
            for p in self.get_model().get_particles():
                if IMP.isd.Nuisance.get_is_setup(p):
                    p.add_to_derivative(nkey, self.strength, accum)
                else:
                    p.add_to_derivative(xkey, self.strength, accum)
                    p.add_to_derivative(ykey, 0.0, accum)
                    p.add_to_derivative(zkey, 0.0, accum)
        return e
    def get_version_info(self):
        return IMP.VersionInfo("","")
    def do_show(self, fh):
        fh.write("Test restraint")
    def do_get_inputs(self):
        return [x for x in self.get_model().get_particles()]

class WriteTrajState(IMP.OptimizerState):
    """Write system coordinates (trajectory) into a Python list"""
    def __init__(self, traj):
        IMP.OptimizerState.__init__(self)
        self.traj = traj
    def update(self):
        model = self.get_optimizer().get_model()
        step = []
        for p in model.get_particles():
            if IMP.isd.Nuisance.get_is_setup(p):
                step.append((p.get_value(nkey),p.get_value(vnkey)))
            else:
                step.append((p.get_value(xkey), p.get_value(ykey),
                           p.get_value(zkey), p.get_value(vxkey)))
        self.traj.append(step)

class Tests(IMP.test.TestCase):
    """Test molecular dynamics optimizer on nuisances"""

    def setUp(self):
        """Set up particles and optimizer"""
        IMP.test.TestCase.setUp(self)
        IMP.base.set_log_level(0)
        self.model = IMP.Model()
        self.particles = []
        self.particles.append(IMP.isd.Nuisance.setup_particle(
            IMP.kernel.Particle(self.model), -43.0))
        self.particles[-1].set_nuisance_is_optimized(True)
        self.particles[-1].add_attribute(masskey, cmass, False)
        self.md = IMP.isd.MolecularDynamics(self.model)

    def _check_trajectory(self, coor, traj, timestep, vxfunc):
        """Check generated trajectory against that predicted using vxfunc"""
        vx = 0.
        msg = "Predicted coordinate %.5f doesn't match generated %.5f, " + \
              "for step %d, coordinate %d[%d]"
        velmsg = "Predicted velocity %.5f doesn't match generated %.5f, " + \
                 "for step %d, particle %d"
        for (num, step) in enumerate(traj):
            newvx = vxfunc(vx)
            for n in range(len(coor)):
                self.assertAlmostEqual(vx, step[n][1], delta=1e-3,
                                       msg=velmsg % (vx, step[n][1],
                                                     num, n))
                for d in range(1):
                    self.assertAlmostEqual(coor[n][d], step[n][d], delta=1e-3,
                                           msg=msg % (coor[n][d], step[n][d],
                                                      num, n, d))
                coor[n][0] += (newvx+vx)/2.0 * timestep
            vx = newvx

    def _optimize_model(self, timestep):
        """Run a short MD optimization on the model."""
        start = [[p.get_value(nkey)] for p in self.model.get_particles()]
        # Add starting (step 0) position to the trajectory, with zero velocity
        traj = [[x+[0] for x in start]]
        state = WriteTrajState(traj)
        self.md.add_optimizer_state(state)
        self.md.set_maximum_time_step(timestep)
        self.md.optimize(50)
        return start, traj

    def test_nonrigid_translation(self):
        """Check that non-rigid MD translation on nuisances is Newtonian"""
        timestep = 4.0
        strength = 50.0
        r = XTransRestraint(strength)
        self.model.add_restraint(r)
        (start, traj) = self._optimize_model(timestep)
        delttm = -timestep * kcal2mod / cmass
        self._check_trajectory(start, traj, timestep,
                               lambda a: a + strength * delttm)

    def test_velocity_cap(self):
        """Check that velocity capping works on nuisances"""
        timestep = 4.0
        strength = 5000.0
        r = XTransRestraint(strength)
        self.model.add_restraint(r)
        self.md.set_velocity_cap(0.3)
        (start, traj) = self._optimize_model(timestep)
        # Strength is so high that velocity should max out at the cap
        for i in range(len(traj) - 1):
            oldx = traj[i][0][0]
            newx = traj[i+1][0][0]
            # Calculate velocity from change in position
            self.assertAlmostEqual((oldx-newx) / timestep, 0.3, delta=1e-5)

    def test_non_xyz(self):
        """Should skip nuisance particles without xyz attributes"""
        p = IMP.kernel.Particle(self.model)
        p.add_attribute(IMP.FloatKey("attr"), 0.0, True)
        self.md.optimize(100)

    def test_make_velocities(self):
        """Test that MD on nuisances generates particle velocities"""
        self.md.optimize(0)
        for p in self.model.get_particles():
            self.assertTrue(p.has_attribute(vnkey))

    def _check_temperature(self, desired, tolerance):
        """Check the temperature of the system"""
        ekinetic = self.md.get_kinetic_energy()
        tkinetic = self.md.get_kinetic_temperature(ekinetic)
        self.assertAlmostEqual(tkinetic, desired,
                     msg="Temperature %f does not match expected %f within %f" \
                         % (tkinetic, desired, tolerance),
                     delta=tolerance)

    def test_temperature(self):
        """Check temperature on nuisances"""
        # Averages for temperature only make sense if we have a comparatively
        # large number of particles:
        for i in range(500):
            self.particles.append(IMP.isd.Nuisance.setup_particle(
                IMP.kernel.Particle(self.model), random.uniform(-100,100)))
            self.particles[-1].set_nuisance_is_optimized(True)
            self.particles[-1].add_attribute(masskey, cmass, False)
        # Initial temperature should be zero:
        ekinetic = self.md.get_kinetic_energy()
        tkinetic = self.md.get_kinetic_temperature(ekinetic)
        self.assertEqual(ekinetic, 0.0)
        self.assertEqual(tkinetic, 0.0)
        # After assigning T=100K, kinetic temp should be 100K:
        self.md.assign_velocities(100.0)
        ekinetic = self.md.get_kinetic_energy()
        self.assertNotEqual(ekinetic, 0.0)
        self._check_temperature(100.0, 20.0)
        # Make sure that the random number generator is working properly;
        # we should get different particle velocities each time we assign
        # velocities
        velocity = self.particles[0].get_value(vnkey)
        self.md.assign_velocities(100.0)
        velocity2 = self.particles[0].get_value(vnkey)
        # Kinetic energy, however, should be almost identical
        ekinetic2 = self.md.get_kinetic_energy()
        self.assertAlmostEqual(ekinetic, ekinetic2, delta=1e-2)

    def test_get_optimizer_states(self):
        """Test get_optimizer_states() method on nuisances"""
        wrtraj = WriteTrajState([])
        scaler = IMP.atom.VelocityScalingOptimizerState(
                             self.particles, 298.0, 10)
        self.md.add_optimizer_state(wrtraj)
        self.md.add_optimizer_state(scaler)
        m = self.md.get_optimizer_states()
        self.assertEqual(len(m), 2)
        for a in m:
            self.assertIsInstance(a, IMP.OptimizerState)

if __name__ == '__main__':
    IMP.test.main()
