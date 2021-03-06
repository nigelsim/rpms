# $Id$
# Authority: dries
# Upstream: Tels <nospam-abuse$bloodgate,com>

%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define real_name Graph-Easy-As_svg

Summary: Output a Graph::Easy as Scalable Vector Graphics (SVG)
Name: perl-Graph-Easy-As_svg
Version: 0.23
Release: 1%{?dist}
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Graph-Easy-As_svg/

Source: http://www.cpan.org/modules/by-module/Graph/Graph-Easy-As_svg-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl
BuildRequires: perl(Graph::Easy) >= 0.63
BuildRequires: perl(Image::Info) >= 1.28
#BuildRequires: perl(Test::More) >= 0.62

%description
Render Graph-Easy as SVG (Scalable Vector Graphics).

Graphs can be generated by Perl code, or parsed from a simple text format
that is human readable and maintainable.

%prep
%setup -n %{real_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install

### Clean up buildroot
find %{buildroot} -name .packlist -exec %{__rm} {} \;

### Clean up docs
find examples/ -type f -exec %{__chmod} a-x {} \;

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc CHANGES INSTALL LICENSE MANIFEST MANIFEST.SKIP META.yml README SIGNATURE TODO examples/
%doc %{_mandir}/man3/Graph::Easy::As_svg.3pm*
%dir %{perl_vendorlib}/Graph/
%dir %{perl_vendorlib}/Graph/Easy/
#%{perl_vendorlib}/Graph/Easy/As_svg/
%{perl_vendorlib}/Graph/Easy/As_svg.pm

%changelog
* Mon Jun 23 2008 Dag Wieers <dag@wieers.com> - 0.23-1
- Updated to release 0.23.

* Mon May 05 2008 Dag Wieers <dag@wieers.com> - 0.22-1
- Updated to release 0.22.

* Wed Jan 03 2007 Dries Verachtert <dries@ulyssis.org> - 0.21-1
- Updated to release 0.21.

* Mon Sep 18 2006 Dries Verachtert <dries@ulyssis.org> - 0.20-1
- Updated to release 0.20.

* Sun Mar 26 2006 Dries Verachtert <dries@ulyssis.org> - 0.17-1
- Updated to release 0.17.

* Sat Jan  7 2006 Dries Verachtert <dries@ulyssis.org> - 0.16-1
- Updated to release 0.16.

* Sun Dec 25 2005 Dries Verachtert <dries@ulyssis.org> - 0.15-1
- Updated to release 0.15.

* Fri Dec  9 2005 Dries Verachtert <dries@ulyssis.org> - 0.13-1
- Initial package.
