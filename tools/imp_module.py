"""Tools and Builders for IMP modules. See `IMPModule` for more information."""

import os.path
import pyscanner

from SCons.Script import Builder, File, Action

def action_config(target, source, env):
    """The IMPModuleConfig Builder generates a configuration header file
       used to mark classes and functions for export and to define namespaces,
       and a corresponding SWIG interface, e.g.
       env.IMPModuleConfig(('config.h', 'foo_config.i'), env.Value('foo'))
       generates a configuration header and interface for the 'foo' module."""
    name = source[0].get_contents()
    h = file(target[0].abspath, 'w')
    i = file(target[1].abspath, 'w')
    vars = {'name':name, 'NAME':name.upper(),
            'filename':os.path.basename(target[0].abspath),
            'namespace':'IMP::' + name, 'NAMESPACE':'IMP' + name.upper()}
    print >> h, """/*
 * \\file %(filename)s
 * \\brief Provide macros to mark functions and classes as exported
 *        from a DLL/.so, and to set up namespaces
 *
 * When building the module, IMP%(NAME)s_EXPORTS should be defined, and when
 * using the module externally, it should not be. Classes and functions
 * defined in the module's headers should then be marked with
 * IMP%(NAME)sEXPORT if they are intended to be part of the API, or with
 * IMP%(NAME)sLOCAL if they are not (the latter is the default).
 *
 * The Windows build environment requires applications to mark exports in
 * this way; we use the same markings to set the visibility of ELF symbols
 * if we have compiler support.
 *
 * All code in this module should live in the %(namespace)s namespace.
 * This is simply achieved by wrapping things with the
 * %(NAMESPACE)s_BEGIN_NAMESPACE and %(NAMESPACE)s_END_NAMESPACE macros.
 * There are similar macros for module code that is designed to be for
 * internal use only.
 *
 * This header is auto-generated by tools/imp-module.py; it should not be
 * edited manually.
 *
 * Copyright 2007-9 Sali Lab. All rights reserved.
 *
 */

#ifndef IMP%(NAME)s_CONFIG_H
#define IMP%(NAME)s_CONFIG_H

#ifdef _MSC_VER
#ifdef IMP%(NAME)s_EXPORTS
#define IMP%(NAME)sEXPORT __declspec(dllexport)
#else
#define IMP%(NAME)sEXPORT __declspec(dllimport)
#endif
#define IMP%(NAME)sLOCAL
#else
#ifdef GCC_VISIBILITY
#define IMP%(NAME)sEXPORT __attribute__ ((visibility("default")))
#define IMP%(NAME)sLOCAL __attribute__ ((visibility("hidden")))
#else
#define IMP%(NAME)sEXPORT
#define IMP%(NAME)sLOCAL
#endif
#endif
""" % vars

    print >> i, """/* Ignore shared object exports macros */
#define IMP%(NAME)sEXPORT
#define IMP%(NAME)sLOCAL
""" % vars

    for out in (i, h):
        print >> out, """#define %(NAMESPACE)s_BEGIN_NAMESPACE \\
namespace IMP \\
{ \\
\\
namespace %(name)s \\
{

#define %(NAMESPACE)s_END_NAMESPACE \\
} /* namespace %(name)s */ \\
\\
} /* namespace IMP */

#define %(NAMESPACE)s_BEGIN_INTERNAL_NAMESPACE \\
%(NAMESPACE)s_BEGIN_NAMESPACE \\
\\
namespace internal \\
{

#define %(NAMESPACE)s_END_INTERNAL_NAMESPACE \\
} /* namespace internal */ \\
\\
%(NAMESPACE)s_END_NAMESPACE""" % vars

    print >> h, """
#endif  /* IMP%(NAME)s_CONFIG_H */""" % vars


