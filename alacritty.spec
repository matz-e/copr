%define git_owner       jwilm
%define git_url         https://github.com/%{git_owner}/%{name}
%define commit          0e49bfb02a80c480df802f2f0a79dc2fa0de6753
%define abbrev          %(c=%{commit}; echo ${c:0:7})
Name:           alacritty
Summary:        A cross-platform, GPU enhanced terminal emulator
License:        ASL 2.0
Release:        1%{?dist}
URL:            %{git_url}

Version:        0.2.1.git%{abbrev}
Source0:        %{git_url}/archive/%{commit}/%{git_owner}-%{name}-%{abbrev}.tar.gz

Requires:       freetype-devel
Requires:       fontconfig-devel
Requires:       xclip

BuildRequires:  cmake

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  gcc-c++


%description
Alacritty is the fastest terminal emulator in existence. Using the GPU for
rendering enables optimizations that simply aren't possible in other emulators.

%prep
%setup -qn %{name}-%{commit}

%build
cargo build --release

%install
install -D -m755 target/release/%{name} %{buildroot}/%{_bindir}/%{name}
install -D -m644 Alacritty.desktop %{buildroot}/%{_datadir}/applications/Alacritty.desktop
install -d -m755 %{buildroot}/%{_datadir}/%{name}
install -m644 alacritty*.yml %{buildroot}/%{_datadir}/%{name}
install -d -m755 %{buildroot}/%{_datadir}/terminfo/a
tic -o %{buildroot}/%{_datadir}/terminfo alacritty.info

%post
update-desktop-database &> /dev/null ||:

%postun
update-desktop-database &> /dev/null ||:

%posttrans
desktop-file-validate %{_datadir}/applications/alacritty.desktop &> /dev/null || :

%files
%{_bindir}/alacritty
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}/*.yml
%{_datadir}/terminfo/*

%changelog
* Mon Nov 05 2018 Poppy Schmo <oranenj@iki.fi> 0.2.1-1
- Build from git with COPR

* Sat Jun 17 2017 Poppy Schmo <poppyschmoATprouxTawnMaighlDawtCahm> 0.1.0-2
- Remove trailing abbrev sha from version number

* Mon Apr 10 2017 Poppy Schmo <poppyschmoATprouxTawnMaighlDawtCahm> 0.1.0-1
- Copy PKGBUILD from the AUR https://aur.archlinux.org/packages/alacritty-git
