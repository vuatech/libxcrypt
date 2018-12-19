%define major 1
%define libname %mklibname crypt %{major}
%define develname %mklibname crypt -d
%define staticname %mklibname crypt -d -s

%global optflags %{optflags} -Ofast -falign-functions=32 -fno-math-errno -fno-trapping-math -fno-strict-aliasing -fuse-ld=bfd
%global ldflags %{optflags} -Ofast -fuse-ld=bfd

Summary:	Crypt Library for DES, MD5, Blowfish and others
Name:		libxcrypt
Version:	4.4.1
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://github.com/besser82/libxcrypt
Source0:	https://github.com/besser82/libxcrypt/archive/%{name}-%{version}.tar.gz
#Patch0:		libxcrypt-4.0.1-strict-aliasing.patch
BuildRequires:	findutils

%description
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, SHA256, SHA512 and passwords with
blowfish encryption.

%package -n %{libname}
Summary:	Crypt Library for DES, MD5, Blowfish and others
Group:		System/Libraries
Obsoletes:	%{mklibname xcrypt 2} < 4.0.0
Provides:	glibc-crypt_blowfish = 1.3
Provides:	eglibc-crypt_blowfish = 1.3

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
Provides:	glibc-crypt_blowfish-devel = 1.3
Provides:	eglibc-crypt_blowfish-devel = 1.3

%description -n %{develname}
This package contains the header files necessary
to develop software using %{name}.

%package -n %{staticname}
Summary:	Static libraries for %{name}
Group:		Development/C
Requires:	%{develname} = %{EVRD}

%description -n %{staticname}
This package contains the static libraries necessary
to develop software using %{name} without requiring
%{name} to be installed on the target system.

%prep
%autosetup -p1

%build
autoreconf -fiv

%configure  \
    --libdir=/%{_lib} \
    --enable-shared \
    --enable-static \
    --enable-obsolete-api \
    --enable-weak-hashes || (cat config.log && die)

%make_build

%install
%make_install
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
mv %{buildroot}/%{_lib}/pkgconfig/*.pc %{buildroot}%{_libdir}/pkgconfig/
mv %{buildroot}/%{_lib}/*.a %{buildroot}%{_libdir}/

# We do not need libowcrypt.*, since it is a SUSE
# compat thing.  Software needing it to be build can
# be patched easily to just link against '-lcrypt'.
find %{buildroot} -name 'libow*' -print -delete

%check
# Make sure the symbol versioning script worked
if ! nm $(ls .libs/libcrypt.so.%{major}* |head -n1) |grep -q 'crypt_r@GLIBC_2'; then
	echo "Symbol versioning script seems to have messed up"
	echo "Make sure this is fixed unless you want to break pam."
	echo "You may want to try a different ld."
	exit 1
fi

%files -n %{libname}
/%{_lib}/lib*.so.%{major}*

%files -n %{develname}
%doc AUTHORS NEWS README.md
%{_includedir}/*.h
/%{_lib}/libcrypt.so
/%{_lib}/libxcrypt.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/crypt*.3*
%{_mandir}/man5/crypt.5*

%files -n %{staticname}
%{_libdir}/libcrypt.a
%{_libdir}/libxcrypt.a
