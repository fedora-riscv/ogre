#!/bin/sh

set -e
set -x

version=1.12.9

[ ! -e ogre-${version} ] && wget https://github.com/OGRECave/ogre/archive/v${version}/ogre-${version}.tar.gz

# Clean up
tar xf ogre-${version}.tar.gz
pushd ogre-${version}
  # - Non-free licensed headers under RenderSystems/GL/include/GL removed
  rm RenderSystems/GL/include/GL/{gl,glext}.h

  # - GLEW sources updated
  # not working glew.c:1542:1: error: unknown type name 'PFNGLPROGRAMUNIFORM1DEXTPROC';
  rpm -q glew-devel glew-debugsource
  echo if package glew-debugsource is not installed, dnf debuginfo-install glew
  cp -f /usr/include/GL/{glew,glxew,wglew}.h RenderSystems/GL/include/GL/
  cp -f /usr/src/debug/glew-*/src/glew.c RenderSystems/GL/src/glew.cpp
  dos2unix RenderSystems/GL/src/glew.cpp


  # https://github.com/OGRECave/ogre/issues/882
  # - Non-free chiropteraDM.pk3 under Samples/Media/packs removed
  # rm Samples/Media/packs/chiropteraDM.{pk3,txt}

  # - Non-free textures under Samples/Media/materials/textures/nvidia removed
  # rm Samples/Media/materials/textures/nvidia/*
popd
tar cjf ogre-${version}-clean.tar.bz2 ogre-${version}
