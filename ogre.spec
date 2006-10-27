Name:           ogre
Version:        1.2.3
Release:        1%{?dist}
Summary:        Object-Oriented Graphics Rendering Engine
License:        LGPL
Group:          System Environment/Libraries
URL:            http://www.ogre3d.org/
Source0:        http://dl.sf.net/sourceforge/ogre/ogre-linux_osx-v%(echo %{version} | tr . -).tar.bz2
Patch0:         ogre-1.2.1-rpath.patch
Patch1:         ogre-1.2.2-soname.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cegui-devel zziplib-devel DevIL-devel SDL-devel freetype-devel
BuildRequires:  libglademm24-devel libsigc++20-devel

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

%description devel-doc
This package contains the Ogre API documentation and the Ogre development
manual. Install this package if you want to develop programs that use Ogre.


%prep
%setup -q -n ogrenew
%patch0 -p1 -z .rpath
%patch1 -p1 -z .soname
# sigh stop autoxxx from rerunning because of our patches above.
touch aclocal.m4
touch configure
touch `find -name Makefile.in`
touch OgreMain/include/config.h.in
# we don't do this with a patch since we need %{_libdir}
sed -i 's|libOgrePlatform.so|%{_libdir}/OGRE/libOgrePlatform.so|' \
  OgreMain/include/OgrePlatform.h
rm -fr `find Docs -name CVS`
#remove execute bits from src-files for -debuginfo package
chmod -x `find RenderSystems/GL -type f`


%build
# Upstream advises --with-platform=GLX, but that uses Xrandr for fullscreen,
# which has issues (see bz 190918).
# Notice that if we switch back to GLX --with-cfgtk=gtk can be removed and so
# can the libglademm24-devel and libsigc++20-devel BuildRequires.
%configure --with-platform=SDL --with-cfgtk=gtk --disable-cg
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/OGRE/*.la
# move libOgrePlatform.so out of %{_libdir} and into the OGRE plugins dirs as
# its not versioned and only used through dlopen, so its effectivly a plugin.
mv $RPM_BUILD_ROOT%{_libdir}/libOgrePlatform.so $RPM_BUILD_ROOT%{_libdir}/OGRE

# fix rpm-debuginfo not handling symlinks correctly <sigh> see BZ 189928
pushd PlatformManagers/SDL
rm src/OgreSDLConfig.cpp
cp src/OgreSDLConfig_gtk.cpp src/OgreSDLConfig.cpp
rm include/OgreSDLConfig.h
cp include/OgreSDLConfig_gtk.h include/OgreSDLConfig.h
popd

# the gtk-configurator wants this file and it doesn't get installed
# by make install so DYI
mkdir -p $RPM_BUILD_ROOT%{_datadir}/OGRE/Media
install -p -m 644 Samples/Media/materials/textures/ogrelogo-small.jpg \
  $RPM_BUILD_ROOT%{_datadir}/OGRE/Media


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

%files devel
%defattr(-,root,root,-)
%{_libdir}/libOgreMain.so
%{_libdir}/libCEGUIOgreRenderer.so
%{_includedir}/OGRE
%{_libdir}/pkgconfig/*.pc

%files devel-doc
%defattr(-,root,root,-)
%doc LINUX.DEV Docs/api Docs/manual Docs/vbo-update Docs/style.css


%changelog
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
