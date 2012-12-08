%define snap r142

#Module-Specific definitions
%define mod_name mod_proxy_html
%define mod_conf A28_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	3.1.2
Release:	%mkrel 0.%{snap}.7
Group:		System/Servers
License:	GPL
URL:		http://apache.webthing.com/mod_proxy_html/
Source0:	mod_proxy_html-%{version}-%{snap}.tar.gz
Source1:	http://apache.webthing.com/mod_proxy_html/config.html
Source2:	http://apache.webthing.com/mod_proxy_html/guide.html
Source3:	http://apache.webthing.com/mod_proxy_html/faq.html
Source4:	%{mod_conf}
BuildRequires:	libxml2-devel
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires(pre):	apache-mod_proxy >= 2.2.0
Requires(pre):	apache-mod_ssl >= 2.2.0
Requires(pre):	apache-mod_xml2enc >= 1.0.3
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Requires:	apache-mod_proxy >= 2.2.0
Requires:	apache-mod_ssl >= 2.2.0
Requires:	apache-mod_xml2enc >= 1.0.3
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	apache-mod_xml2enc-devel >= 1.0.3
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_proxy_html is an output filter to rewrite HTML links in a proxy situation,
to ensure that links work for users outside the proxy. It serves the same
purpose as Apache's ProxyPassReverse directive does for HTTP headers, and is an
essential component of a reverse proxy.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .
cp %{SOURCE4} %{mod_conf}

# use correct name and version
perl -pi -e "s|^#define VERSION_STRING .*|#define VERSION_STRING \"%{mod_name}/%{version}\"|g" %{mod_name}.c

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

head -36 mod_proxy_html.c > README.mod_proxy_html

%build
%{_bindir}/apxs `xml2-config --cflags` `xml2-config --libs` %{ldflags} -c %{mod_name}.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc config.html guide.html faq.html proxy_html.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 3.1.2-0.r142.5mdv2011.0
+ Revision: 674430
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 3.1.2-0.r142.4
+ Revision: 662777
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 3.1.2-0.r142.3mdv2011.0
+ Revision: 588284
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 3.1.2-0.r142.2mdv2010.1
+ Revision: 515839
- rebuilt for apache-2.2.15

* Sun Dec 27 2009 Oden Eriksson <oeriksson@mandriva.com> 3.1.2-0.r142.1mdv2010.1
+ Revision: 482866
- fix a silly mistake
- 3.1.2 (r142)
- use another example: http://localhost/store/

* Mon Nov 30 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-0.r123.5mdv2010.1
+ Revision: 471957
- fix #55255 (mod_proxy fails to install correctly and breaks apache)

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-0.r123.4mdv2010.0
+ Revision: 451702
- rebuild

* Fri Jul 31 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-0.r123.3mdv2010.0
+ Revision: 405140
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-0.r123.2mdv2009.1
+ Revision: 326621
- fix build with -Wformat-security
- use %%ldflags
- rebuild

* Sun Aug 10 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.1-0.r123.1mdv2009.0
+ Revision: 270191
- 3.0.1 (r123)

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-0.r122.6mdv2009.0
+ Revision: 235643
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-0.r122.5mdv2009.0
+ Revision: 215294
- rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-0.r122.4mdv2008.1
+ Revision: 181442
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-0.r122.3mdv2008.1
+ Revision: 180212
- make the default example work since the ssl move on qa.mandriva.com

* Mon Feb 18 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-0.r122.2mdv2008.1
+ Revision: 171594
- make the example work again (http://localhost/qa/ -> http://qa.mandriva.com/)

* Mon Feb 18 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-0.r122.1mdv2008.1
+ Revision: 171487
- new svn snap (r122)

  + Thierry Vignaud <tv@mandriva.org>
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Oct 13 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0-0.r95.1mdv2008.1
+ Revision: 97977
- new snap (r95)

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0-0.r93.1mdv2008.0
+ Revision: 82353
- new snap (r93)

* Tue Jul 17 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0-0.r90.1mdv2008.0
+ Revision: 52991
- 3.0-r90


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.5.2-4mdv2007.1
+ Revision: 140728
- rebuild

* Thu Feb 22 2007 Oden Eriksson <oeriksson@mandriva.com> 2.5.2-3mdv2007.1
+ Revision: 124419
- tag it with the correct name and version
- provide a working example in the configuration

* Fri Jan 26 2007 Oden Eriksson <oeriksson@mandriva.com> 2.5.2-2mdv2007.1
+ Revision: 114228
- fix missing -T in the setup section, duh...
- nuke the A28_mod_proxy_html.conf.bz2 file
- bunzip all sources
- new mod_proxy_html.c, same version

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 2.5.2-1mdv2007.1
+ Revision: 79479
- Import apache-mod_proxy_html

* Tue Jul 18 2006 Oden Eriksson <oeriksson@mandriva.com> 2.5.2-1mdv2007.0
- 2.5.2

* Wed Dec 14 2005 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-2mdk
- rebuilt against apache-2.2.0

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-1mdk
- 2.5.1
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.4.3-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.4.3-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.4.3-4mdk
- use the %%mkrel 1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.4.3-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.4.3-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Mon Feb 14 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.4.3-1mdk
- 2.4.3

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.4-1mdk
- rebuilt for apache 2.0.53

* Thu Nov 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_2.4-1mdk
- initial mandrake package

