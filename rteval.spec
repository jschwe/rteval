%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_ver: %define python_ver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:		rteval
Version:	3.0
Release:	1%{?dist}
Summary:	Utility to evaluate system suitability for RT Linux

Group:		Development/Tools
License:	GPLv2
URL:		https://git.kernel.org/pub/scm/utils/rteval/rteval.git
Source0:	rteval-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	python3-devel
Requires:	platform-python
Requires:	python3-schedutils python3-ethtool python3-lxml
Requires:	python3-dmidecode >= 3.10
Requires:	rt-tests >= 0.97
Requires:	rteval-loads >= 1.4
Requires:	rteval-common => %{version}-%{release}
Requires:	sysstat
Requires:	bzip2
Requires:       kernel-headers
Requires:       sos
BuildArch:	noarch
Obsoletes:	rteval <= 1.7
Requires:	numactl

%description
The rteval script is a utility for measuring various aspects of
realtime behavior on a system under load. The script unpacks the
kernel source, and then goes into a loop, running hackbench and
compiling a kernel tree. During that loop the cyclictest program
is run to measure event response time. After the run time completes,
a statistical analysis of the event response times is done and printed
to the screen.


%package common
Summary: Common rteval files
BuildArch: noarch

%description common
Common files used by rteval, rteval-xmlrpc and rteval-parser

%prep
%setup -q

# version sanity check (make sure specfile and rteval.py match)
cp rteval/version.py rtevalversion.py
srcver=$(%{__python} -c "from rtevalversion import RTEVAL_VERSION; print RTEVAL_VERSION")
rm -rf rtevalversion.py
if [ $srcver != %{version} ]; then
   printf "\n***\n*** rteval spec file version do not match the rteval/rteval.py version\n***\n\n"
   exit -1
fi

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%doc COPYING
%dir %{_datadir}/%{name}
%{python_sitelib}/rteval/rtevalclient.py*
%{python_sitelib}/rteval/rtevalConfig.py*
%{python_sitelib}/rteval/rtevalXMLRPC.py*
%{python_sitelib}/rteval/version.py*
%{python_sitelib}/rteval/Log.py*
%{python_sitelib}/rteval/misc.py*
%{python_sitelib}/rteval/systopology.py*

