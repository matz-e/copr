%define git_owner       jwilm
%define git_url         https://github.com/%{git_owner}/%{name}
%define commit          4fbae5e397c514c245432a6415a4c99c52b7978f
%define abbrev          %(c=%{commit}; echo ${c:0:7})

Name:           alacritty
Summary:        A cross-platform, GPU enhanced terminal emulator
License:        ASL 2.0
Release:        1%{?dist}
URL:            %{git_url}

Version:        0.3.2
Source0:        %{git_url}/archive/%{commit}/%{git_owner}-%{name}-%{abbrev}.tar.gz

Requires:       xclip

BuildRequires:  cmake
BuildRequires:  freetype-devel
BuildRequires:  fontconfig-devel

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  gcc-c++


%description
Alacritty is the fastest terminal emulator in existence. Using the GPU for
rendering enables optimizations that simply aren't possible in other emulators.

%prep
%autosetup -n %{name}-%{commit}

%build
cargo build --release

%install
install -D -m755 target/release/%{name} %{buildroot}/%{_bindir}/%{name}
install -D -m644 extra/linux/alacritty.desktop %{buildroot}/%{_datadir}/applications/alacritty.desktop
install -D -m644 extra/logo/alacritty-term.svg %{buildroot}/%{_datadir}/pixmaps/Alacritty.svg
install -d -m755 %{buildroot}/%{_datadir}/%{name}
install -m644 alacritty*.yml %{buildroot}/%{_datadir}/%{name}
cat extra/alacritty.man | gzip - > extra/alacritty.1.gz
install -D -m644 extra/alacritty.1.gz %{buildroot}/%{_mandir}/man1/alacritty.1.gz
install -D -m644 extra/completions/_alacritty %{buildroot}/%{_datadir}/zsh/site-functions/_alacritty
install -D -m644 extra/completions/alacritty.bash %{buildroot}/%{_datadir}/bash/bash-completion/completions/alacritty/alacritty.bash
install -D -m644 extra/completions/alacritty.fish %{buildroot}/%{_datadir}/fish/vendor_completions.d/alacritty.fish
# install -D -m755 extra/alacritty.info %{buildroot}/%{_datadir}/terminfo/a
tic -xe alacritty,alacritty-direct -o %{buildroot}/%{_datadir}/terminfo extra/alacritty.info

%post
update-desktop-database &> /dev/null ||:

%postun
update-desktop-database &> /dev/null ||:

%posttrans
desktop-file-validate %{_datadir}/applications/alacritty.desktop &> /dev/null || :

%files
%license LICENSE-APACHE
%doc README.md CHANGELOG.md
%{_bindir}/alacritty
%{_mandir}/man1/alacritty.1.gz
%{_datadir}/%{name}/*.yml
%{_datadir}/applications/*.desktop
%{_datadir}/bash
%{_datadir}/fish
%{_datadir}/pixmaps/Alacritty.svg
%{_datadir}/terminfo/a/alacritty*
%{_datadir}/zsh

%changelog
* Sun May 05 2019 matz-e <m@sushinara.net> 0.3.2-1
- Add shell completions

* Sat Apr 27 2019 matz-e <m@sushinara.net> 0.3.2
- Bump to 0.3.2

* Mon Nov 05 2018 Poppy Schmo <oranenj@iki.fi> 0.2.1-2.git8161798
- Build from git with COPR

* Mon Nov 05 2018 Poppy Schmo <oranenj@iki.fi> 0.2.1-1
- Build from git with COPR

* Sat Jun 17 2017 Poppy Schmo <poppyschmoATprouxTawnMaighlDawtCahm> 0.1.0-2
- Remove trailing abbrev sha from version number

* Mon Apr 10 2017 Poppy Schmo <poppyschmoATprouxTawnMaighlDawtCahm> 0.1.0-1
- Copy PKGBUILD from the AUR https://aur.archlinux.org/packages/alacritty-git
