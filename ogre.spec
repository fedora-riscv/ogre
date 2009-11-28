Name:           ogre
Version:        1.6.4
Release:        5%{?dist}
Summary:        Object-Oriented Graphics Rendering Engine
# LGPLv2+ with exceptions - main library
# CC-BY-SA - devel docs
# Freely redistributable without restriction - most of samples content
# MIT      - shaders for DeferredShadingMedia samples
License:        LGPLv2+ with exceptions and CC-BY-SA and Freely redistributable without restriction and MIT
Group:          System Environment/Libraries
URL:            http://www.ogre3d.org/
# This is modified http://downloads.sourceforge.net/ogre/ogre-v%(echo %{version} | tr . -).tar.bz2
# with non-free files striped (see ogre-make-clean.sh):
# - Non-free licensed headers under RenderSystems/GL/include/GL removed
# - GLEW sources (RenderSystems/GL/include/GL, RenderSystems/GL/src/GL/glew.cpp) updated to 1.5.1 - upstream doesn't want to update http://www.ogre3d.org/phpBB2/viewtopic.php?t=44558
# - Non-free chiropteraDM.pk3 under Samples/Media/packs removed
# - Non-free fonts under Samples/Media/fonts removed
Source0:        %{name}-%{version}-clean.tar.bz2
Source1:        ogre-samples.sh
Patch0:         ogre-1.2.1-rpath.patch
#Patch1:         ogre-1.6.0-system-glew.patch
# Upstream patch to GLEW applied to new version
Patch1:         ogre-1.6.0rc1-glew.patch
Patch2:         ogre-1.6.4-system-tinyxml.patch
Patch3:         ogre-1.6.1-fix-ppc-build.patch
Patch4:         ogre-renderer-libs.patch
Patch5:         ogre-vertex-split-poses-9195.patch
Patch6:         ogre-RenderQueueGroupID-doc-9196.patch
Patch7:         ogre-multiple-contexts-GL-9202.patch
Patch8:         ogre-default-shadows-9213.patch
Patch9:         ogre-no-empty-dropdowns-9269.patch
Patch10:        ogre-modifiers-option-9283.patch
Patch11:        ogre-NULL-fix-9337.patch
Patch12:        ogre-line-list-stencil-shadows-9342.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cegui-devel zziplib-devel freetype-devel
BuildRequires:  libXaw-devel libXrandr-devel libXxf86vm-devel libGLU-devel
BuildRequires:  ois-devel freeimage-devel openexr-devel
#BuildRequires:  glew-devel
BuildRequires:  tinyxml-devel

%description
OGRE (Object-Oriented Graphics Rendering Engine) is a scene-oriented,
flexible 3D engine written in C++ designed to make it easier and more
intuitive for developers to produce applications utilizing
hardware-accelerated 3D graphics. The class library abstracts all the
details of using the underlying system libraries like Direct3D and
OpenGL and provides an interface based on world objects and other
intuitive classes.


%package devel
Summary:        Ogre header files and documentation
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains the header files for Ogre.
Install this package if you want to develop programs that use Ogre.


%package devel-doc
Summary:        Ogre development documentation
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description devel-doc
This package contains the Ogre API documentation and the Ogre development
manual. Install this package if you want to develop programs that use Ogre.


%package samples
Summary:        Ogre samples executables and media
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}, dejavu-sans-fonts

%description samples
This package contains the compiled (not the source) sample applications coming
with Ogre.  It also contains some media (meshes, textures,...) needed by these
samples. The samples are installed in %{_libdir}/Samples and can be executed
with the wrapper script called "Ogre-Samples".


%prep
%setup -q -n ogre
%patch0 -p1 -z .rpath
%patch1 -p1 -z .glew
%patch2 -p1 -z .sys-tinyxml
%patch3 -p1 -z .ppc
%patch4 -p1
%patch5
%patch6
%patch7
%patch8
%patch9
%patch10
%patch11
%patch12
# remove execute bits from src-files for -debuginfo package
chmod -x `find RenderSystems/GL -type f` \
  `find Samples/DeferredShading -type f` Samples/DynTex/src/DynTex.cpp
