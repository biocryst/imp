from SCons.Script import Glob, Dir, File, Builder, Action
import pyscanner
import os
import os.path


def _get_name(env):
    if env.has_key('IMP_APPLICATION'):
        return env['IMP_APPLICATION']
    else:
        return "IMP." + env['IMP_MODULE']

def _action_unit_test(target, source, env):
    #app = "cd %s; %s %s %s -v > /dev/null"
    fsource=[]
    for x in source[2:]:
        if str(x).endswith(".py"):
            fsource.append(x.abspath)
    app = "mkdir -p %s; cd %s; %s %s %s %s > /dev/null" \
          % (Dir("#/build/tmp").abspath, Dir("#/build/tmp").abspath, source[0].abspath, env['PYTHON'],
             source[1].abspath,
             " ".join(fsource))
    if env.Execute(app) == 0:
        file(str(target[0]), 'w').write('PASSED\n')
        print "%s %ss succeeded" % (_get_name(env), env['TEST_TYPE'])
    else:
        print "%s %ss FAILED" % (_get_name(env), env['TEST_TYPE'])
        return 1


def _print_unit_test(target, source, env):
    print "Running %s %ss" % (_get_name(env), env['TEST_TYPE'])

UnitTest = Builder(action=Action(_action_unit_test,
                                _print_unit_test),
                   source_scanner=pyscanner.PythonScanner)



def _action_cpp_test(target, source, env):
    #app = "cd %s; %s %s %s -v > /dev/null"
    out= open(target[0].abspath, "w")
    print >> out, """
import unittest
import IMP
import IMP.test
import sys
try:
    import subprocess
except ImportError:
    subprocess = None

class DirectoriesTests(IMP.test.TestCase):
"""
    for t in source:
        nm= os.path.split(str(t))[1].replace(".", "_")
        print >> out, """
    def test_%(name)s(self):
       \"\"\"Running C++ test %(name)s\"\"\"
       if subprocess is None:
           sys.stderr.write("test skipped: subprocess module unavailable: ")
           return
       # Note: Windows binaries look for needed DLLs in the current
       # directory. So we need to change into the directory where the DLLs have
       # been installed for the binary to load correctly.
       p = subprocess.Popen(["%(path)s"],
                            shell=False, cwd="%(libdir)s")
       self.assertEqual(p.wait(), 0)
""" %{'name':nm, 'path':t.abspath, 'libdir':env.Dir('#/build/lib').abspath}
    print >> out, """
if __name__ == '__main__':
    unittest.main()
"""


def _print_cpp_test(target, source, env):
    print "Generating cpp testing harness"

CPPTestHarness = Builder(action=Action(_action_cpp_test,
                                       _print_cpp_test))
