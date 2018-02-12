import os
import ycm_core

flags = [
'-Wall',
'-Werror',

# std is required
# clang won't know which language to use compiling headers
'-std=c++11',

# '-x' and 'c++' also required
# use 'c' for C projects
'-x',
'c++',
'-x',
'c++11',
'-I', '.',
'-I', './common',

# include third party libraries
#'-isystem',
#'/usr/include/python2.7',
]

# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags. Notice that YCM itself uses that approach.
graphite_folder = "/home/maxence/ext/GraphiteThree_latest"
compilation_database_folder = '.'
if os.path.isfile(graphite_folder + "/build/Linux64-gcc-dynamic-Release/compile_commands.json"):
    compilation_database_folder = graphite_folder + '/build/Linux64-gcc-dynamic-Release'
elif os.path.isfile(graphite_folder + "/build/Linux64-gcc-dynamic-Debug/compile_commands.json"):
    compilation_database_folder = graphite_folder + '/build/Linux64-gcc-dynamic-Debug'


if os.path.exists( compilation_database_folder ):
  database = ycm_core.CompilationDatabase( compilation_database_folder )
else:
  database = None

SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.c', '.m', '.mm' ]

def DirectoryOfThisScript():
  return os.path.dirname( os.path.abspath( __file__ ) )


def MakeRelativePathsInFlagsAbsolute( flags, working_directory ):
  if not working_directory:
    return list( flags )
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    new_flag = flag

    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join( working_directory, flag )

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        new_flag = path_flag + os.path.join( working_directory, path )
        break

    if new_flag:
      new_flags.append( new_flag )
  return new_flags


def IsHeaderFile( filename ):
  extension = os.path.splitext( filename )[ 1 ]
  return extension in [ '.h', '.hxx', '.hpp', '.hh' ]


def GetCompilationInfoForFile( filename ):
    # The compilation_commands.json file generated by CMake does not have entries
    # for header files. So we do our best by asking the db for flags for a
    # corresponding source file, if any. If one exists, the flags for that file
    # should be good enough.
    if IsHeaderFile( filename ):
        basename = os.path.splitext( filename )[ 0 ]
        for extension in SOURCE_EXTENSIONS:
            replacement_file = basename + extension
            if os.path.exists( replacement_file ):
                compilation_info = database.GetCompilationInfoForFile( replacement_file )
                if compilation_info.compiler_flags_:
                    return compilation_info
        common_file_cpp = "/home/maxence/src/unobtainium/common/unobtainium_common.cpp"
        if os.path.exists(common_file_cpp):
            compilation_info = database.GetCompilationInfoForFile( common_file_cpp )
            if compilation_info.compiler_flags_:
                return compilation_info
        return None
    return database.GetCompilationInfoForFile( filename )


def FlagsForFile( filename, **kwargs ):
  if database:
    # Bear in mind that compilation_info.compiler_flags_ does NOT return a
    # python list, but a "list-like" StringVec object
    compilation_info = GetCompilationInfoForFile( filename )
    if not compilation_info:
      return None

    final_flags = MakeRelativePathsInFlagsAbsolute(
      compilation_info.compiler_flags_,
      compilation_info.compiler_working_dir_ )
    # final_flags.append('-x')
    # final_flags.append('c++')
    # final_flags.append('-std=c++11')
    # final_flags.append('-isystem')
    # final_flags.append('/usr/include')
    # final_flags.append('-isystem')
    # final_flags.append('/usr/include/x86_64-linux-gnu')
    # final_flags.append('-isystem')
    # final_flags.append('/usr/local/include')
    # final_flags.append('-isystem')
    # final_flags.append('/usr/bin/../lib/clang/3.5/include')
    # final_flags.append('-isystem')
    # final_flags.append('/usr/bin/../lib/gcc/x86_64-linux-gnu/4.8/include')
    # final_flags.append('-isystem')
    # final_flags.append('/usr/include/c++/4.8')
    # final_flags.append('-isystem')
    # final_flags.append('/usr/include/x86_64-linux-gnu/c++/4.8')
  else:
    relative_to = DirectoryOfThisScript()
    final_flags = MakeRelativePathsInFlagsAbsolute( flags, relative_to )

  return {
    'flags': final_flags,
    'do_cache': True
  }
