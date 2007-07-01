#!/bin/bash

set -e

# find out LIBDIR
if [ -f /usr/lib64/OGRE/Samples/resources.cfg ]; then
  LIBDIR=/usr/lib64
else
  LIBDIR=/usr/lib
fi

mkdir -p $HOME/.ogre-samples
cd $HOME/.ogre-samples

cp -f $LIBDIR/OGRE/Samples/resources.cfg .
cp -f $LIBDIR/OGRE/Samples/media.cfg .

echo "# Defines plugins to load" > plugins.cfg
echo >> plugins.cfg
echo "# Define plugin folder" >> plugins.cfg
echo "PluginFolder=$LIBDIR/OGRE" >> plugins.cfg
echo >> plugins.cfg
echo "# Define D3D rendering implementation plugin" >> plugins.cfg
for i in `(cd $LIBDIR/OGRE; ls *.so)`; do
  if [ $i != libOgrePlatform.so ]; then
    echo "Plugin=$i" >> plugins.cfg
  fi
done

set +e

for i in `(cd $LIBDIR/OGRE/Samples/; find -type f -perm +111)`; do
  if [ $i != ./BSP ]; then
    $LIBDIR/OGRE/Samples/$i
  fi
done
