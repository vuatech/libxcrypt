%define major 2
%define libname %mklibname xcrypt %{major}
%define develname %mklibname xcrypt -d

%global optflags %{optflags} -Ofast -falign-functions=32 -fno-math-errno -fno-trapping-math

Summary:	Crypt Library for DES, MD5, Blowfish and others
Name:		libxcrypt
Version:	4.0.0
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/besser82/libxcrypt
Source0:	https://github.com/besser82/libxcrypt/archive/%{name}-%{version}.tar.gz
Patch0:		libxcrypt-3.1.1-clang.patch 
Patch1:		libxcrypt-3.1.1-dl-linkage.patch

%description
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, SHA256, SHA512 and passwords with
blowfish encryption.

%package -n %{libname}
Summary:	Crypt Library for DES, MD5, Blowfish and others
Group:		System/Libraries

%description -n %{libname}
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, SHA256, SHA512 and passwords with
blowfish encryption.

%package -n %{develname}
Summary:	Development libraries for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name} = %{EVRD}

%description -n %{develname}
This package contains the header files and static libraries necessary
to develop software using %{name}.

%prep
%setup -q
%apply_patches

%build
./bootstrap.sh

%configure  \
	--enable-Wno-cast-align \
	--enable-Wno-null-pointer-arithmetic \
	--libdir=/%{_lib}

%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_libdir}
rm %{buildroot}/%{_lib}/libxcrypt.so
rm %{buildroot}/%{_lib}/xcrypt/lib*.so
ln -sf ../../%{_lib}/libxcrypt.so.2 %{buildroot}%{_libdir}/libxcrypt.so

%files -n %{libname}
/%{_lib}/lib*.so.%{major}*
%dir /%{_lib}/xcrypt
/%{_lib}/xcrypt/lib*.so.*

%files -n %{develname}
%doc README NEWS README.bcrypt README.ufc-crypt
%{_prefix}/include/*.h
%{_libdir}/lib*.so