def action_version_info(target, source, env):
    """The IMPModuleVersionInfo Builder generates a source file and header to
       return version information, e.g.
       env.IMPModuleVersionInfo(('src/internal/version_info.cpp',
                                 'include/internal/version_info.h'),
                                (env.Value('foo'), env.Value('Me'),
                                 env.Value('1.0')))
       generates version information for the 'foo' module."""
    module = env['IMP_MODULE']
    author = env['IMP_MODULE_AUTHOR']#source[0].get_contents()
    version = env['IMP_MODULE_VERSION']#source[1].get_contents()
    cpp = file(target[0].abspath, 'w')
    h = file(target[1].abspath, 'w')

    for (f, ext) in ((cpp, 'cpp'), (h, 'h')):
        print >> f, """/**
 *  \\file %(module)s/internal/version_info.%(ext)s
 *  \\brief %(module)s module version information.
 *
 *  Copyright 2007-9 Sali Lab. All rights reserved.
 *
 */
""" % {'module':module, 'ext':ext}

    print >> h, """#ifndef IMP%(MODULE)s_INTERNAL_VERSION_INFO_H
#define IMP%(MODULE)s_INTERNAL_VERSION_INFO_H

#include "../config.h"

#include <IMP/VersionInfo.h>
""" % {'module':module, 'MODULE':module.upper()}

    print >> cpp, '#include <IMP/%s/internal/version_info.h>\n' \
                  % (module)

    for f in (h, cpp):
        print >> f, "IMP%s_BEGIN_INTERNAL_NAMESPACE\n" % module.upper()

    print >> h, """//! Version and authorship of the %(module)s module.
extern IMP%(MODULE)sEXPORT VersionInfo version_info;""" \
        % {'module':module, 'MODULE':module.upper()}

    print >> cpp, 'VersionInfo version_info("%s", "%s");' \
              % (author, version)

    for f in (h, cpp):
        print >> f, "\nIMP%s_END_INTERNAL_NAMESPACE" % module.upper()

    print >> h, "\n#endif  /* IMP%s_INTERNAL_VERSION_INFO_H */" % module.upper()

def action_link_test(target, source, env):
    """The IMPModuleLinkTesto Builder generates a source file. By linking in two
    of these, any functions which are defined in headers but not declared inline are detected"""
    module = source[0].get_contents()
    cpp = file(target[0].abspath, 'w')

    print >> cpp, """/**
 *  \\file %s/internal/%s
 *  \\brief Test linking for non-inlined functions.
 *
 *  This file is auto-generated, do not edit.
 *
 *  Copyright 2007-9 Sali Lab. All rights reserved.
 *
 */
""" % (module, os.path.split(target[0].abspath)[1])

    print >> cpp, """
#ifndef NDEBUG
#include "IMP/%s.h"
#endif""" % (module)

def _add_all_alias(aliases, env, name):
    """Add an 'all' alias `name` to the list of aliases, but only if the
       environment has been validated (i.e. this module is OK to build)."""
    if env['VALIDATED'] is None:
        print "Module environment not correctly set up - you must call\n" + \
              "either env.validate() or env.invalidate() in the " + \
              "module SConscript"
        env.Exit(1)
    if env['VALIDATED']:
        aliases.append(name)

def _get_module_install_aliases(env):
    """Get a list of all 'install' aliases for this module"""
    aliases = ['%s-install' % env['IMP_MODULE'], 'modules-install']
    _add_all_alias(aliases, env, 'install')
    return aliases

def _get_module_test_aliases(env):
    """Get a list of all 'test' aliases for this module"""
    aliases = ['%s-test' % env['IMP_MODULE'], 'modules-test']
    _add_all_alias(aliases, env, 'test')
    return aliases

def _add_module_default_alias(env, targets):
    """Add the default alias for this module, to build the given targets."""
    if env['VALIDATED']:
        env.Default(targets)


def IMPSharedLibrary(env, files, install=True):
    """Build, and optionally also install, an IMP module's C++
       shared library. This is only available from within an environment
       created by `IMPSharedLibraryEnvironment`."""
    module = env['IMP_MODULE']
    lib = env.SharedLibrary('#/build/lib/imp_%s' % module,
                            list(files) + [env['VER_CPP'], \
                                               env['LINK_0_CPP'],\
                                               env['LINK_1_CPP']])
    if env['PLATFORM'] == 'darwin':
        env.AddPostAction (lib, "install_name_tool -id %s %s" \
                               % (lib[0].abspath, lib[0].path))
        libdir= os.path.split(lib[0].abspath)[0]
    if install:
        libinst = env.Install(env['libdir'], lib)
        if env['PLATFORM'] == 'darwin':
            env.AddPostAction (libinst, "install_name_tool -id %s %s" \
                                   % (libinst[0].abspath, libinst[0].path))
            instlibdir= os.path.split(libinst[0].abspath)[0]
            env.AddPostAction (libinst, "install_name_tool -change %s/libimp.dylib %s/libimp.dylib %s" \
                                   % (libdir, instlibdir, libinst[0].path))
            env.AddPostAction (libinst, "install_name_tool -change %s/libimp_core.dylib %s/libimp_core.dylib %s" \
                                   % (libdir, instlibdir, libinst[0].path))
        for alias in _get_module_install_aliases(env):
            env.Alias(alias, [libinst])
        return lib, libinst
    else:
        return lib

def IMPSharedLibraryEnvironment(env):
    """Create a customized environment suitable for building IMP module C++
       shared libraries. Use the resulting object's `IMPSharedLibrary` pseudo
       builder to actually build the shared library."""
    from tools import get_sharedlib_environment
    module = env['IMP_MODULE']
    env = get_sharedlib_environment(env, 'IMP%s_EXPORTS' % module.upper(),
                                    cplusplus=True)
    env.AddMethod(IMPSharedLibrary)
    return env

