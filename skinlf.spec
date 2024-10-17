%define _version2 20060722

Summary:	Allows developers to write skinnable application using the Swing toolkit
Name:		skinlf
Group:		Development/Java
Version:	6.7
Release:	0.0.7
License:	Skin Look And Feel License
URL:		https://skinlf.l2fprod.com/index.html
Source0:	%{name}-%{version}-%{_version2}.tar.bz2
Source1:	imageconversion.jar
Source2:	%{name}-build.xml
Source3:	%{name}-resources.tar.bz2
Patch0:		%{name}-no-jimi.patch
BuildRequires:	ant
BuildRequires:	dos2unix
BuildRequires:	java-rpmbuild >= 1.5
BuildRequires:	jpackage-utils >= 1.5
BuildRequires:	laf-plugin >= 0.2
BuildRequires:	xalan-j2
#BuildRequires:	jimi >= 1.0
Requires:	java >= 1.5
#Requires:	jimi >= 1.0
Requires:	jpackage-utils >= 1.5
Requires:	laf-plugin >= 0.2
Requires:	xalan-j2
BuildArch:	noarch

%description
Skin Look And Feel allows Java developers to write skinnable application using
the Swing toolkit. Skin Look And Feel is able to read GTK (The Gimp Toolkit)
and KDE (The K Desktop Environment) skins to enhance your application GUI
controls such as Buttons, Checks, Radios, Scrollbars, Progress Bar, Lists,
Tables, Internal Frames, Colors, Background Textures, Regular Windows. Skin
Look And Feel (aka SkinLF) also includes NativeSkin to create irregular
windows.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%package demo
Summary:	Some examples for %{name}
Group:		Development/Java
Requires:	%{name} = %{version}-%{release}

%description demo
Some examples for %{name}.

%prep
%setup -q -n %{name}-%{version}

cp %{SOURCE1} .
cp %{SOURCE2} build.xml
tar xfj %{SOURCE3}
%patch0

dos2unix  AUTHORS CHANGES INSTALL LICENSE LICENSE_nanoxml README THANKS
%__chmod 644 AUTHORS CHANGES INSTALL LICENSE LICENSE_nanoxml README THANKS

%build
%ant jar javadocs

%install
[ -d %{buildroot} -a "%{buildroot}" != "" ] && %__rm -rf %{buildroot}

# jars
install -dm 755 %{buildroot}%{_javadir}
install -pm 644 lib/%{name}.jar \
	%{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr docs/* \
	%{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

# demo
install -dm 755 %{buildroot}%{_datadir}/%{name}
install -m 644 lib/%{name}_demo.jar \
	%{buildroot}%{_datadir}/%{name}
install -m 644 lib/themepack.zip \
	%{buildroot}%{_datadir}/%{name}

# create startscripts for demo-apps
%if 0
# not supported for linux
%__cat > bin/clock.sh << EOF
#!/bin/bash
%{java} -cp %{_javadir}/%{name}.jar:%{_javadir}/laf-plugin.jar:%{_datadir}/%{name}/%{name}_demo.jar examples.Clock clock.gif
EOF

# not supported for linux
cat > bin/region.sh << EOF
#!/bin/bash
%{java} -cp %{_javadir}/%{name}.jar:%{_datadir}/%{name}/%{name}_demo.jar examples.nativesplash
EOF
%endif

cat > bin/alwaysontop.sh << EOF
#!/bin/bash
%{java} -cp %{_javadir}/%{name}.jar:%{_datadir}/%{name}/%{name}_demo.jar examples.alwaysontop
EOF

cat > bin/demo.sh << EOF
#!/bin/bash
THEMEPACK=\$1
if [ "\$THEMEPACK" == "" ]; then
	THEMEPACK=%{_datadir}/%{name}/themepack.zip
else
	shift
fi
%{java} -cp %{_javadir}/%{name}.jar:%{_javadir}/laf-plugin.jar:%{_datadir}/%{name}/%{name}_demo.jar examples.demo \$THEMEPACK \$@
EOF

# install startscripts for demo-apps
install -m 755 bin/*.sh \
	%{buildroot}%{_datadir}/%{name}

%post javadoc
%__rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%doc AUTHORS CHANGES INSTALL LICENSE LICENSE_nanoxml README THANKS
%{_javadir}/%{name}*.jar

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.jar
%{_datadir}/%{name}/*.sh
%{_datadir}/%{name}/themepack.zip

