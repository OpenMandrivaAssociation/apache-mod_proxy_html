%define snap r122

#Module-Specific definitions
%define mod_name mod_proxy_html
%define mod_conf A28_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	3.0
Release:	%mkrel 0.%{snap}.5
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
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Requires:	apache-mod_proxy >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
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
%{_sbindir}/apxs `xml2-config --libs` `xml2-config --cflags` -c %{mod_name}.c

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
