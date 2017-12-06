# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------
""" Bison configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"

import os, sys, re
from openalea.sconsx.config import *


class Bison:
   def __init__(self, config):
      self.name = 'bison'
      self.config = config
      self._default = {}


   def default(self):

      if CONDA_ENV:
          if os.name == 'posix':
            self._default['bin'] = os.path.join(CONDA_LIBRARY_PREFIX, 'bin')
          else:
            # On windows, the conda package providing bison (m2-bison) is located in Library/usr
            self._default['bin'] = os.path.join(CONDA_LIBRARY_PREFIX, 'usr', 'bin')            
      elif isinstance(platform, Win32):
         try:
            # Try to use openalea egg
            from openalea.deploy import get_base_dir
            base_dir = get_base_dir("bisonflex")
            self._default['bin'] = os.path.join(base_dir, 'bin')
         except:
            self._default['bin'] = r'C:\Tools\Bin'

      elif isinstance(platform, Posix):
         self._default['bin'] = '/usr/bin'


   def option( self, opts):

      self.default()

      opts.Add('bison_bin', 'Bison binary path',
                self._default['bin'])


   def update(self, env):
      """ Update the environment with specific flags """
      t = Tool('yacc', toolpath=[getLocalPath()])
      t(env)

      env.Append(YACCFLAGS=['-d', '-v'])
      bison = env.WhereIs('bison', env['bison_bin'])
      env.Replace(YACC=bison)

      if bison:
         f =os.popen(str(bison)+" --version")
         l =f.readline()
         l =l.split()
         version_text = re.compile(r"\d+.\d+").match(l[-1])
         if version_text is None:
            raise UserWarning, "Unable to retrieve bison version number"
         version = float(version_text.group(0))
         f.close()

         if version >= 1.30:
            BISON_HPP =True
         else:
            BISON_HPP =False

         env.Append(BISON_HPP=BISON_HPP)
         if BISON_HPP:
            env.Append(CPPDEFINES =["BISON_HPP"])
         env['WITH_BISON'] = True  
         env.Append(CPPDEFINES =["WITH_BISON"])
      else:
        env['WITH_BISON'] = False  



   def configure(self, config):
      b = WhereIs("bison", config.conf.env['bison_bin'])

      if not b:
        s ="""
        Warning !!! Bison not found !
        Please, install Bison and try again.
        """
        print s
        sys.exit(-1)


def create(config):
   " Create bison tool "
   bison = Bison(config)

   return bison

