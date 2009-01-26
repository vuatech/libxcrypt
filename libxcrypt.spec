%define major 2
%define libname	%mklibname xcrypt %{major}
%define develname %mklibname xcrypt -d

Summary:	Crypt Library for DES, MD5, Blowfish and others
Name:		libxcrypt
Version:	3.0.2
Release:	%mkrel 2
License:	LGPLv2+
Group:		System/Libraries
Url:		provide_url_to_some_site
# where is full url to the source ?
Source0:	%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, SHA256, SHA512 and passwords with
blowfish encryption.

%package -n %{libname}
Summary:	Crypt Library for DES, MD5, Blowfish and others
Group:          System/Libraries

%description -n %{libname}
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, SHA256, SHA512 and passwords with
blowfish encryption.

%package -n %{develname}
Summary:	Development libraries for %{name}
Group:          Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}

%description -n %{develname}
This package contains the header files and static libraries necessary
to develop software using %{name}.

%prep
%setup -q

%build
export CFLAGS="%{optflags} -Wno-cast-align"
%configure2_5x  \
	--libdir=/%{_lib} \
	--disable-static

%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_libdir}
rm %{buildroot}/%{_lib}/libxcrypt.{so,la}
rm %{buildroot}/%{_lib}/xcrypt/lib*.{so,la}
ln -sf ../../%{_lib}/libxcrypt.so.2 %{buildroot}%{_libdir}/libxcrypt.so

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README NEWS README.bcrypt README.ufc-crypt
/%{_lib}/lib*.so.%{major}*
%dir /%{_lib}/xcrypt
/%{_lib}/xcrypt/lib*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_prefix}/include/*.h
%{_libdir}/lib*.so

