#!/bin/sh

set -e
set -x

version=1.12.9

[ ! -e ogre-${version} ] && wget -c https://github.com/OGRECave/ogre/archive/v${version}/ogre-${version}.tar.gz

# Clean up
tar xf ogre-${version}.tar.gz
pushd ogre-${version}
  # - Non-free licensed headers under RenderSystems/GL/include/GL removed
  rm RenderSystems/GL/include/GL/{gl,glext}.h

  # - GLEW sources updated
  # not working glew.c:1542:1: error: unknown type name 'PFNGLPROGRAMUNIFORM2IVEXTPROC';
  rpm -q glew-devel glew-debugsource
  echo if package glew-debugsource is not installed, please do 'dnf debuginfo-install glew'
  cp -f /usr/include/GL/{glew,glxew,wglew}.h RenderSystems/GL/include/GL/
  cp -f /usr/src/debug/glew-*/src/glew.c RenderSystems/GL/src/glew.c

  # https://github.com/OGRECave/ogre/issues/882
  # - Non-free chiropteraDM.pk3 under Samples/Media/packs removed
  # rm Samples/Media/packs/chiropteraDM.{pk3,txt}
  # https://github.com/OGRECave/ogre/commit/d7dc7119720a06f5d373bc6553bae1399ab5fb2e
  # Samples: BSP - replace chiropteraDM by OpenArena oa_rpg3dm2

  # - Non-free textures under Samples/Media/materials/textures/nvidia removed
  # rm Samples/Media/materials/textures/nvidia/*
  # https://github.com/OGRECave/ogre/commit/302e970e6d56c5642f1879700ff891798c98d3b2
  # Samples: Terrain - replace proprietary nvidia textures by cc0textures 
popd
tar cJf ogre-${version}-clean.tar.xz ogre-${version}
