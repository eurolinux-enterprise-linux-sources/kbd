Name:           kbd
Version:        1.15
Release:        11%{?dist}
Summary:        Tools for configuring the console (keyboard, virtual terminals, etc.)

Group:          System Environment/Base
License:        GPLv2+
URL:            http://ftp.altlinux.org/pub/people/legion/kbd
Source0:        http://ftp.altlinux.org/pub/people/legion/kbd/kbd-%{version}.tar.gz
Source1:        kbd-latsun-fonts.tar.bz2
Source2:        ro_maps.tar.bz2
Source3:        kbd-latarcyrheb-16-fixed.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:         kbd-1.15-po.patch
Patch1:         kbd-1.15-keycodes-man.patch
Patch2:         kbd-1.15-sparc.patch
Patch3:         kbd-1.15-unicode_start.patch
Patch4:         kbd-1.15-resizecon-x86_64.patch
Patch5:         kbd-1.15-quiet_doc.patch
Patch6:         kbd-1.15-defkeymap.patch

BuildRequires:  bison, flex, gettext
Conflicts:      util-linux < 2.11r-9
Requires:       initscripts >= 5.86-1
Requires:       %{name}-misc = %{version}-%{release}

%description
The %{name} package contains tools for managing a Linux
system's console's behavior, including the keyboard, the screen
fonts, the virtual terminals and font files.

%package misc
Summary:        Data for kbd package
BuildArch:      noarch

%description misc
The %{name}-misc package contains data for kbd package - console fonts,
keymaps etc. Please note that %{name}-misc is not helpful without kbd.

%prep
%setup -q -a 1 -a 2 -a 3
%patch0 -p1 -b .po
%patch1 -p1 -b .keycodes-man
%patch2 -p1 -b .sparc
%patch3 -p1 -b .unicode_start
%patch4 -p1 -b .resizecon_x86_64
%patch5 -p1 -b .quiet_doc
%patch6 -p1 -b .defkeymap

# 7-bit maps are obsolete; so are non-euro maps
pushd data/keymaps/i386
mv qwerty/fi.map qwerty/fi-old.map
cp qwerty/fi-latin9.map qwerty/fi.map
cp qwerty/pt-latin9.map qwerty/pt.map
cp qwerty/sv-latin1.map qwerty/se-latin1.map

mv azerty/fr.map azerty/fr-old.map
cp azerty/fr-latin9.map azerty/fr.map

cp azerty/fr-latin9.map azerty/fr-latin0.map # legacy alias

# Rename conflicting keymaps
mv dvorak/no.map dvorak/no-dvorak.map
mv fgGIod/trf.map fgGIod/trf-fgGIod.map
mv olpc/es.map olpc/es-olpc.map
mv olpc/pt.map olpc/pt-olpc.map
mv qwerty/cz.map qwerty/cz-qwerty.map
popd

# Convert to utf-8
iconv -f iso-8859-1 -t utf-8 < "ChangeLog" > "ChangeLog_"
mv "ChangeLog_" "ChangeLog"

%build
%configure --prefix=%{_prefix} --datadir=/lib/kbd --mandir=%{_mandir} --localedir=%{_datadir}/locale --enable-nls
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# ro_win.map.gz is useless
rm -f $RPM_BUILD_ROOT/lib/kbd/keymaps/i386/qwerty/ro_win.map.gz

# Create additional name for Serbian latin keyboard
ln -s sr-cy.map.gz $RPM_BUILD_ROOT/lib/kbd/keymaps/i386/qwerty/sr-latin.map.gz

# The rhpl keyboard layout table is indexed by kbd layout names, so we need a
# Korean keyboard
ln -s us.map.gz $RPM_BUILD_ROOT/lib/kbd/keymaps/i386/qwerty/ko.map.gz

