Name:	wolffia	
Version:	0.22
Release:	1
Summary:	Molecular dynamics simulation package.
Group:		Applications/Education
License:	Yuyo
URL:		http://wolffia.uprh.edu/

Requires: python >= 2.7, PyQt4 >= 4.8.6, PyQwt >= 5.2.0, python-openbabel >= 2.3.1, PyOpenGL >= 3.0.1

%description
 Wolffia is a graphical user interface to setup, execute,
 monitor and analyze molecular dynamics simulations.

%prep

%build

%clean

%files
%defattr(-,root,root,-)
%doc

/usr/share/wolffia/*
/usr/bin/*


%changelog

