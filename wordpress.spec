%undefine _debugsource_packages

Summary:	Personal publishing platform
Name:		wordpress
Version:	6.8
Release:	1
License:	GPLv2+
Group:		System/Servers
URL:		https://wordpress.org/
Source0:	http://wordpress.org/%{name}-%{version}.tar.gz
Source1:	README.install.urpmi
Requires:	(apache-mod_php or nginx)
Requires:	php-mysqlnd
BuildArch:	noarch

%description
WordPress is a state-of-the-art, semantic, personal publishing platform with a
focus on aesthetics, Web standards, and usability. It was born out of a desire
for an elegant, well-architectured personal publishing system, and is the
official successor to b2/cafelog. While primarily geared towards functioning
as a Weblog, it is also a flexible CMS capable of managing many types of Web
sites. In addition to the basic Weblog functions, it also has an integrated
link manager (e.g. for blogrolls), XFN support, support for "static" pages,
Atom and RSS feeds for both content and comments, XML-RPC blogging API support
(Blogger, MetaWeblog, and Movable Type APIs), spam blocking features, advanced
cruft-free URL generation, a flexible theme system, and an advanced plugin API.

%prep
%autosetup -p1 -n %{name}
# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

# disable wordpress update option
sed -i -e "s/add_action/#add_action/g" wp-includes/update.php

%build

%install
install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}/srv/www/%{name}

#cp %{SOURCE1} ./README.install.urpmi

cp -aRf * %{buildroot}/srv/www/%{name}/

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF

Alias /%{name} /srv/www/%{name}

<Directory /srv/www/%{name}>
    AllowOverride None
    Require all granted

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
cp %{SOURCE1} ./README.install.urpmi

%files
%doc README.install.urpmi
%doc license.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
/srv/www/%{name}
