Summary: nethserver-zabbix sets up the monitoring system
%define name nethserver-zabbix
Name: %{name}
%define version 0.0.1
%define release 8
Version: %{version}
Release: %{release}%{?dist}
License: GPL
Group: Networking/Daemons
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-buildroot
#Requires: zabbix-web-pgsql-scl
Requires: nethserver-postgresql,zabbix-server-pgsql,zabbix-agent,zabbix-web,net-snmp-utils,nethserver-net-snmp,php-pgsql,nethserver-rh-php73-php-fpm
Requires: nmap
Conflicts: nethserver-zabbix22
BuildRequires: nethserver-devtools
BuildArch: noarch

%description
NethServer Zabbix configuration

%changelog
* Mon May 18 2020 Markus Neuberger <info@markusneuberger.at> - 0.0.1-8
- Add support for Zabbix 5 LTS - thanks to dz00te
* Mon Mar 23 2020 Markus Neuberger <info@markusneuberger.at> - 0.0.1-7
- Add new images - thanks to Andy Wismer
- Add Zabbix application to cockpit
- New zabbix DBs are created with unicode
- Add script zabbixUnicode to migrate old db to unicode
- Add HTTPS redirect
* Thu Mar 08 2018 Markus Neuberger <info@markusneuberger.at> - 0.0.1-6
- Add backup-config - thanks to Andy Wismer
- Add backup-data - thanks to Andy Wismer
- Add zabbix postgresql db backup/restore - thanks to Andy Wismer
* Sun Feb 25 2018 Markus Neuberger <info@markusneuberger.at> - 0.0.1-5
- Added nice map images - thanks to Andy Wismer
- Added backup script - thanks to Emiliano Vavassori
* Mon Jan 29 2018 Markus Neuberger <info@markusneuberger.at> - 0.0.1-4
- Change from mysql to postgresql - thanks to Emiliano Vavassori
- Integrating zabbix service - thanks to Emiliano Vavassori
- Adding SNMP support and MIBs - thanks to Emiliano Vavassori
* Sat Jan 27 2018 Markus Neuberger <info@markusneuberger.at> - 0.0.1-3
- Changed versioning
* Sat Dec 09 2017 Markus Neuberger <info@markusneuberger.at> - 0.0.1-2
- Added automatic initial config
* Mon Dec 04 2017 Markus Neuberger <info@markusneuberger.at> - 0.0.1-1
- Initial NS7 release
- Added conflicts nethserver-zabbix22

#%pre
#getent passwd zabbix >/dev/null || useradd -m -d /var/lib/zabbix -s /bin/bash zabbix
#exit 0

%prep
%setup

%build
perl createlinks
mkdir -p root/var/lib/nethserver/zabbix/backup

%install
rm -rf $RPM_BUILD_ROOT
(cd root; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-%{release}-filelist

mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/%{name}/

cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/
cp -a ui/* %{buildroot}/usr/share/cockpit/%{name}/

%{genfilelist} $RPM_BUILD_ROOT \
  --file /etc/sudoers.d/50_nsapi_nethserver_zabbix 'attr(0440,root,root)' \
  --file /usr/libexec/nethserver/api/%{name}/read 'attr(775,root,root)' \
  --file /usr/local/bin/zabbixUnicode.sh 'attr(770,root,root)' \
  --file /usr/local/bin/nethbackup_check 'attr(770,root,root)' \
  --dir /var/lib/nethserver/zabbix/backup 'attr(755,postgres,postgres)' \
> %{name}-%{version}-%{release}-filelist
exit 0

%post
%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update
%doc COPYING