# Move binaries which we use before /usr is mounted from %{_bindir} to /bin.
mkdir -p $RPM_BUILD_ROOT/bin
for binary in setfont dumpkeys kbd_mode unicode_start unicode_stop loadkeys ; do
  mv $RPM_BUILD_ROOT%{_bindir}/$binary $RPM_BUILD_ROOT/bin/
done

# Some microoptimization
sed -i -e 's,\<kbd_mode\>,/bin/kbd_mode,g;s,\<setfont\>,/bin/setfont,g' \
        $RPM_BUILD_ROOT/bin/unicode_start

# Link open to openvt
ln -s openvt $RPM_BUILD_ROOT%{_bindir}/open

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog AUTHORS README COPYING doc/kbd.FAQ*.html doc/font-formats/*.html doc/utf/utf* doc/dvorak/*
/bin/*
%{_bindir}/*
%{_mandir}/*/*

%files misc
%defattr(-,root,root,-)
/lib/kbd

%changelog
* Tue Jun 22 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-11
- Ship /lib/kbd in separate subpackage

* Mon Jun  7 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-10
- Fix name referring to default keymap

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.15-9.1
- Rebuilt for RHEL 6

* Wed Aug 26 2009 Karsten Hopp <karsten@redhat.com> 1.15-9
- drop excludearch s390x, we need this package to be able to build other packages on s390x

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar  5 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-7
- Add loadkeys 'q' option to loadkeys manpage and --help
  Resolves: #487538

