# wolffia

Wolffia eases the preparation of classical molecular dynamics simulations by providing a simple but powerfull user interface to many widely used applications.

## Getting Started

Wolffia is a graphical user interface that works as a simulation environment for performing Classical Molecular Dynamics simulations. Its tab-based design is intended to guide the user throughout the simulation process: building a mixture, defining force fields, setting-up periodic boundary conditions and solvating, energy minimization, and simulation. It provides utilities not just for creating, editing and displaying molecular systems but also to allow the user to run simulations by using NAMD (and soon with LAMMPS), a well established simulation suite, as it automatically assembles the configuration settings for doing so. It can be used for the preprocessing, experimentation, or both. A catalog of molecular structures is included for user convenience. A graphical representation of NAMD's output can be monitored during minimization and simulation runs. Its development is focused on the need of integrated and user-friendly software for working with this simulation technique.

Wolffia's latest release is available at http://wolffia.uprh.edu/.

[![Alt text](https://img.youtube.com/vi/16naAAW-ncQ/0.jpg)](https://www.youtube.com/watch?v=16naAAW-ncQ)

## Prerequisites

Wolffia has been mainly tested in Debian based operating systems. Additional operating systems may be supported.
Wolffia currently uses Python 2. Support for Python 3 is currently under development.

Under Ubuntu:
```
sudo apt-get install python-qt4-gl python-qwt5-qt4 pyqt4-dev-tools python-openbabel python-networkx python-opengl sshpass python-matplotlib python-scipy
```

Wolffia currently uses namd2 to perform the simulations. NAMD2 is not a requirement for wolffia to run. Simulations can be built using wolffia and executed on a remote system with NAMD2 installed. Wolffia offers the capability of performing simulations on remote systems.

You may download NAMD2 from their [official website](https://www.ks.uiuc.edu/Development/Download/download.cgi?PackageName=NAMD).
You may install it following the steps outlined below.
```
sudo mkdir /usr/local/namdo
sudo cd /usr/local/namd;
sudo tar -xzf ${path_where_namd_was_downloaded}.tar.gz
sudo ln -s /usr/local/namd/${namd_extracted_directory}/namd2 /usr/local/bin/namd2
sudo ln -s /usr/local/namd/${namd_extracted_directory}/charmrun /usr/local/bin/charmrun
```

## Installation

Installing wolffia as a project without the need of elevated privileges.
```
git clone https://github.com/compMathUPRH/wolffia.git # clone from git
cd wolffia; make;                                     # compile wolffia
./wolffia                                             # run wolffia
``` 

As an executable for multiple users (requires elevated privileges).
```
git clone https://github.com/compMathUPRH/wolffia.git
sudo cp -r path/to/wolffia /usr/local/share
sudo ln -s  /usr/local/share/wolffia/wolffia /usr/local/bin/wolffia
```

## Acknowledgements

This work is being sponsored by UPRH-PENN Partnership for Research and Education in Materials, University of Puerto Rico at Humacao. 

## References

Cuadrado, M. M., Martínez, C. C., Serrano, M. L., Miranda, F. M., & Alfaro, R. V. (2012). An Implementation of a Graphical Interface for Molecular Simulation Software using Python and Qt4. 2012 NCUR.

Sotero-Esteva, J. O. (2013). Wolffia: An environment with a graphical user interface to prepare and monitor classical molecular dynamics simulations.

Sotero–Esteva, J. O., Martínez, F., Quiñones, R., Cuadrado, W., & de Jesús, A. FAST SET-UP OF CLASSICAL MOLECULAR DYNAMICS SIMULATIONS OF NANOMATERIALS USING WOLFFIA.

López, M., & Campus, R. P. Usability of the mixture building section of Wolffia.
