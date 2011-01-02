#!/bin/sh

set -e
set -x

version=1.7.2

[ ! -e ogre-${version} ]

tar xjf ogre_src_v$(echo ${version} | tr . -).tar.bz2

cd ogre_src_v$(echo ${version} | tr . -)

# - Non-free licensed headers under RenderSystems/GL/include/GL removed
rm RenderSystems/GL/include/GL/{gl,glext,glxext,glxtokens,wglext}.h

# - GLEW sources updated to 1.5.5
rpm -q glew-devel glew-debuginfo
cp -f /usr/include/GL/{glew,glxew,wglew}.h RenderSystems/GL/include/GL/
cp -f /usr/src/debug/glew-*/src/glew.c RenderSystems/GL/src/glew.cpp
dos2unix RenderSystems/GL/src/glew.cpp

# - Non-free chiropteraDM.pk3 under Samples/Media/packs removed
rm Samples/Media/packs/chiropteraDM.{pk3,txt}

# - Non-free fonts under Samples/Media/fonts removed
rm Samples/Media/fonts/{bluebold,bluecond,bluehigh,solo5}.ttf

# - Non-free textures under Samples/Media/materials/textures/nvidia removed
rm Samples/Media/materials/textures/nvidia/*

cd ..

mv ogre_src_v$(echo ${version} | tr . -) ogre-${version}

tar cjf ogre-$version-clean.tar.bz2 ogre-${version}
