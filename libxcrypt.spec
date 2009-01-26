
Name:           libxcrypt
License:        LGPL v2.1 or later; Public Domain, Freeware
Group:          System/Libraries
AutoReqProv:    on
Version:        3.0.2
Release:        %mkrel 1
Summary:        Crypt Library for DES, MD5, Blowfish and others
Source:         libxcrypt-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, SHA256, SHA512 and passwords with
blowfish encryption.



%package devel
License:        LGPL v2.1 or later; Public Domain, Freeware
Summary:        Development Include Files and Libraries for enhanced crypt functionality
Group:          Development/Libraries/C and C++
Requires:       libxcrypt = %{version}
AutoReqProv:    on

%description devel
libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, and passwords with blowfish
encryption.

This package contains the header files and static libraries necessary
to develop software using libxcrypt.



%prep
%setup -q

%build
./configure CFLAGS="$RPM_OPT_FLAGS -Wno-cast-align" \
	--prefix=%{_prefix} \
	--libdir=/%{_lib} --disable-static
make


%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_libdir}
rm %{buildroot}/%{_lib}/libxcrypt.{so,la}
rm %{buildroot}/%{_lib}/xcrypt/lib*.{so,la}
ln -sf ../../%{_lib}/libxcrypt.so.2 %{buildroot}%{_libdir}/libxcrypt.so
/sbin/ldconfig -n %{buildroot}/%{_lib}/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING README NEWS README.bcrypt README.ufc-crypt
/%{_lib}/libxcrypt.so.*
%dir /%{_lib}/xcrypt
/%{_lib}/xcrypt/lib*.so.*

%files devel
%defattr(-,root,root)
%{_prefix}/include/*.h
%{_libdir}/libxcrypt.so

