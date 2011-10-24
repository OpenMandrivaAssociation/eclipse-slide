#ExclusiveArch: i386 x86_64

BuildRequires: eclipse-pde >= 3.2
BuildRequires: javacc
BuildRequires: ant >= 1.6
BuildRequires: jpackage-utils >= 0:1.5
BuildRequires: eclipse-setools >= 3.3.2
BuildRequires: ganymed-ssh2
BuildRequires: java-1.6.0-openjdk

## The source for this package was pulled from upstream's svn repo.
## Use the following commands to generate the tarball:
# mkdir eclipse-slide
# cd eclipse-slide
# svn export http://oss.tresys.com/repos/slide/tags/%{version}/slide-plugin slide-plugin
# svn export http://oss.tresys.com/repos/slide/tags/%{version}/eclipse-feature eclipse-feature
# svn export http://oss.tresys.com/repos/slide/tages/%{version}/com.tresys.slide.doc.user slide-help
# tar -czvf eclipse-slide.tar.gz *
#Source0: %{name}.tar.gz
#Release: 0.1.svn2029

Source0: http://oss.tresys.com/projects/slide/chrome/site/src/%{name}-%{version}.tar.gz
Release: 2

%define eclipse_name		eclipse/dropins/slide
%define eclipse_base		%{_datadir}/%{eclipse_name}
%define svnbase			http://oss.tresys.com/repos/slide/trunk/

#get version numbers from eclipse plugin files
#%define version		%(tar -Oxzf ${RPM_SOURCE_DIR}/%{SOURCE0} eclipse-feature/feature.xml | xpath /feature/@version 2> /dev/null | cut -d '"' -f 2)
#%define plugin_ver	%(tar -Oxzf ${RPM_SOURCE_DIR}/%{SOURCE0} slide-plugin/META-INF/MANIFEST.MF | grep Bundle-Version | cut -d : -f 2 | tr -d " ")
#%define help_ver	%(tar -Oxzf ${RPM_SOURCE_DIR}/%{SOURCE0} slide-help/META-INF/MANIFEST.MF | grep Bundle-Version | cut -d : -f 2 | tr -d " ")


Summary: SELinux policy editing plugin for Eclipse
Name: eclipse-slide
Version: 1.3.16

License: GPLv2
BuildArch: noarch
Group: Development/Java
URL: http://oss.tresys.com/projects/slide
Requires: eclipse-platform >= 3.2
Requires: ganymed-ssh2
Requires: eclipse-setools >= 3.3.2.2
Requires: policycoreutils >= 1.33
Requires: selinux-policy-devel
Requires: java-1.6.0-openjdk
ExclusiveOS: linux

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
SLIDE is an integrated development environment (IDE) for Security Enhanced 
Linux (SELinux) developers and integrators. 
SLIDE provides features to make the task of SELinux policy development and 
testing easier.  This is achieved by providing wizards to automate common 
tasks and by providing developer-friendly features.  SLIDE is also designed 
for use with the SELinux Reference Policy, another open source project by 
Tresys that has become the standard SELinux security policy.

SLIDE Features include:
A graphical user interface for policy development, including policy syntax 
highlighting and integrated compilation.
Integration with SELinux Reference Policy.
Support for both modular and monolithic SELinux policy development.
Wizards to create complete SELinux policies as well as individual policy 
modules.
Integrated remote policy installation and audit monitoring, to facilitate 
policy testing. 
Seamless integration with the power of standard Eclipse. 

%prep
%setup -q -c -n eclipse-slide

%build 
cd slide-plugin
ant -f rpmbuild.xml buildjar
cd ../slide-help
ant -f rpmbuild.xml

%install

PLUGIN_VER=`grep Bundle-Version slide-plugin/META-INF/MANIFEST.MF | cut -d : -f 2 | tr -d " "`
HELP_VER=`grep Bundle-Version slide-help/META-INF/MANIFEST.MF | cut -d : -f 2 | tr -d " "`

PLUGIN_DIR=%{eclipse_base}/plugins/com.tresys.slide_${PLUGIN_VER}
HELP_JAR=%{eclipse_base}/plugins/com.tresys.slide.doc.user_${HELP_VER}.jar
FEATURE_DIR=%{eclipse_base}/features/com.tresys.slide_%{version}

#rm -rf ${RPM_BUILD_ROOT}
install -pd -m755 ${RPM_BUILD_ROOT}${FEATURE_DIR}
install -pd -m755 ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -pd -m755 ${RPM_BUILD_ROOT}${PLUGIN_DIR}/META-INF


install -p -m644 ${RPM_BUILD_DIR}/eclipse-slide/slide-plugin/SLIDE.jar ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -p -m644 ${RPM_BUILD_DIR}/eclipse-slide/slide-plugin/COPYING ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -p -m644 ${RPM_BUILD_DIR}/eclipse-slide/slide-plugin/plugin.xml ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -p -m644 ${RPM_BUILD_DIR}/eclipse-slide/slide-plugin/plugin.properties ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -p -m644 ${RPM_BUILD_DIR}/eclipse-slide/slide-plugin/about.html ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -p -m644 ${RPM_BUILD_DIR}/eclipse-slide/slide-plugin/META-INF/MANIFEST.MF ${RPM_BUILD_ROOT}${PLUGIN_DIR}/META-INF

cp -pR ${RPM_BUILD_DIR}/eclipse-slide/slide-plugin/lib ${RPM_BUILD_ROOT}${PLUGIN_DIR}/lib
ln -sf %{_datadir}/java/ganymed-ssh2.jar ${RPM_BUILD_ROOT}/${PLUGIN_DIR}/lib/ganymed-ssh2.jar
cp -pR ${RPM_BUILD_DIR}/eclipse-slide/slide-plugin/icons ${RPM_BUILD_ROOT}${PLUGIN_DIR}/icons
cp -pR ${RPM_BUILD_DIR}/eclipse-slide/slide-plugin/resources ${RPM_BUILD_ROOT}${PLUGIN_DIR}/resources

install -p -m644 ${RPM_BUILD_DIR}/eclipse-slide/eclipse-feature/feature.xml ${RPM_BUILD_ROOT}${FEATURE_DIR}
install -p -m644 ${RPM_BUILD_DIR}/eclipse-slide/slide-help/help.jar ${RPM_BUILD_ROOT}${HELP_JAR}


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{eclipse_base}/
#%exclude %{eclipse_base}/plugins/com.tresys.slide*/lib/*.py[co]