* Mon Mar  2 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-6
- Remove static loadkeys binary (it's not needed anymore)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  6 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-4
- Merge review (drop Provides/Obsoletes, change Prereq to Requires,
  add URL, convert ChangeLog to utf-8, replace locale destination
  with macro, add COPYING and add dvorak documentation)
  Resolves: #225958

* Thu Jan 29 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-3
- Rename conflicting keymaps to have unique names
  Resolves: #481674

* Mon Jan 12 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-2
- Move loadkeys to /bin

* Thu Jan  8 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.15-1
- Update to kbd-1.15

* Mon Sep  8 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-32
- Rediff all patches to work with patch --fuzz=0
- Add static loadkeys
  Related: #451672

* Tue Feb 26 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-31
- Fix trq.map
  Resolves: #216710

* Fri Feb 22 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-30
- Rebuild fo GCC 4.3

* Tue Nov 27 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-29
- Stop kbdrate using consolehelper
  Resolves: #393231

* Thu Nov 15 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-28
- Fix ro.map.gz, add ro_std.map.gz, drop ro_win.map.gz,
  add Lat2-Terminus16.psf console font (many thanks to Alexandru Szasz
  <alexxed@gmail.com>)
  Resolves: #253892

* Wed Oct 17 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-27
- Add resizecons (with man page) for x86_64
  Resolves: #333651

* Mon Oct 15 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-26
- Fix ro.map to generate right unicode for s, S, t, T with comma
- Fix LatArCyrHeb-16 unicode mapping table to show comma-version
  of s, S, t, T and cedilla-version of s, S, t, T as the same glyph
  (because there is no font in kbd for comma-version)
  Resolves: #329071

* Tue Sep 18 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-25
- Add new romanian keymap
  Resolves: #253892

* Mon Aug 27 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-24
- Fix license
- Symlink sr-cy layout to sr-latin
  Resolves: #253957

* Tue Jul  3 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-23
- Rebuild

* Tue Jul  3 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.12-22
- Fix sun12x22 font missing unicode mapping table
  Resolves: #244628

* Tue Jan  9 2007 Miloslav Trmac <mitr@redhat.com> - 1.12-21
- Add a "ko" (Korean) keyboard layout, equivalent to the "us" layout
  Resolves: #220151

* Thu Dec  7 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-20
- Document that setkeycodes doesn't affect USB keyboards and that the kernel
  doesn't provide the raw scan codes by default
  Resolves: #211803

* Tue Oct 31 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-19
- Ship "el" translation instead of the obsolete "gr" translation
  Resolves: #210749
- Fix %% quoting in %%changelog

* Fri Sep 29 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-18
- Add a missing tilde to U+00E3 in latarcyrheb-sun16.psfu (#204470)

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 1.12-17
- Obsoletes/Provides open
- Create a symlink from open to openvt

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.12-16.1
- rebuild

* Sun Jul  9 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-16
- Don't include <asm/kbdio.h> on SPARC (#198040, patch by Dennis Gilmore
  <dennis@ausil.us>)

* Mon May 29 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-15
- Fix missing BuildRequires (#193406)

* Mon Mar 27 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-14
- Don't install resizecons.8 on non-x86 (#186877, patch by Keiichi Mori
  <kmori@redhat.com>)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.12-13.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.12-13.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 20 2006 Miloslav Trmac <mitr@redhat.com> - 1.12-13
- Fix build with new coreutils
- Hardcode paths in unicode_start to avoid a few file lookups (#178329)
- Drop unnecessary Prereq: sed mktemp

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-12
- Don't reload the keymap in unicode_start (#172425)

* Fri Nov 11 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-11
- Don't ship character set lists (they are already in glibc-common) and an
  obsolete copy of kbd.FAQ

* Fri May 20 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-10
- Don't attempt to open directories as source files (#141634, original patch by
  Paul Nasrat)

* Tue May 17 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-9
- Fix another violation of C aliasing rules (#157720, patch by Jan Kratochvil)

* Sat Mar 12 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-8
- Fix violation of C aliasing rules (#150440)

* Sun Mar  6 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-7
- Don't run ldconfig
- Don't strip executables

* Fri Mar  4 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-6
- Rebuild with gcc4

* Sun Feb 20 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-5
- Put "Meta_acute" back in German keymaps, just ignore it in (loadkeys -u)
  (patch by Jochen Schmitt)
- Don't ship patch backup files, simpler way

* Sat Feb 19 2005 Miloslav Trmac <mitr@redhat.com> - 1.12-4
- Don't ship a patch backup file
- Mention in setfont.8 that 512-glyph fonts reduce the number of available
  colors (#140935, patch by Dmitry Butskoj)
- Remove "Meta_acute" from German keymaps (#143124)
- Make the %%triggerun script condition more precise, ignore failure of the
  script

* Mon Feb 14 2005 Adrian Havill <havill@redhat.com>
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Adrian Havill <havill@redhat.com>
- update to 1.12

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 14 2004 Bill Nottingham <notting@redhat.com> 1.08-12
- remove speakup patch at request of author

* Wed Jan 14 2004 Bill Nottingham <notting@redhat.com> 1.08-12
- remove speakup patch at request of author

* Fri Oct 10 2003 Bill Nottingham <notting@redhat.com> 1.08-11
- remove keytable init script (#106783)

* Tue Aug 12 2003 Adrian Havill <havill@rtedhat.com> 1.08-10.1
- bump for RHEL

* Tue Aug 12 2003 Adrian Havill <havill@rtedhat.com> 1.08-10
- apply the rukbd patch (#78218)

* Thu Jul 31 2003 Adrian Havill <havill@redhat.com> 1.08-9
- don't print "plus before..." warnings about non-supported capslock
  in unimode <Andries.Brouwer@cwi.nl> (#81855)

* Wed Jul 30 2003 Adrian Havill <havill@redhat.com> 1.08-8
- replaced Russian keyboard map with working UTF-8 equivalent (#79338)

* Thu Jul 24 2003 Adrian Havill <havill@redhat.com> 1.08-7
- make euro/latin-9 the default instead of latin-1 and 7-bit (#97013)
- fix swedish keymap; se, not sv (#88791)
- add fr-latin0 legacy alias of fr-latin-9 (#88324)
- add ".map" ext to filename param of init script (#90562)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 06 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- build new rpm

* Fri Feb 21 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- ExcludeArch mainframe

* Thu Jan 30 2003 Bill Nottingham <notting@redhat.com> 1.08-4
- remove condrestart from initscript

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec  6 2002 Nalin Dahyabhai <nalin@redhat.com> 1.08-2
- only output terminal unicode init sequence if both stdout and stderr are
  connected to terminals, so that it doesn't show up when script outputs
  get piped to files

* Fri Nov 22 2002 Nalin Dahyabhai <nalin@redhat.com> 1.08-1
- update to 1.08
- drop updates which went mainline

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.06-27
- add detached signature
- remove directory names from PAM configuration so that the same config file
  can be used for any arch on multilib systems

* Wed Sep  4 2002 Bill Nottingham <notting@redhat.com> 1.06-26
- don't munge /etc/sysconfig/i18n

* Tue Sep  3 2002 Bill Nottingham <notting@redhat.com> 1.06-25
- don't run setsysfont in upgrade trigger on console-tools

* Thu Aug 29 2002 Jakub Jelinek <jakub@redhat.com> 1.06-24
- use cyr-sun16 cyrillic chars in latarcyrheb-sun16 font
  instead of old LatArCyrHeb-16 chars
- add Euro character to latarcyrheb-sun16
- use latarcyrheb-sun16 by default in unicode_start script

* Tue Aug 27 2002 Jakub Jelinek <jakub@redhat.com> 1.06-23
- add back lat[02]-sun16 fonts plus latarcyrheb-sun16 font

* Thu Aug 22 2002 Karsten Hopp <karsten@redhat.de>
- needs to conflict with older util-linux packages
  (kbdrate moved between packages)

* Tue Aug 13 2002 Bill Nottingham <notting@redhat.com> 1.06-21
- remove Evil Hack in favor of slightly-less-evil-hack in initscripts

* Tue Jul  9 2002 Bill Nottingham <notting@redhat.com> 1.06-20
- fix speakup keymap names

* Tue Jul 09 2002 Phil Knirsch <pknirsch@redhat.com> 1.06-19
- Evil hack to make setfont work correctly on all consoles (#68018)

* Thu Jun 27 2002 Bill Nottingham <notting@redhat.com> 1.06-18
- move unicode_stop to /bin too
- fix path to loadkeys in keytable.init
- add in speakup keymaps

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.06-16
- fix incorrect path in console.apps configuration file

* Thu May 30 2002 Bill Nottingham <notting@redhat.com> 1.06-14
- move some more stuff to /bin (unicode_start and dependencies)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Feb 25 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-12
- Rebuild in new environment

* Wed Jan 30 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-11
- Oops, actually list the pam files in %%files

* Tue Jan 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-10
- Add and consolehelper'ify kbdrate

* Tue Jan 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-9
- Re-remove kbdrate

* Thu Jan 24 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-7
- Fix build in current environment
- Get rid of kbdrate, it's in util-linux these days

* Wed Jul 18 2001 Matt Wilson <msw@redhat.com>
- added a patch (Patch4) that allows --tty= in setfont
- modified patch not to break translations

* Tue Jul  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-4
- Add cyrillic patches from leon@geon.donetsk.ua (#47144)

* Tue Jun 26 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-3
- Fix "Alt+AltGr=Compose" in qwertz-keyboards

* Mon Jun 25 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-2
- Fix "make install" and init script (#45327)

* Sat Jun 16 2001 Than Ngo <than@redhat.com>
- update to 1.0.6
- use %%{_tmppath}
- use find_lang
- support new gettext
- remove some patch files, which are included in 1.0.6
- fix to use RPM_OPT_FLAGS

* Thu May  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.05-3
- Fix up resizecons

* Wed May  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.05-2
- Build everything, obsoletes console-tools
- s/Copyright:/License:/
- License is GPL, not just distributable
- Add our compose mappings from old console-tools
- Add triggerpostun -- console-tools magic to get sane fonts and mappings

* Tue Apr 17 2001 Erik Troan <ewt@redhat.com>
- initial packaging for kbdrate
