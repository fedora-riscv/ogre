#!/bin/sh

set -e
set -x

version=1.9.0

[ ! -e ogre-${version} ]

rpm -q mercurial
hg clone https://bitbucket.org/sinbad/ogre ogre-${version}
hg archive -R ogre-${version} -r v$(echo ${version} | tr . -) -t tbz2 ogre-${version}.tar.bz2
rm -rf ogre-${version}

# Clean up
tar xjf ogre-${version}.tar.bz2
pushd ogre-${version}
  # - Non-free licensed headers under RenderSystems/GL/include/GL removed
  rm RenderSystems/GL/include/GL/{gl,glext,glxext,glxtokens,wglext}.h

  # - GLEW sources updated
  rpm -q glew-devel glew-debuginfo
  cp -f /usr/include/GL/{glew,glxew,wglew}.h RenderSystems/GL/include/GL/
  cp -f /usr/src/debug/glew-*/src/glew.c RenderSystems/GL/src/glew.cpp
  dos2unix RenderSystems/GL/src/glew.cpp

  # - Non-free chiropteraDM.pk3 under Samples/Media/packs removed
  rm Samples/Media/packs/chiropteraDM.{pk3,txt}

  # - Non-free textures under Samples/Media/materials/textures/nvidia removed
  rm Samples/Media/materials/textures/nvidia/*
popd
tar cjf ogre-${version}-clean.tar.bz2 ogre-${version}
