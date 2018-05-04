%define major 1
%define libname %mklibname crypt %{major}
%define develname %mklibname crypt -d

%global optflags %{optflags} -Ofast -falign-functions=32 -fno-math-errno -fno-trapping-math

Summary:	Crypt Library for DES, MD5, Blowfish and others
Name:		libxcrypt
Version:	4.0.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/besser82/libxcrypt
Source0:	https://github.com/besser82/libxcrypt/archive/%{name}-%{version}.tar.gz

%description
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, SHA256, SHA512 and passwords with
blowfish encryption.

%package -n %{libname}
Summary:	Crypt Library for DES, MD5, Blowfish and others
Group:		System/Libraries
Obsoletes:	%{mklibname xcrypt 2} < 4.0.0

%description -n %{libname}
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, SHA256, SHA512 and passwords with
blowfish encryption.

%package -n %{develname}
Summary:	Development libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name} = %{EVRD}
Obsoletes:	%{mklibname xcrypt -d} < 4.0.0

%description -n %{develname}
This package contains the header files and static libraries necessary
to develop software using %{name}.

%prep
%setup -q
%apply_patches

%build
autoreconf -fiv

%configure  \
	--libdir=/%{_lib}

%make

%install
%makeinstall_std

%files -n %{libname}
/%{_lib}/lib*.so.%{major}*

%files -n %{develname}
%doc README NEWS README.bcrypt README.ufc-crypt
%{_prefix}/include/*.h
%{_libdir}/lib*.so
