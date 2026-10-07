# Repackages upstream's prebuilt release; nothing is compiled here.
%global debug_package %{nil}
%global tarball_dir zapfast-v%{version}-%{_arch}-unknown-linux-gnu
%global release_url https://github.com/crmne/zapfast/releases/download/v%{version}
%ifarch x86_64
%global tarball_src 0
%else
%global tarball_src 1
%endif

Name:           zapfast
Version:        0.19.0
Release:        %autorelease
Summary:        Fast native WhatsApp client
License:        MIT
URL:            https://zapfast.rocks
Source0:        %{release_url}/zapfast-v%{version}-x86_64-unknown-linux-gnu.tar.gz
Source1:        %{release_url}/zapfast-v%{version}-aarch64-unknown-linux-gnu.tar.gz
Source2:        %{release_url}/checksums.txt#/zapfast-%{version}-checksums.txt
Source3:        %{release_url}/checksums.txt.sig#/zapfast-%{version}-checksums.txt.sig
# Upstream's update-signing key (assets/update-public-key.hex) in PEM form
Source4:        zapfast-update-public-key.pem

ExclusiveArch:  x86_64 aarch64

BuildRequires:  desktop-file-utils
BuildRequires:  openssl

# Loaded with dlopen() at runtime, so the dependency generator misses them
Requires:       libdbus-1.so.3()(64bit)
Requires:       libEGL.so.1()(64bit)
Requires:       libGL.so.1()(64bit)
Requires:       libwayland-client.so.0()(64bit)
Requires:       libwayland-cursor.so.0()(64bit)
Requires:       libwayland-egl.so.1()(64bit)
Requires:       libX11.so.6()(64bit)
Requires:       libX11-xcb.so.1()(64bit)
Requires:       libXcursor.so.1()(64bit)
Requires:       libXi.so.6()(64bit)
Requires:       libXrandr.so.2()(64bit)
Requires:       libxkbcommon.so.0()(64bit)
Requires:       libxkbcommon-x11.so.0()(64bit)
Requires:       alsa-plugins-pulseaudio
Requires:       hicolor-icon-theme

# ZapFast was previously released as FastsApp
Provides:       fastsapp = %{version}-%{release}
Obsoletes:      fastsapp < %{version}-%{release}

%description
ZapFast is a fast, native WhatsApp client written in Rust.

This package repackages the official upstream release after verifying
its Ed25519 publisher signature.

%prep
# Authenticate upstream's checksum manifest, then this arch's tarball
openssl pkeyutl -verify -pubin -inkey %{SOURCE4} -rawin -in %{SOURCE2} -sigfile %{SOURCE3}
awk -v f=%{tarball_dir}.tar.gz -v p=%{S:%{tarball_src}} '$2 == f {print $1 "  " p}' %{SOURCE2} | sha256sum --check --strict
%setup -q -T -b %{tarball_src} -n %{tarball_dir}

%install
install -Dpm 0755 zapfast %{buildroot}%{_bindir}/zapfast
install -Dpm 0644 packaging/applications/zapfast.desktop %{buildroot}%{_datadir}/applications/zapfast.desktop
install -Dpm 0644 packaging/icons/zapfast.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/zapfast.svg
install -Dpm 0644 contrib/omarchy/zapfast.json.tpl %{buildroot}%{_datadir}/zapfast/omarchy/zapfast.json.tpl
install -Dpm 0755 contrib/omarchy/zapfast-theme %{buildroot}%{_datadir}/zapfast/omarchy/zapfast-theme

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/zapfast.desktop

%files
%license LICENSE THIRD-PARTY-NOTICES.md
%doc README.md
%{_bindir}/zapfast
%{_datadir}/applications/zapfast.desktop
%{_datadir}/icons/hicolor/scalable/apps/zapfast.svg
%{_datadir}/zapfast/

%changelog
%autochangelog
