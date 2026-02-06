Name:           ksystemstats-scripts
Version:        1.0
Release:        1%{?dist}
Summary:        Custom sensors plugin for KDE System Monitor via text streams

License:        GPL-3.0-or-later
URL:            https://github.com/itotm/ksystemstats_scripts#
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 3.16
BuildRequires:  gcc-c++
BuildRequires:  extra-cmake-modules >= 6.10.0
BuildRequires:  kf6-rpm-macros

# Qt6 dependencies
BuildRequires:  cmake(Qt6Core) >= 6.7.0

# KF6 dependencies  
BuildRequires:  cmake(KF6CoreAddons) >= 6.10.0
BuildRequires:  cmake(KF6I18n) >= 6.10.0

# KSysGuard dependency
BuildRequires:  libksysguard-devel >= 6.2.90

Requires:       kf6-filesystem
Requires:       ksystemstats >= 6.2.90

%description
KSystemStats Scripts provides a simple way to create custom sensors for KDE 
System Monitor via text streams. Scripts can be written in any language 
(Python, Bash, etc.) and communicate via stdin/stdout to provide custom 
monitoring data.

Scripts should be placed in ~/.local/share/ksystemstats-scripts/ and made 
executable. The plugin monitors this directory and automatically loads/reloads
scripts when they are added, modified, or enabled/disabled.

%prep
%autosetup -n ksystemstats_scripts-%{version}

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DQT_MAJOR_VERSION=6
%cmake_build

%install
%cmake_install

%files
%license LICENSE.txt
%doc README.md example.py example.sh
%{_qt6_plugindir}/ksystemstats/ksystemstats_plugin_scripts.so

%changelog
* Wed Feb 04 2026 - 1.0-1
- Initial package for COPR