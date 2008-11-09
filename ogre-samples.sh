#!/bin/sh

selectPCZ()
{
  sed -i 's|^\(Plugin=Plugin_OctreeSceneManager.so\)|#\1|' plugins.cfg
  sed -i 's|^#\(Plugin=libPlugin_PCZSceneManager.so\)|\1|' plugins.cfg
  sed -i 's|^#\(Plugin=Plugin_OctreeZone.so\)|\1|' plugins.cfg
}

unselectPCZ()
{
  sed -i 's|^#\(Plugin=Plugin_OctreeSceneManager.so\)|\1|' plugins.cfg
  sed -i 's|^\(Plugin=libPlugin_PCZSceneManager.so\)|#\1|' plugins.cfg
  sed -i 's|^\(Plugin=Plugin_OctreeZone.so\)|#\1|' plugins.cfg
}

runSample()
{
  sample=$1
  if [ "$sample" = "PCZTestApp" ]; then
    selectPCZ
  else
    unselectPCZ
  fi

  echo "Running $sample..."
  $LIBDIR/OGRE/Samples/$sample

  if [ "$sample" = "PCZTestApp" ]; then
    unselectPCZ
  fi
}

set -e

# find out LIBDIR
if [ -f /usr/lib64/OGRE/Samples/resources.cfg ]; then
  LIBDIR=/usr/lib64
else
  LIBDIR=/usr/lib
fi

mkdir -p $HOME/.ogre-samples
cd $HOME/.ogre-samples

for i in plugins.cfg media.cfg quake3settings.cfg resources.cfg; do
  cp -f $LIBDIR/OGRE/Samples/$i .
done

set +e

if [ "$1" = "-a" ]; then
  for i in `(cd $LIBDIR/OGRE/Samples/; find -type f -perm +111 | sort)`; do
    runSample `echo $i | sed 's|./||'`
  done
elif [ $# -ge 1 ]; then
  while [ $# -ge 1 ]; do
    runSample $1
    shift
  done
else
  echo "Usage:" `basename $0` "(samples | -a)"
  echo
  echo "samples - Runs specified samples from list"
  echo "-a      - Runs all samples"
  echo
  echo -n "Available samples:"
  for i in `(cd $LIBDIR/OGRE/Samples/; find -type f -perm +111 | sort)`; do
    echo -n " $i" | sed 's|./||'
  done
  echo
fi
