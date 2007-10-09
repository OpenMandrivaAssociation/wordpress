%define _provides_exceptions pear(wp-config.php)
%define _requires_exceptions pear(wp-config.php)

Summary:	WordPress is personal publishing platform
Name:		wordpress
Version:	2.3
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://wordpress.org/
Source0:	ftp://ftp.stu.edu.tw/pub/wordpress/%{name}-%{version}.tar.bz2
Requires(pre):	apache-mod_php php-mysql
Requires:	apache-mod_php php-mysql
BuildArch:	noarch
BuildRequires:	dos2unix
BuildRequires:	apache-base >= 2.0.54
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
WordPress is a state-of-the-art, semantic, personal publishing platform with a
focus on aesthetics, Web standards, and usability. It was born out of a desire
for an elegant, well-architectured personal publishing system, and is the
official successor to b2/cafelog. While primarily geared towards functioning as
a Weblog, it is also a flexible CMS capable of managing many types of Web
sites. In addition to the basic Weblog functions, it also has an integrated
link manager (e.g. for blogrolls), XFN support, support for "static" pages,
Atom and RSS feeds for both content and comments, XML-RPC blogging API support
(Blogger, MetaWeblog, and Movable Type APIs), spam blocking features, advanced
cruft-free URL generation, a flexible theme system, and an advanced plugin API.

%prep

%setup -q -n %{name}

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

# strip away annoying ^M
find -type f | grep -v "\.gif" | grep -v "\.png" | grep -v "\.jpg" | xargs dos2unix -U

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}/var/www/%{name}

cp -aRf * %{buildroot}/var/www/%{name}/

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF

Alias /%{name} /var/www/%{name}

<Directory /var/www/%{name}>
    AllowOverride None
    Allow from All

#    Options FollowSymlinks
#    RewriteEngine On
#    RewriteBase /
#    RewriteCond %{REQUEST_FILENAME} !-f
#    RewriteCond %{REQUEST_FILENAME} !-d
#    RewriteRule . /index.php [L]
		    
</Directory>

EOF

# cleanup
rm -f %{buildroot}/var/www/%{name}/license.txt

%post
%_post_webapp

%postun
%_postun_webapp

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc license.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
/var/www/%{name}
