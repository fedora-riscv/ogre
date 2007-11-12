Name:           ogre
Version:        1.4.5
Release:        2%{?dist}
Summary:        Object-Oriented Graphics Rendering Engine
License:        LGPLv2+
Group:          System Environment/Libraries
URL:            http://www.ogre3d.org/
Source0:        http://downloads.sourceforge.net/ogre/ogre-linux_osx-v%(echo %{version} | tr . -).tar.bz2
Source1:        ogre-samples.sh
Patch0:         ogre-1.2.1-rpath.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cegui-devel zziplib-devel DevIL-devel freetype-devel gtk2-devel
BuildRequires:  libXaw-devel libXrandr-devel libXxf86vm-devel libGLU-devel
BuildRequires:  ois-devel

%description
OGRE (Object-Oriented Graphics Rendering Engine) is a scene-oriented,
flexible 3D engine written in C++ designed to make it easier and more
intuitive for developers to produce applications utilising
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
Requires:       %{name} = %{version}-%{release}

%description samples
This package contains the compiled (not the source) sample applications coming
with Ogre.  It also contains some media (meshes, textures,...) needed by these
samples. The samples are installed in %{_libdir}/Samples and can be executed
with the wrapper script called "Ogre-Samples".


%prep
%setup -q -n ogrenew
%patch0 -p1 -z .rpath
# building ogre while ogre-devel is installed results in binaries getting
# linked against the installed version, instead of the just build one <sigh>
if [ -f /usr/include/OGRE/Ogre.h ]; then
  echo "Error building ogre while ogre-devel is installed does not work!"
  exit 1
fi
# stop some CVS stuff from getting installed
rm -r `find Docs Samples/Media -name CVS`
# fix line-endings of Docs
sed -i 's/\r//g' Docs/ChangeLog.html Docs/manual/*.html
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
cp Docs/api/html/*.html Docs/api/html/*.gif Docs/api/html/*.png \
  Docs/api/html/*.css api
for i in api/OgreParticleEmitter_8h-source.html \
         api/classOgre_1_1ParticleSystem.html \
         api/classOgre_1_1DynLib.html \
         api/classOgre_1_1ParticleEmitter.html; do
  iconv -f ISO_8859-2 -t UTF8 $i > api/tmp
  mv api/tmp $i
done


%build
# notice we disable freeimage (and thus use DevIL) because freeimage
# is GPL not LGPL
%configure --disable-cg --disable-freeimage
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/OGRE/*.la

# Install the samples
mkdir -p $RPM_BUILD_ROOT%{_libdir}/OGRE/Samples
# The Sample binaries get installed into the buildroot in a subdir of
# the cwd??
mv $RPM_BUILD_ROOT`pwd`/Samples/Common/bin/* \
  $RPM_BUILD_ROOT%{_libdir}/OGRE/Samples
for cfg in media.cfg quake3settings.cfg resources.cfg; do
  install -p -m 644 Samples/Common/bin/$cfg \
    $RPM_BUILD_ROOT%{_libdir}/OGRE/Samples
done
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/Ogre-Samples

mkdir -p $RPM_BUILD_ROOT%{_datadir}/OGRE/Samples
cp -a Samples/Media $RPM_BUILD_ROOT%{_datadir}/OGRE/Samples


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING 
%doc Docs/ChangeLog.html Docs/ReadMe.html Docs/style.css Docs/ogre-logo.gif
%{_bindir}/Ogre*
%{_libdir}/lib*Ogre*-%{version}.so
%{_libdir}/OGRE
%{_datadir}/OGRE
%exclude %{_bindir}/Ogre-Samples
%exclude %{_libdir}/OGRE/Samples
%exclude %{_datadir}/OGRE/Samples

%files devel
%defattr(-,root,root,-)
%{_libdir}/libOgreMain.so
%{_libdir}/libCEGUIOgreRenderer.so
%{_includedir}/OGRE
%{_libdir}/pkgconfig/*.pc

%files devel-doc
%defattr(-,root,root,-)
%doc LINUX.DEV api Docs/manual Docs/vbo-update Docs/style.css

%files samples
%defattr(-,root,root)
%{_bindir}/Ogre-Samples
%{_libdir}/OGRE/Samples
%{_datadir}/OGRE/Samples


%changelog
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
