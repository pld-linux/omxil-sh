#
# Conditional build:
%bcond_without	haacd		# AAC support via HAACD API/libSACP1
%bcond_without	hmp3d		# MP3 support via HMP3D API/libhmp3d
%bcond_without	shcodecs	# VPU support via libshcodecs
#
Summary:	OpenMAX IL components for SH-Mobile
Summary(pl.UTF-8):	Komponenty OpenMAX IL dla platformy SH-Mobile
Name:		omxil-sh
Version:	0.6.0
%define	snap	20091216
Release:	0.%{snap}.1
License:	LGPL v2.1+
Group:		Libraries
# git clone https://github.com/kfish/omxil-sh.git omxil-sh
Source0:	%{name}-%{snap}.tar.xz
# Source0-md5:	7be528945769685670d2ca3f2e72b1db
URL:		https://oss.renesas.com/modules/document/index.php
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	libomxil-bellagio
%{?with_shcodecs:BuildRequires:	libshcodecs-devel}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with haacd} || %{with hmp3d}
#BuildRequires:	proprietary Renesas SDK (libSACP1, libhmp3d)
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
omxil-sh is a collection of OpenMAX IL components for SH-Mobile, using
the Bellagio OpenMAX IL project framework.

%description -l pl.UTF-8
omxil-sh to zbiór komponentów OpenMAX IL dla platformy SH-Mopbile,
wykorzystujący szkielet Bellagio OpenMAX IL.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_haacd:--disable-aac} \
	%{!?with_hmp3d:--disable-mp3} \
	%{!?with_shcodecs:--disable-vpu}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with haacd} || %{with hmp3d} || %{with shcodecs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/bellagio/*.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/bin/omxregister-bellagio
%postun	-p /usr/bin/omxregister-bellagio

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_bindir}/omxsh-decode-audio
%attr(755,root,root) %{_bindir}/omxsh-decode-video
%{?with_haacd:%attr(755,root,root) %{_libdir}/bellagio/libomxshaac.so*}
%{?with_hmp3d:%attr(755,root,root) %{_libdir}/bellagio/libomxshmp3.so*}
%{?with_shcodecs:%attr(755,root,root) %{_libdir}/bellagio/libomxshvpudec.so*}