%files
%defattr(-,root,root,-)
%if "%{python_ver}" >= "2.5"
%{python_sitelib}/*.egg-info
%endif

%doc COPYING README doc/rteval.txt
%{_mandir}/man8/rteval.8.gz
%config(noreplace) %{_sysconfdir}/rteval.conf
%{_datadir}/%{name}/rteval_*.xsl
%{python_sitelib}/rteval/__init__.py*
%{python_sitelib}/rteval/rtevalMailer.py*
%{python_sitelib}/rteval/rtevalReport.py*
%{python_sitelib}/rteval/xmlout.py*
%{python_sitelib}/rteval/modules
%{python_sitelib}/rteval/sysinfo
/usr/bin/rteval

%changelog
* Thu Mar 16 2017 Clark Williams <williams@redhat.com> - 2.14-1
- removed leftover import of systopology from sysinfo

* Wed Mar 15 2017 Clark Williams <williams@redhat.com> - 2.13-2
- Updated specfile to correct version and bz [1382155]

* Tue Sep 20 2016 Clark Williams <williams@rehdat.com> - 2.12-1
- handle empty environment variables SUDO_USER and USER [1312057]

* Tue Aug 30 2016 Clark Williams <williams@rehdat.com> - 2.11-1
- make sure we return non-zero for early exit from tests

* Wed Aug  3 2016 Clark Williams <williams@rehdat.com> - 2.10-1
- bumped version for RHEL 7.3 release

* Mon May  9 2016 Clark Williams <williams@redhat.com> - 2.9.1
- default cpulist for modules if only one specified [1333831]

* Tue Apr 26 2016 Clark Williams <williams@redhat.com> - 2.8.1
- add the --version option to print the rteval version
- made the --cyclictest-breaktrace option work properly [1209986]

* Fri Apr  1 2016 Clark Williams <williams@redhat.com> - 2.7.1
- treat SIGINT and SIGTERM as valid end-of-run events [1278757]
- added cpulist options to man page

* Thu Feb 11 2016 Clark Williams <williams@redhat.com> - 2.6.1
- update to make --loads-cpulist and --measurement-cpulist work [1306437]

* Thu Dec 10 2015 Clark Williams <williams@refhat.com> - 2.5-1
- stop using old numactl --cpubind argument

* Wed Dec  9 2015 Clark Williams <williams@refhat.com> - 2.4.2
- added Require of package numactl

* Tue Nov 17 2015 Clark Williams <williams@refhat.com> - 2.4.1
- rework hackbench load to not generate cross-node traffic [1282826]

* Wed Aug 12 2015 Clark Williams <williams@redhat.com> - 2.3-1
- comment out HWLatDetect module from default config [1245699]

* Wed Jun 10 2015 Clark Williams <williams@redhat.com> - 2.2-1
- add --loads-cpulist and --measurement-cpulist to allow cpu placement [1230401]

* Thu Apr 23 2015 Luis Claudio R. Goncalves <lgoncalv@redhat.com> - 2.1-8
- load default configs when no config file is specified (Jiri kastner) [1212452]

* Wed Jan 14 2015 Clark Williams <williams@redhat.com> - 2.1-7
- added requires of bzip2 to specfile [1151567]

* Thu Jan  8 2015 Clark Williams <williams@redhat.com> - 2.1-6
- cleaned up product documentation [1173315]

* Mon Nov 10 2014 Luis Claudio R. Goncalves <lgoncalv@redhat.com> - 2.1-5
- rebuild for RHEL-7.1 (1151567)

* Thu Mar 27 2014 Clark Williams <williams@redhat.com> - 2.1-4
- cherry-picked old commit to deal with installdir problem

* Wed Mar 26 2014 Clark Williams <williams@redhat.com> - 2.1-3
- added sysstat requires to specfile

* Tue Mar 12 2013 David Sommerseth <davids@redhat.com> - 2.1-2
- Migrated from libxslt-python to python-lxml

* Fri Jan 18 2013 David Sommerseth <davids@redhat.com> - 2.1-1
- Made some log lines clearer
- cyclictest: Added --cyclictest-breaktrace feature
- cyclictest: Removed --cyclictest-distance option
- cyclictest: Use a tempfile buffer for cyclictest's stdout data
- cyclictest: Report if breaktrace was triggered
- cyclictest: Make the unit test work again
- cyclictest: Only log and show statistic data when samples are collected
- Copyright updates

* Thu Jan 17 2013 David Sommerseth <davids@redhat.com> - 2.0.1-1
- Fix up type casting in the core module code
- hwlatdetect: Add some more useful debug info
- Reworked the run logic for modules - allow them to flag they won't run
- Fixed a few log messages in load modules
- Add a 30 seconds sleep before unleashing the measurement threads

* Thu Jan 10 2013 David Sommerseth <davids@redhat.com> - 2.0-3
- Separate out RTEVAL_VERSION into rteval.version, to avoid
  massive BuildRequirements

* Fri Dec 21 2012 David Sommerseth <davids@redhat.com> - 2.0-2
- Split out common files into rteval-common

* Fri Dec 21 2012 David Sommerseth <davids@redhat.com> - 2.0-1
- Updated to rteval v2.0 and reworked spec file to use setup.py directly

* Tue Oct 23 2012 Clark Williams <williams@redhat.com> - 1.36-1
- deal with system not having dmidecode python module
- make sure to cast priority parameter to int
- from Raphaël Beamonte <raphael.beamonte@gmail.com>:
  - Rewrite of the get_kthreads method to make it cross-distribution
  - Adds getcmdpath method to use which to locate the used commands
  - Rewrite of the get_services method to make it cross-distribution

* Mon Apr  2 2012 Clark Williams <williams@redhat.com> - 1.35-1
- fix thinko where SIGINT and SIGTERM handlers were commented out

* Thu Jan 12 2012 Clark Williams <williams@redhat.com> - 1.34-1
- fix missing config merge in rteval.py to pass parameters
  down to cyclictest
- modify hackbench to use helper function to start process

* Sat May 14 2011 Clark Williams <williams@redhat.com> - 1.33-1
- modify hackbench cutoff to be 0.75GB/core

* Mon Aug 23 2010 Clark Williams <williams@redhat.com> - 1.32-1
- update docs
- refactor some RTEval methods to utility functions
- modify hackbench.py not to run under low memory conditions
- clean up XML generation to deal with new hackbench code
- clean up XSL code to deal with new XML 'run' attribute
- from David Sommerseth <davids@redhat.com>:
  - improve CPU socket counting logic
  - delay log directory creation until actually needed
- from Gowrishankar <gowrishankar.m@in.ibm.com>:
  - check if the core id really exists (multithreading fix)

* Mon Jul 26 2010 Clark Williams <williams@redhat.com> - 1.31-1
- from David Sommerseth <davids@redhat.com>:
  - Updated hackbench implementation to avoid overusing resources
  - Don't show NUMA node information if it's missing in the summary.xml
  - Show CPU cores properly

* Wed Jul 21 2010 Clark Williams <williams@redhat.com> - 1.30-1
- added code to hackbench to try to detect and ease memory pressure

* Fri Jul 16 2010 Clark Williams <williams@redhat.com> - 1.29-1
- fixed incorrect type value in kcompile.py

* Fri Jul 16 2010 Clark Williams <williams@redhat.com> - 1.28-1
- added logic to loads to adjust number of jobs based on ratio
  of memory per core

* Wed Jul 14 2010 Clark Williams <williams@redhat.com> - 1.27-1
- modified hackbench to go back to using threads rather than
  processes for units of work
- added memory size, number of numa nodes and run duration to the
  parameter dictionary passed to all loads and cyclictest

* Tue Jul 13 2010 Clark Williams <williams@redhat.com> - 1.26-1
- modified hackbench parameters to reduce memory consumption

* Mon Jul 12 2010 Clark Williams <williams@redhat.com> - 1.25-1
- fixed cyclictest bug that caused everything to be uniprocessor
- updated source copyrights to 2010

* Fri Jul  9 2010 Clark Williams <williams@redhat.com> - 1.24-1
- modified hackbench arguments and added new parameters for
  hackbench in rteval.conf

* Thu Jul  8 2010 Clark Williams <williams@redhat.com> - 1.23-1
- version bump to deal with out-of-sync cvs issue

* Thu Jul  8 2010 Clark Williams <williams@redhat.com> - 1.22-1
- merged David Sommerseth <davids@redhat.com> changes to use
  hackbench from rt-tests packages rather than carry local copy
- converted all loads and cyclictest to pass __init__ parameters
  in a dictionary rather than as discrete parameters
- added logging for load output

* Tue Apr 13 2010 Clark Williams <williams@redhat.com> - 1.21-1
- from Luis Claudio Goncalves <lgoncalv@redhat.com>:
  - remove unecessary wait() call in cyclictest.py
  - close /dev/null after using it
  - call subprocess.wait() when needed
  - remove delayloop code in hackbench.py
- from David Sommerseth <davids@redhat.com>:
  - add SIGINT handler
  - handle non-root user case
  - process DMI warnings before command line arguments
  - added --annotate feature to rteval
  - updates to xmlrpc code

* Tue Apr  6 2010 Clark Williams <williams@redhat.com> - 1.20-1
- code fixes from Luis Claudio Goncalves <lgoncalv@redhat.com>
- from David Sommerseth <davids@redhat.com>:
  - xmlrpc server updates
  - cputopology.py for recording topology in xml
  - added NUMA node recording for run data
  - rpmlint fixes
- added start of rteval whitepaper in docs dir

* Tue Mar 16 2010 Clark Williams <williams@redhat.com> - 1.19-1
- add ability for --summarize to read tarfiles
- from David Sommerseth <davids@redhat.com>
  - gather info about loaded kernel modules for XML file
  - added child tracking to hackbench to prevent zombies

* Tue Feb 16 2010 Clark Williams <williams@redhat.com> - 1.18-1
- fix usage of python 2.6 features on RHEL5 (python 2.4)

* Tue Feb 16 2010 Clark Williams <williams@redhat.com> - 1.17-1
- added logic to filter non-printables from service status output
  so that we have legal XML output
- added logic to hackbench.py to cleanup properly at the end
  of the test

* Thu Feb 11 2010 Clark Williams <williams@redhat.com> - 1.16-1
- fix errors in show_remaining_time() introduced because
  time values are floats rather than ints

* Thu Feb 11 2010 Clark Williams <williams@redhat.com> - 1.15-1
- added logic to use --numa and --smp options of new cyclictest
- added countdown report for time remaining in a run

* Tue Feb  9 2010 Clark Williams <williams@redhat.com> - 1.14-1
- David Sommerseth <davids@redhat.com>:
  merged  XMLReport() changes for hwcert suite

* Tue Dec 22 2009 Clark Williams <williams@redhat.com> - 1.13-1
- added cyclictest default initializers
- added sanity checks to statistics reduction code
- updated release checklist to include origin push
- updated Makefile clean and help targets
- davids updates (mainly for v7 integration):
  - Add explicit sys.path directory to the python sitelib+
    '/rteval'
  - Send program arguments via RtEval() constructor
  - Added more DMI data into the summary.xml report
  - Fixed issue with not including all devices in the
    OnBoardDeviceInfo tag

* Thu Dec  3 2009 David Sommerseth <davids@redhat.com> - 1.12-2
- fixed Makefile and specfile to include and install the
  rteval/rteval_histogram_raw.py source file for gaining
  raw access to histogram data
- Removed xmlrpc package during merge against master_ipv4 branch

* Wed Nov 25 2009 Clark Williams <williams@redhat.com> - 1.12-1
- fix incorrect reporting of measurement thread priorities

* Mon Nov 16 2009 Clark Williams <williams@redhat.com> - 1.11-5
- ensure that no double-slashes ("//") appear in the symlink
  path for /usr/bin/rteval (problem with rpmdiff)

* Tue Nov 10 2009 Clark Williams <williams@redhat.com> - 1.11-4
- changed symlink back to install and tracked by %%files

* Mon Nov  9 2009 Clark Williams <williams@redhat.com> - 1.11-3
- changed symlink generation from %%post to %%posttrans

* Mon Nov  9 2009 Clark Williams <williams@redhat.com> - 1.11-2
- fixed incorrect dependency for libxslt

* Fri Nov  6 2009 Clark Williams <williams@redhat.com> - 1.11-1
- added base OS info to XML file and XSL report
- created new package rteval-loads for the load source code

* Wed Nov  4 2009 Clark Williams <williams@redhat.com> - 1.10-1
- added config file section for cyclictest and two settable
  parameters, buckets and interval

* Thu Oct 29 2009 Clark Williams <williams@redhat.com> - 1.9-1
- merged davids updates:
	-H option (raw histogram data)
	cleaned up xsl files
	fixed cpu sorting

* Mon Oct 26 2009 David Sommerseth <davids@redhat.com> - 1.8-3
- Fixed rpmlint complaints

* Mon Oct 26 2009 David Sommerseth <davids@redhat.com> - 1.8-2
- Added xmlrpc package, containing the XML-RPC mod_python modules

* Tue Oct 20 2009 Clark Williams <williams@redhat.com> - 1.8-1
- split kcompile and hackbench into sub-packages
- reworked Makefile (and specfile) install/uninstall logic
- fixed sysreport incorrect plugin option
- catch failure when running on root-squashed NFS

* Tue Oct 13 2009 Clark Williams <williams@redhat.com> - 1.7-1
- added kthread status to xml file
- merged davids changes for option processing and additions
  to xml summary

* Tue Oct 13 2009 Clark Williams <williams@redhat.com> - 1.6-1
- changed stat calculation to loop less
- added methods to grab service and kthread status

* Mon Oct 12 2009 Clark Williams <williams@redhat.com> - 1.5-1
- changed cyclictest to use less memory when doing statisics
  calculations
- updated debug output to use module name prefixes
- changed option processing to only process config file once

* Fri Oct  9 2009 Clark Williams <williams@redhat.com> - 1.4-1
- changed cyclictest to use histogram rather than sample array
- calcuated statistics directly from histogram
- changed sample interval to 100us
- added -a (affinity) argument to force cpu affinity for
  measurement threads

* Thu Sep 24 2009 David Sommerseth <davids@redhat.com> - 1.3-3
- Cleaned up the spec file and made rpmlint happy

* Wed Sep 23 2009 David Sommerseth <davids@redhat.com> - 1.3-2
- Removed version number from /usr/share/rteval path

* Tue Sep 22 2009 Clark Williams <williams@redhat.com> - 1.3-1
- changes from davids:
  * changed report code to sort by processor id
  * added report submission retry logic
  * added emailer class

* Fri Sep 18 2009 Clark Williams <williams@redhat.com> - 1.2-1
- added config file handling for modifying load behavior and
  setting defaults
- added units in report per IBM request

* Wed Aug 26 2009 Clark Williams <williams@redhat.com> - 1.1-2
- missed a version change in rteval/rteval.py

* Wed Aug 26 2009 Clark Williams <williams@redhat.com> - 1.1-1
- modified cyclictest.py to start cyclictest threads with a
  'distance' of zero, meaning they all have the same measurement
  interval

* Tue Aug 25 2009 Clark Williams <williams@redhat.com> - 1.0-1
- merged davids XMLRPC fixes
- fixed --workdir option
- verion bump to 1.0

* Thu Aug 13 2009 Clark Williams <williams@redhat.com> - 0.9-2
- fixed problem with incorrect version in rteval.py

* Tue Aug  4 2009 Clark Williams <williams@redhat.com> - 0.9-1
- merged dsommers XMLRPC and database changes
- Specify minimum python-dmidecode version, which got native XML support
- Added rteval_dmi.xsl
- Fixed permission issues in /usr/share/rteval-x.xx

* Wed Jul 22 2009 Clark Williams <williams@redhat.com> - 0.8-1
- added code to capture clocksource info
- added code to copy dmesg info to report directory
- added code to display clocksource info in report
- added --summarize option to display summary of existing report
- added helpfile target to Makefile

* Thu Mar 26 2009 Clark Williams <williams@torg> - 0.7-1
- added require for python-schedutils to specfile
- added default for cyclictest output file
- added help parameter to option parser data
- renamed xml output file to summary.xml
- added routine to create tarfile of result files

* Wed Mar 18 2009 Clark Williams <williams@torg> - 0.6-6
- added code to handle binary data coming from DMI tables

* Wed Mar 18 2009 Clark Williams <williams@torg> - 0.6-5
- fixed logic for locating XSL template (williams)
- fixed another stupid typo in specfile (williams)

* Wed Mar 18 2009 Clark Williams <williams@torg> - 0.6-4
- fixed specfile to install rteval_text.xsl in /usr/share directory

* Wed Mar 18 2009 Clark Williams <williams@torg> - 0.6-3
- added Requires for libxslt-python (williams)
- fixed race condition in xmlout constructor/destructor (williams)

* Wed Mar 18 2009 Clark Williams <williams@torg> - 0.6-2
- added Requires for libxslt (williams)
- fixed stupid typo in rteval/rteval.py (williams)

* Wed Mar 18 2009 Clark Williams <williams@torg> - 0.6-1
- added xml output logic (williams, dsommers)
- added xlst template for report generator (dsommers)
- added dmi/smbios output to report (williams)
- added __del__ method to hackbench to cleanup after run (williams)
- modified to always keep run data (williams)

* Fri Feb 20 2009 Clark Williams <williams@torg> - 0.5-1
- fixed tab/space mix problem
- added report path line to report

* Fri Feb 20 2009 Clark Williams <williams@torg> - 0.4-1
- reworked report output
- handle keyboard interrupt better
- removed duration mismatch between rteval and cyclictest

* Mon Feb  2 2009 Clark Williams <williams@torg> - 0.3-1
- initial checkin