# Fix path to Media files for the Samples
sed -i 's|../../Media|%{_datadir}/OGRE/Samples/Media|g' \
  Samples/Common/bin/resources.cfg
# Remove spurious execute buts from some Media files
chmod -x `find Samples/Media/DeferredShadingMedia -type f` \
  Samples/Media/overlays/Example-DynTex.overlay \
  Samples/Media/gui/TaharezLook.looknfeel \
  Samples/Media/gui/Falagard.xsd \
  Samples/Media/materials/scripts/Example-DynTex.material
# create a clean version of the api docs for %%doc
mkdir api
find . \( -wholename './Docs/api/html/*.html' -or \
  -wholename './Docs/api/html/*.gif' -or -wholename './Docs/api/html/*.png' \
  -or -wholename './Docs/api/html/*.css' \) -exec cp --target-directory='api' '{}' +
for i in api/OgreParticleEmitter_8h-source.html \
         api/classOgre_1_1ParticleSystem.html \
         api/classOgre_1_1DynLib.html \
         api/classOgre_1_1ParticleEmitter.html; do
  iconv -f ISO_8859-2 -t UTF8 $i > api/tmp
  touch -r $i api/tmp
  mv api/tmp $i
done
# Add lgpl.txt symlink for links in License.html
rm -r Docs/licenses/*
ln -s ../COPYING Docs/licenses/lgpl.txt
# remove included tinyxml headers to ensure use of system headers
rm Tools/XMLConverter/include/tiny*


%build
%configure --disable-cg --disable-devil --enable-openexr
# Don't link to unneeded stuff
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Stop ogre from linking the GL render plugin against the system libOgre
# instead of the just build one.
sed -i 's|-L%{_libdir}||g' `find -name Makefile`
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/OGRE/*.la

# These 2 not really public header files are needed for ogre4j
install -p -m 644 \
  OgreMain/include/OgreOptimisedUtil.h \
  OgreMain/include/OgrePlatformInformation.h \
  $RPM_BUILD_ROOT%{_includedir}/OGRE

# Create config for ldconfig
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo "%{_libdir}/OGRE" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/%{name}-%{_arch}.conf

# Install the samples
mkdir -p $RPM_BUILD_ROOT%{_libdir}/OGRE/Samples
# The Sample binaries get installed into the buildroot in a subdir of
# the cwd??
mv $RPM_BUILD_ROOT`pwd`/Samples/Common/bin/* \
  $RPM_BUILD_ROOT%{_libdir}/OGRE/Samples
for cfg in plugins.cfg media.cfg quake3settings.cfg resources.cfg; do
  install -p -m 644 Samples/Common/bin/$cfg \
    $RPM_BUILD_ROOT%{_libdir}/OGRE/Samples
done
sed -i 's|^PluginFolder=.*$|PluginFolder=%{_libdir}/OGRE|' \
    $RPM_BUILD_ROOT%{_libdir}/OGRE/Samples/plugins.cfg
# Change location of pak + switch from non-free chiropteraDM map
sed -i 's|^Pak0Location: ../../Media/.*$|Pak0Location: %{_datadir}/OGRE/Samples/Media/packs/ogretestmap.zip|' \
    $RPM_BUILD_ROOT%{_libdir}/OGRE/Samples/quake3settings.cfg
sed -i 's|^Map:.*$|Map: ogretestmap.bsp|' \
    $RPM_BUILD_ROOT%{_libdir}/OGRE/Samples/quake3settings.cfg
# Fixing bug with wrong case for media
mv Samples/Media/PCZAppMedia/ROOM_NY.mesh Samples/Media/PCZAppMedia/room_ny.mesh
mv Samples/Media/PCZAppMedia/ROOM_PY.mesh Samples/Media/PCZAppMedia/room_py.mesh
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/Ogre-Samples

mkdir -p $RPM_BUILD_ROOT%{_datadir}/OGRE/Samples
cp -a Samples/Media $RPM_BUILD_ROOT%{_datadir}/OGRE/Samples
ln -s ../../../../fonts/dejavu/DejaVuSans-Bold.ttf \
  $RPM_BUILD_ROOT%{_datadir}/OGRE/Samples/Media/fonts/bluebold.ttf
ln -s ../../../../fonts/dejavu/DejaVuSans.ttf \
  $RPM_BUILD_ROOT%{_datadir}/OGRE/Samples/Media/fonts/bluehigh.ttf
ln -s ../../../../fonts/dejavu/DejaVuSansCondensed.ttf \
  $RPM_BUILD_ROOT%{_datadir}/OGRE/Samples/Media/fonts/bluecond.ttf
ln -s ../../../../fonts/dejavu/DejaVuSans.ttf \
  $RPM_BUILD_ROOT%{_datadir}/OGRE/Samples/Media/fonts/solo5.ttf       


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING
%doc Docs/ChangeLog.html Docs/License.html Docs/licenses Docs/ReadMe.html Docs/style.css Docs/ogre-logo*.gif
%{_bindir}/Ogre*
%{_bindir}/rcapsdump
%{_libdir}/lib*Ogre*-%{version}.so
%{_libdir}/OGRE
%{_datadir}/OGRE
%exclude %{_bindir}/Ogre-Samples
%exclude %{_libdir}/OGRE/Samples
%exclude %{_datadir}/OGRE/Samples
%config(noreplace) /etc/ld.so.conf.d/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libOgreMain.so
%{_libdir}/libCEGUIOgreRenderer.so
%{_includedir}/OGRE
%{_libdir}/pkgconfig/*.pc

%files devel-doc
%defattr(-,root,root,-)
%doc LINUX.DEV api Docs/manual Docs/shadows Docs/vbo-update Docs/style.css

%files samples
%defattr(-,root,root)
%doc Samples/ReadMe.html
%{_bindir}/Ogre-Samples
%{_libdir}/OGRE/Samples
%{_datadir}/OGRE/Samples


%changelog
* Sat Nov 28 2009 Bruno Wolff III <bruno@wolff.to> - 1.6.4-5
- Get upstream fixes since 1.6.4 release. This includes a couple of crash bugs.

* Mon Nov 23 2009 Bruno Wolff III <bruno@wolff.to> - 1.6.4-4
- Allow CEGIUOgreRenderer to find needed libraries

* Sat Nov 21 2009 Bruno Wolff III <bruno@wolff.to> - 1.6.4-3
- Spec file cleanups

* Tue Nov 17 2009 Bruno Wolff III <bruno@wolff.to> - 1.6.4-2
- Rebuild for ois 1.2

* Mon Sep 28 2009 Alexey Torkhov <atorkhov@gmail.com> - 1.6.4-1
- New upstream release 1.6.4

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 Alexey Torkhov <atorkhov@gmail.com> - 1.6.2-1
- New upstream release 1.6.2
- Exceptions added to License
- Reenabling OpenEXR plugin, as it fixed now

* Fri Mar 06 2009 Alexey Torkhov <atorkhov@gmail.com> - 1.6.1-5
- Add licenses of samples to License tag

* Mon Mar 02 2009 Alexey Torkhov <atorkhov@gmail.com> - 1.6.1-4
- Update Ogre-Samples to work properly without CgProgramManager plugin

* Fri Feb 27 2009 Alexey Torkhov <atorkhov@gmail.com> - 1.6.1-3
- Fixing PPC build

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 10 2009 Alexey Torkhov <atorkhov@gmail.com> 1.6.1-1
- New upstream release 1.6.1

* Tue Jan 20 2009 Hans de Goede <hdegoede@redhat.com> 1.6.0-5
- Adjust font requires for font rename (rh 480465)

* Sat Jan 10 2009 Hans de Goede <hdegoede@redhat.com> 1.6.0-4
- use regular (full) instead of lgc dejavu fonts for the demos (rh 477434)

* Sat Dec 27 2008 Hans de Goede <hdegoede@redhat.com> 1.6.0-3
- Remove non-free fonts from samples subpackage (rh 477434)

* Wed Dec  3 2008 Hans de Goede <hdegoede@redhat.com> 1.6.0-2
- Rebuild for new cegui

* Thu Nov 06 2008 Alexey Torkhov <atorkhov@gmail.com> 1.6.0-1
- New upstream release 1.6.0
- Updated samples running script
- Removed non-free quake map from samples media
- Added docs license in License tag

* Sat Sep 21 2008 Alexey Torkhov <atorkhov@gmail.com> 1.6.0-0.1.rc1
- New upstream release 1.6.0rc1
- Disabling broken OpenEXR plugin, it is not updated for long time and doesn't
  compile. FreeImage now have EXR support
- Updated private GLEW sources to 1.5.0 due to license issues and compiling
  against it instead of system ones, as it is patched by upstream

* Fri Jul 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.9-2
- Rebuild for new cegui

* Wed Jul  2 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.9-1
- New upstream release 1.4.9

* Thu May 22 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.8-2
- Rebuild for new cegui
- Use system tinyxml (bz 447698)

* Tue May 13 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.8-1
- New upstream release 1.4.8
- Warning as always with a new upstream ogre release this breaks the ABI
  and changes the soname!

* Sun Mar 30 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.7-2
- Switch to freeimage as imagelibrary, as upstream is abandoning DevIL support
  (bz 435399)
- Enable the openexr plugin

* Sun Mar 16 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.7-1
- New upstream release 1.4.7
- Warning as always with a new upstream ogre release this breaks the ABI
  and changes the soname!

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.6-5
- Autorebuild for GCC 4.3

* Thu Jan 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.6-4
- Install 2 additional header files for ogre4j (bz 429965)

* Tue Jan 22 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.6-3
- Rebuild for new glew

* Sat Jan 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.6-2
- Oops I just found out that ogre contains private copies of GL and GLEW
  headers, which fall under the not 100% SGI Free Software B and GLX Public
  License licenses, remove these (even from the tarbal!) and use the system
  versions instead

* Sat Dec 29 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.6-1
- New upstream release 1.4.6
- Warning as always with a new upstream ogre release this breaks the ABI
  and changes the soname!

* Wed Nov 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.5-3
- Fix building of ogre with an older version of ogre-devel installed
  (bz 382311)

* Mon Nov 12 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.5-2
- Ogre-Samples now takes the name of which samples to run as arguments, if no
  arguments are provided, it will run all of them like it used too (bz 377011)
- Don't install a useless / broken plugins.cfg in the Samples folder,
  Ogre-Samples will generate a correct one when run (bz 377011)

* Mon Oct  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.5-1
- New upstream release 1.4.5

* Fri Sep 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.4-1
- New upstream release 1.4.4 (bz 291481)

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.2-2
- Update License tag for new Licensing Guidelines compliance

* Sat Jun 30 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.2-1
- New upstream release 1.4.2
- Warning as always with a new upstream ogre release this breaks the ABI
  and changes the soname!
- Warning this release also breaks the API!

* Thu May 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.5-2
- Fix building on ppc64

* Fri Feb 16 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.5-1
- New upstream release 1.2.5

* Fri Jan 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.3-2
- Rebuild for new cairomm
- Added a samples sub-package (suggested by Xavier Decoret)

* Fri Oct 27 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.3-1
- New upstream release 1.2.3
- Warning as always with a new upstream ogre release this breaks the ABI
  and changes the soname!

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.2-2.p1
- FE6 Rebuild

* Thu Jul 27 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.2-1.p1
- New upstream release 1.2.2p1
- Drop integrated char_height patch
- Drop ogre-1.2.1-visibility.patch since this is fixed with the latest gcc
  release, but keep it in CVS in case things break again.
- Add a patch that replaces -version-info libtool argument with -release,
  which results in hardcoding the version number into the soname. This is
  needed because upstream changes the ABI every release, without changing the
  CURRENT argument passed to -version-info .
- Also add -release when linking libCEGUIOgreRenderer.so as that was previously
  unversioned.

* Tue Jul 18 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.1-3
- Add ogre-1.2.1-visibility.patch to fix issues with the interesting new
  gcc visibility inheritance.

* Fri Jul  7 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.2.1-2
- Make -devel package Requires on the main package fully versioned.
- Move libOgrePlatform.so out of %%{_libdir} and into the OGRE plugins dirs as
  its not versioned and only used through dlopen, so its effectivly a plugin.  

* Thu Jun 15 2006 Hans de Goede 1.2.1-1
- Initial FE packaging attempt, loosely based on a specfile created by
  Xavier Decoret <Xavier.Decoret@imag.fr>