def IMPHeaders(env, files):
    """Install the given header files, plus any auto-generated files for this
       IMP module."""
    from tools.hierarchy import InstallHierarchy
    includedir = os.path.join(env['includedir'], 'IMP')
    inst = InstallHierarchy(env, includedir, env['IMP_MODULE'],
                            env['IMP_MODULE_DESCRIPTION'],
                            list(files) + [env['CONFIG_H'], env['VER_H']])
    for alias in _get_module_install_aliases(env):
        env.Alias(alias, inst)
    return inst

def IMPPython(env, files):
    """Install the given Python files for this IMP module."""
    from tools.hierarchy import InstallPythonHierarchy
    pydir = os.path.join(env['pythondir'], 'IMP')
    inst, lib = InstallPythonHierarchy(env, pydir, env['IMP_MODULE'], files)
    for alias in _get_module_install_aliases(env):
        env.Alias(alias, inst)
    if env.get('python', True):
        _add_module_default_alias(env, lib)
    return lib

def IMPPythonExtension(env, swig_interface):
    """Build and install an IMP module's Python extension and the associated
       wrapper file from a SWIG interface file. This is only available from
       within an environment created by `IMPPythonExtensionEnvironment`."""
    module = env['IMP_MODULE']
    swigcom = env['SWIGCOM']
    if isinstance(swigcom, list) and isinstance(swigcom[0], str):
        repl = '$SWIG -interface _IMP_%s ' % module
        swigcom[0] = swigcom[0].replace('$SWIG ', repl)
    pyext = env.LoadableModule('#/build/lib/_IMP_%s' % module, swig_interface,
                               SWIGCOM=swigcom)
    # Place the generated Python wrapper in lib directory:
    gen_pymod = File('IMP.%s.py' % module)
    pymod = env.LinkInstallAs('#/build/lib/IMP/%s/__init__.py' % module,
                              gen_pymod)
    # Install the Python extension and module:
    libinst = env.Install(env['pyextdir'], pyext)
    if env['PLATFORM'] == 'darwin':
        libdir= os.path.split(pyext[0].abspath)[0]
        env.AddPostAction (libinst, "install_name_tool -change %s/libimp_%s.dylib %s/libimp_%s.dylib %s" \
                                   % (libdir, module,
                                      env['libdir'], module, libinst[0].path))
    pyinst = env.Install(os.path.join(env['pythondir'], 'IMP', module), pymod)
    for alias in _get_module_install_aliases(env):
        env.Alias(alias, [libinst, pyinst])
    if env.get('python', True):
        _add_module_default_alias(env, [pyext, pymod])
    return pyext, pymod

def IMPPythonExtensionEnvironment(env):
    """Create a customized environment suitable for building IMP module Python
       extensions. Use the resulting object's `IMPPythonExtension` pseudo
       builder to actually build the extension."""
    from tools import get_pyext_environment
    module = env['IMP_MODULE']
    env = get_pyext_environment(env, module.upper(), cplusplus=True)
    env.Append(LIBS=['imp_%s' % module])
    env['SWIGPATH'] = [env['CPPPATH'], '#']
    env.Append(SWIGFLAGS='-python -c++ -naturalvar')
    env.AddMethod(IMPPythonExtension)
    return env

def _action_unit_test(target, source, env):
    scripts = [File('#/bin/imppy.sh')]
    if env['TEST_ENVSCRIPT']:
        scripts.append(File(env['TEST_ENVSCRIPT']))
    #app = "cd %s; %s %s %s -v > /dev/null" \
    app = "%s %s %s %s -v > /dev/null" \
          % (#os.path.split(target[0].path)[0],
             " ".join([x.abspath for x in scripts]), env['PYTHON'], source[0].abspath,
             os.path.split(target[0].path)[0])
    if env.Execute(app) == 0:
        file(str(target[0]), 'w').write('PASSED\n')
    else:
        print "unit tests FAILED"
        return 1

def _print_unit_test(target, source, env):
    return "IMPModuleTest('%s')" % source[0]

def _emit_unit_test(target, source, env):
    # Add all test_*.py scripts to sources
    for dirpath, dirnames, filenames in os.walk('.'):
        for f in filenames:
            if f.startswith('test_') and f.endswith('.py'):
                source.append(os.path.join(dirpath, f))
    # Add environment scripts to sources
    source.append('#/bin/imppy.sh')
    if env['TEST_ENVSCRIPT']:
        source.append(env['TEST_ENVSCRIPT'])
    return target, source

