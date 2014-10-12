# $Id$
# Authority: dag

Summary: Lightweight, non-caching, optionally anonymizing HTTP proxy
Name: tinyproxy
Version: 1.8.2
Release: 2%{?dist}
License: GPL
Group: System Environment/Daemons
URL: http://tinyproxy.sourceforge.net/

Source: https://banu.com/pub/tinyproxy/1.8/tinyproxy-%{version}.tar.bz2
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: asciidoc

%description
tinyproxy is an anonymizing http proxy which is very light on system
resources, ideal for smaller networks and similar situations where
other proxies (such as Squid) may be overkill and/or a security risk.

tinyproxy can also be configured to anonymize http requests (allowing
for exceptions on a per-header basis).

%prep
%setup

%{__cat} <<EOF >tinyproxy.sysconfig
OPTIONS="-c %{_sysconfdir}/tinyproxy/tinyproxy.conf"
EOF

%{__cat} <<'EOF' >tinyproxy.sysv
#!/bin/bash
#
# Initfile for Tinyproxy daemon
#
# chkconfig: 345 90 25
# description: A small, efficient HTTP/SSL proxy daemon.
#
# processname: tinyproxy
# config: /etc/tinyproxy/tinyproxy.conf
# pidfile: /var/run/tinyproxy/tinyproxy.pid

# Source function library.
source /etc/rc.d/init.d/functions

# Source networking configuration.
source /etc/sysconfig/network

# Check that networking is up.
[ "${NETWORKING}" = "no" ] && exit 0

[ -f %{_sysconfdir}/tinyproxy/tinyproxy.conf ] || exit 0

DAEMON="%{_sbindir}/tinyproxy"
OPTIONS=
NAME=tinyproxy
DESC=tinyproxy

if [ -r /etc/sysconfig/tinyproxy ]; then
    . /etc/sysconfig/tinyproxy
fi

test -f $DAEMON || exit 0


case "$1" in
  start)
    echo -n "Starting $DESC: "
    daemon $DAEMON $OPTIONS
    RETVAL=$?
    echo
    [ $RETVAL -eq 0 ] && touch /var/lock/subsys/$NAME
    ;;
  stop)
    echo -n "Stopping $DESC: "
    killproc $DAEMON
    RETVAL=$?
    echo
    [ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/$NAME
    ;;
  reload|force-reload)
    echo -n "Reloading $DESC configuration files."
    killproc $DAEMON -HUP
    echo
    ;;
  status)
    status $DAEMON
    ;;
  restart)
    echo -n "Restarting $DESC: "
    echo
    $0 stop
    $0 start
    RETVAL=$?
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|reload|force-reload|status}"
    exit 1
    ;;
esac

exit $RETVAL
EOF

%build
%configure \
    --program-prefix="%{?_program_prefix}" \
    --enable-filter \
    --enable-tunnel \
    --enable-upstream \
    --enable-xtinyproxy \
    --with-config="%{_sysconfdir}/tinyproxy"  \
    --with-stathost="localhost"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/tinyproxy/
%{__make} install DESTDIR="%{buildroot}"

touch %{buildroot}%{_sysconfdir}/tinyproxy/filter

%{__install} -Dp -m0755 tinyproxy.sysv %{buildroot}%{_initrddir}/tinyproxy
%{__install} -Dp -m0644 tinyproxy.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/tinyproxy

%{__install} -d -m0755 %{buildroot}%{_localstatedir}/log/tinyproxy/
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/run/tinyproxy/

### Clean up buildroot
%{__rm} -f %{buildroot}%{_sysconfdir}/tinyproxy-dist

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/chkconfig --add tinyproxy

%preun
if [ $1 -eq 0 ]; then
    /sbin/service tinyproxy stop &>/dev/null || :
    /sbin/chkconfig --del tinyproxy
fi

%postun
/sbin/service tinyproxy condrestart &>/dev/null || :

%files
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%doc docs/*.txt
%doc %{_mandir}/man5/tinyproxy.conf.5*
%doc %{_mandir}/man8/tinyproxy.8*
%config(noreplace) %{_sysconfdir}/tinyproxy.conf
%config(noreplace) %{_sysconfdir}/tinyproxy/
%config(noreplace) %{_sysconfdir}/sysconfig/tinyproxy
%config %{_initrddir}/tinyproxy
%{_sbindir}/tinyproxy
%{_datadir}/tinyproxy/
%defattr(-, nobody, nobody, 0700) 
%dir %{_localstatedir}/log/tinyproxy/
%dir %{_localstatedir}/run/tinyproxy/

%changelog
* Sun Oct 12 2014 Nigel Sim <nigel.sim@gmail.com> - 1.8.2-2
- Fixed init script
- Create log and run directories

* Thu Oct 21 2010 Dag Wieers <dag@wieers.com> - 1.8.2-1
- Fixed initscript. (Johan Huysmans)

* Tue Mar 23 2010 Dag Wieers <dag@wieers.com> - 1.6.5-1
- Updated to release 1.6.5.

* Mon Feb 25 2008 Dag Wieers <dag@wieers.com> - 1.6.3-1
- Initial package. (using DAR)
