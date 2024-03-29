Summary: A PostgreSQL-based DNS server
Name: mydns-postgres
Version: 1.2.8.31
Release: 1
Copyright: GPL
Group: System Environment/Daemons
Prereq: /sbin/chkconfig /etc/init.d /sbin/service
URL: http://mydns.bboy.net/
Source: %{url}/download/%{name}-%{version}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-root
Packager: Don Moore <bboy@bboy.net>

%description
A nameserver that serves records directly from your
PostgreSQL database.

%prep
%setup -q  

%build
%configure --without-mysql --with-pgsql --enable-static-build
make

%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}/etc/rc.d/init.d
install -c -m 755 contrib/mydns.redhat ${RPM_BUILD_ROOT}/etc/rc.d/init.d/mydns

mkdir -p ${RPM_BUILD_ROOT}/etc
src/mydns/mydns --dump-config > mydns.conf
install -m 644 mydns.conf $RPM_BUILD_ROOT/etc/mydns.conf

mkdir -p ${RPM_BUILD_ROOT}/usr/share/mydns
install -m 644 contrib/admin.php $RPM_BUILD_ROOT/usr/share/mydns/

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
install -c -s src/mydns/mydns ${RPM_BUILD_ROOT}%{_sbindir}/
install -c -s src/util/mydnscheck ${RPM_BUILD_ROOT}%{_sbindir}/
install -c -s src/util/mydnsexport ${RPM_BUILD_ROOT}%{_sbindir}/
install -c -s src/util/mydnsimport ${RPM_BUILD_ROOT}%{_sbindir}/
install -c -s src/util/mydnsptrconvert ${RPM_BUILD_ROOT}%{_sbindir}/
install -c -s src/util/mydns-conf ${RPM_BUILD_ROOT}%{_sbindir}/

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
install -c doc/mydns.conf.5 ${RPM_BUILD_ROOT}%{_mandir}/man5/

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
install -c doc/mydns.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/
install -c doc/mydnscheck.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/
install -c doc/mydnsexport.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/
install -c doc/mydnsimport.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/
install -c doc/mydns-conf.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/

mkdir -p ${RPM_BUILD_ROOT}%{_infodir}
install -c doc/mydns.info ${RPM_BUILD_ROOT}%{_infodir}


%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 = 1 ]; then
	/sbin/chkconfig --add mydns
fi

%preun
if [ $1 = 0 ]; then
	/sbin/chkconfig --del mydns
fi

%postun
if [ $1 -ge 1 ]; then
	/sbin/service mydns condrestart >/dev/null 2>&1
fi


%files
%defattr(-,root,root)
%{_sbindir}/mydns
%{_sbindir}/mydnscheck
%{_sbindir}/mydnsexport
%{_sbindir}/mydnsimport
%{_sbindir}/mydnsptrconvert
%{_sbindir}/mydns-conf
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_infodir}/mydns.info.gz
%doc AUTHORS ChangeLog COPYING NEWS QUICKSTART.postgres README TODO
%config(noreplace) /etc/mydns.conf
%config /etc/rc.d/init.d/mydns
/usr/share/mydns/admin.php

%changelog
* Thu Mar 27 2003 Don Moore <bboy@bboy.net>
- now installs startup scripts

* Fri Jul 12 2002 Don Moore <bboy@bboy.net>
- initial public release