def IMPModuleTest(env, target, source, **keys):
    """Pseudo-builder to run tests for an IMP module. The single target is
       generally a simple output file, e.g. 'test.passed', while the single
       source is a Python script to run (usually run-all-tests.py).
       Right now, the assumption is made that run-all-tests.py executes
       all files called test_*.py in the current directory and subdirectories.
       If the TEST_ENVSCRIPT construction variable is set, it is a shell
       script to run to set up the environment to run the test script.
       A convenience alias for the tests is added, and they are always run."""
    test = env._IMPModuleTest(target, source, **keys)
    for alias in _get_module_test_aliases(env):
        env.Alias(alias, test)
    env.AlwaysBuild(target)
    return test

def invalidate(env, fail_action):
    """'Break' an environment, so that any builds with it use the fail_action
       function (which should be an Action which terminates the build)"""
    for var in ('SHLINKCOM', 'CCCOM', 'CXXCOM', 'SHCCCOM', 'SHCXXCOM',
                'SWIGCOM'):
        env[var] = fail_action
    env.Append(BUILDERS={'_IMPModuleTest': Builder(action=fail_action)})
    env['VALIDATED'] = False

def validate(env):
    """Confirm that a module's environment is OK for builds."""
    module = env['IMP_MODULE']
    env['VALIDATED'] = True

def IMPModuleAbout(env, author, version, description):
    env['IMP_MODULE_DESCRIPTION'] = description
    env['IMP_MODULE_VERSION'] = version
    env['IMP_MODULE_AUTHOR'] = author

def IMPModule(env, module, cpp=True):
    """Set up an IMP module. The module's SConscript gets its own
       customized environment ('env') in which the following pseudo-builders
       or methods are available: IMPPython, IMPModuleTest, validate
       and invalidate. If `cpp` is True, necessary C++ headers are also
       automatically generated, and these additional methods are available:
       IMPSharedLibraryEnvironment, IMPPythonExtensionEnvironment, IMPHeaders.
       Either validate or invalidate must be called in the module's top-level
       SConscript before setting up any builders, to indicate whether the
       module's necessary dependencies have been met.
    """
    env['IMP_MODULES_ALL'].append(module)
    env = env.Clone()
    config = Builder(action=action_config)
    version_info = Builder(action=action_version_info)
    link_test = Builder(action=action_link_test)
    env.Append(BUILDERS = {'IMPModuleConfig': config,
                           'IMPModuleVersionInfo': version_info,
                           'IMPModuleLinkTest': link_test})

    env['IMP_MODULE'] = module
    env['IMP_MODULE_DESCRIPTION'] = "An IMP Module"
    env['IMP_MODULE_VERSION'] = "SVN"
    env['IMP_MODULE_AUTHOR'] = "A. Biologist"
    env.Prepend(CPPPATH=['#/build/include'])
    env.Prepend(LIBPATH=['#/build/lib'], LIBS=['imp'])

    if cpp:
        # Generate version information
        env['VER_CPP'], env['VER_H'] = \
            env.IMPModuleVersionInfo(
                 ('%s/src/internal/version_info.cpp' % (module),
                  '%s/include/internal/version_info.h' % (module)),
                 ())
        # Generate config header and SWIG equivalent
        env['CONFIG_H'] = env.IMPModuleConfig(('%s/include/config.h' % module,
                                               '%s/pyext/%s_config.i' \
                                               % (module, module)),
                                              env.Value(module))[0]
        env['LINK_0_CPP']=env.IMPModuleLinkTest('%s/src/internal/link_0.cpp' % module,
                                                env.Value(module))[0]
        env['LINK_1_CPP']=env.IMPModuleLinkTest('%s/src/internal/link_1.cpp' % module,
                                                env.Value(module))[0]
        env.AddMethod(IMPSharedLibraryEnvironment)
        env.AddMethod(IMPPythonExtensionEnvironment)
        env.AddMethod(IMPHeaders)

    env.AddMethod(IMPPython)
    env.AddMethod(IMPModuleTest)
    env.AddMethod(IMPModuleAbout)
    env.AddMethod(validate)
    env.AddMethod(invalidate)
    env.Append(BUILDERS={'_IMPModuleTest': \
                         Builder(action=Action(_action_unit_test,
                                               _print_unit_test),
                                 emitter=_emit_unit_test,
                                 source_scanner=pyscanner.PythonScanner)})
    env['TEST_ENVSCRIPT'] = None
    env['VALIDATED'] = None
    return env.SConscript('%s/SConscript' % module, exports='env')

def generate(env):
    """Add builders and construction variables for the IMP module tool."""
    env['IMP_MODULES_ALL'] = []
    env.AddMethod(IMPModule)

def exists(env):
    """Right now no external programs are needed"""
    return True
