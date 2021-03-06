Installation
============

.. .. contents:: Contents
..     :local:

To install the IDAES PSE framework, follow the
set of instructions below that are appropriate for your needs and operating system.

If you get stuck, please contact `idaes-support@idaes.org <idaes-support@idaes.org>`_.

The minimal installation only installs IDAES and the free IPOPT_ solver with MUMPS_.
The full installation is recommended for access to more advanced solvers.
The Docker_ installation works on any platform that supports Docker, but
of course requires installation of, and some understanding of, Docker itself
to operate.

.. _Docker: https://www.docker.com/

+-----------------------+------------------+-----------------------------+
| Type of installation  | Operating System | Section                     |
+=======================+==================+=============================+
| Minimal IPOPT/MUMPS   | Linux            | :ref:`min_install_linux`    |
+-----------------------+------------------+-----------------------------+
|                       | Windows          | :ref:`min_install_windows`  |
+-----------------------+------------------+-----------------------------+
|                       | Mac OSX          | not supported [1]_          |
+-----------------------+------------------+-----------------------------+
| Full                  | Linux            | :ref:`full_install_linux`   |
+-----------------------+------------------+-----------------------------+
|                       | Windows          | :ref:`full_install_windows` |
+-----------------------+------------------+-----------------------------+
|                       | Mac OSX          | not supported [1]_          |
+-----------------------+------------------+-----------------------------+
| Docker-based          | Windows, Linux   | :ref:`install_docker`       |
|                       | OSX              |                             |
+-----------------------+------------------+-----------------------------+

.. [1] For advanced users, Mac OSX installation may be performed with some small changes
       to the Linux installation instructions.

.. note::

    These installation procedures are only fully tested on Debian-based Linux
    distributions.

Minimal installation
--------------------
To make it easier to use basic functionality and try the IDAES PSE Toolkit,
we have compiled these  "minimal" instructions, that only allow one to use the free 
IPOPT_ solver with `MUMPS`_. This will not be appropriate for some models.
We are working on an easy installer with better
solvers, but for now you will need to use the full install instructions in
the next sections if this is not sufficient for your needs.

.. _IPOPT: https://www.coin-or.org/Ipopt/documentation/documentation.html

.. _MUMPS: http://mumps.enseeiht.fr/

.. _min_install_windows:

Minimal install with IPOPT/MUMPS for Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Install Miniconda** [2]_

1. Download: https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
2. Install anaconda from the downloaded file in (1).
3. Open the Anaconda powershell (Start -> "Anaconda Powershell Prompt").
4. In the Anaconda Powershell, follow the :ref:`min_install_generic` instructions.

.. _min_install_linux:

Minimal install with IPOPT/MUMPS for Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Install  Miniconda** [2]_

1. Download: https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
2. For the next steps, open a terminal window
3. Run the script you downloaded in (1).
4. Follow the :ref:`min_install_generic` instructions.

.. [2] Miniconda is a product from `Anaconda <https://anaconda.com>`_ that contains
       their package manager, "Conda" (and not much else). This is the package manager we
       will use here for setting up the software development environment
       and installing IDAES' software (package) dependencies.


.. _min_install_generic:

Generic minimal install with IPOPT/MUMPS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have Conda installed, the remaining steps, performed in either the
Anaconda Powershell (Prompt) or a Linux terminal, are the same.

**Isolate the IDAES installation (from other Python packages)**

1. Create an environment with Python = 3.6 or above::

    conda create -n myenv "python>=3.6"

2. Activate the environment you created::

    conda activate myenv

**Install a git client**

3. Install the git client::

    conda install -c anaconda git

**Install IPOPT**

4. Install IPOPT from "conda-forge"::

    conda install -c conda-forge ipopt

5. Check if the installation worked by checking for the ipopt version::

    ipopt -v

**Download IDAES source code and install required packages**

6. Go to the idaes-pse releases page, https://github.com/IDAES/idaes-pse/releases/, and
   look at the most recent release. Under the
   section labeled "Assets" there will be a zip file. Download that file and
   extract the contents in any location of your choice.
7. In the Linux terminal or Anaconda Powershell, navigate to the folder you created
   in the previous step.
8. Install the packages required for IDAES using the following command::

    pip install -r requirements.txt

**Install IDAES**

9. In the folder where the idaes source code was downloaded, run the *setup.py* file::

    python setup.py develop

10. Run tests on unit models::

     pytest idaes/unit_models

11. You should see the tests run and all should pass to ensure the installation worked.
    You can report problems on the `Github issues page <https://github.com/IDAES/idaes-pse/issues>`_
    (Please try to be specific about the command and the offending output.)
12. Launch the Jupyter Notebook

    a. Navigate to `examples` and run Jupyter notebook::

            cd examples
            jupyter notebook

    b. Open a web browser to the URL that is printed from the previous command.


.. _full_install_linux:

Linux installation
------------------
This section has the instructions for a "full" Linux installation. If you want to just try a few
examples and find these instructions difficult to follow, you may try the :ref:`min_install_linux`.

System Requirements
^^^^^^^^^^^^^^^^^^^
The IDAES toolkit can be installed on Linux, Windows, or MacOSX. **The officially supported
platform, and the one we use for our automated testing, is Linux.** Therefore it is recommended
that for maximum stability you use this platform. However we realize many users have
Windows or Mac OSX environments. We include best-effort instructions, that we have gotten
to work for us, for those platforms as well.

    * Linux operating system
    * Python 3.6 or above (Python 2 is no longer supported)
    * Basic GNU/C compilation tools: make, gcc/g++
    * ``wget`` (for downloading software)
    * ``git`` (for getting the IDAES source code)
    * Access to the Internet

Things you must know how to do:

    * Get root permissions via `sudo`.
    * Install packages using the package manager.

Installation steps
^^^^^^^^^^^^^^^^^^

.. code-block:: sh

    sudo apt-get install gcc g++ make libboost-dev

We use a Python packaging system called Conda_.
Below are instructions for installing a minimal version of Conda, called Miniconda_.
The full version installs a large number of scientific analysis and visualization libraries
that are not required by the IDAES framework.

.. _Conda: https://conda.io/
.. _Miniconda: https://conda.io/en/latest/miniconda.html

.. code-block:: sh

    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh

Create and activate a conda environment (along with its own copy of ``pip``)
for the new IDAES installation **(you will need to** ``conda activate idaes``
**when you open a fresh terminal window and wish to use IDAES)**:

.. code-block:: sh

    conda create -n idaes pip
    conda activate idaes

Obtain the source code for IDAES from GitHub:

.. code-block:: sh

    git clone https://github.com/IDAES/idaes-pse.git

Download and compile the AMPL Solver Library (ASL) and external property functions;
this is required for steam properties and cubic equations of state. This step is
optional, but highly recommended.

.. code-block:: sh

    cd <Location to keep the ASL>
    wget https://ampl.com/netlib/ampl/solvers.tgz
    tar -xf solvers.tgz
    cd solvers
    ./configure
    make
    export ASL_BUILD=`pwd`/solvers/sys.x86_64.Linux
    cd <IDAES source main directory>
    make

Install the required Python packages:

.. code-block:: sh

    pip install -r requirements.txt
    python setup.py develop  # or "install"

Install ipopt.  If you have an HSL license, you may prefer to compile ipopt with
HSL support.  Please see the ipopt `documentation <https://projects.coin-or.org/Ipopt>`_
in that case.  Otherwise ipopt can be installed with conda.

.. code-block:: sh

    conda install -c conda-forge ipopt


At this point, you should be able to launch the Jupyter Notebook server and successfully `run examples <examples.html>`_ from the ``examples`` folder:

.. code-block:: sh

    jupyter notebook

Solvers
^^^^^^^
Some of the model code depends on external solvers. The installation instructions
above include the free IPOPT_ solver. Most of the examples can run with this solver,
but a significant number of more advanced problems will not be handled well. Some
other solvers you can install that may improve (or make possible) solutions for
these models are:

    * CPLEX: a linear optimization package from `IBM <https://www.ibm.com/analytics/cplex-optimizer>`_.
    * Gurobi: LP/MILP/MIQP, etc., solvers from `Gurobi <http://www.gurobi.com>`_.

ASL and AMPL
""""""""""""
In some cases, IDAES uses AMPL user-defined functions written in C for property
models.  Compiling these functions is optional, but some models may not work
without them.

The AMPL solver library (ASL) is required, and can be downloaded from
from https://ampl.com/netlib/ampl/solvers.tgz.  Documentation is available at
https://ampl.com/resources/hooking-your-solver-to-ampl/.


.. _full_install_windows:

Windows Installation
--------------------
.. note:: Windows is not officially supported at this time.

This is a complete guide to installing the IDAES framework on Windows. 
The :ref:`Extras section<install:Extras>` includes additional information which may be useful.
This guide includes compiling C++ components.  In the future precompiled versions of these 
libraries will be made available, simplifying the installation process.

Tools
^^^^^
Before installing the IDAES software there are a few development tools that need to be installed.
There are alternatives, but an attempt was made to provide the easiest path here.

1. Install a good text editor (Atom, notepad++, spyder, ... whatever you prefer).
2. Install a *git* client from https://git-scm.com/download/win.
   A git client is not necessary for all users, but
   if you are a developer or advanced user, you will likely want it.
3. Install MSYS2. MSYS2 provides a shell which will allow use of Linux style build tools.
   It also provides a convenient package manager (pacman) which allows for easy
   installation of build tools.

    a. Go to https://www.msys2.org/
    #. Download the x86_64 installer
    #. Run the installer (the default options should be okay)
    #. Open the MSYS2 MinGW 64-bit terminal (go to: start menu/MSYS2 64Bit/MSYS2 MinGW 64Bit).
    #. Update the MSYS2 software::

        pacman -Syu

    #. Repeat the previous step until there are no more updates.
    #. Install the build tools and libraries::

        pacman -S mingw-w64-x86_64-toolchain mingw-w64-x86_64-boost unzip patch make

    #. While MinGW does produce Windows native binaries, depending on linking options,
       some DLLs may be required.  Add the MinWG/MSYS2 DLLs to your path.  For example if MSYS2
       was installed in the default location you would probably want to add ``C:\msys64\mingw64\bin``.
       See :ref:`modify_path_env`.

.. note:: In the MSYS2 terminal the directory structure looks different than the
          regular Windows directory structure.
          The Windows C: drive is located at ``/c``.

Install Miniconda
^^^^^^^^^^^^^^^^^^
1. Download Miniconda (https://docs.conda.io/en/latest/miniconda.html)
2. Run the Miniconda installer (default options should be fine)

Get IDAES
^^^^^^^^^
The two main options for getting IDAES are to download the files or to clone the repository.
Cloning the repository requires a git client. For core IDAES developers or users who
need to track the latest developments **and** have access to the idaes-dev repo,
replace "idaes-pse" with "idaes-dev."

Option 1: Download from Github
""""""""""""""""""""""""""""""
Most users can download the release files from https://github.com/IDAES/idaes-pse/releases.
The latest development version can be downloaded by  going to https://github.com/IDAES/idaes-pse
and clicking the "Clone or Download" button then clicking on "Download Zip." Unzip the files to a convenient location.

Option 2: Fork and Clone the Repository
"""""""""""""""""""""""""""""""""""""""
For people who are not IDAES core developers but potentially would like to make
contributions to the IDAES project or closely follow IDAES development, the best way
to get the IDAES files is to fork the IDAES repo on Github, then clone the new fork.
To fork the repository sign into your Github account, and go to https://github.com/IDAES/idaes-pse.
Then, click the "Fork" button in the upper righthand corner of the page.

To clone a repository:

1. Open a command window.
2. Go to the directory where you want to create the local repo.
3. Enter the command (replace "Github_Account" with the Github account of the
   fork you wish to clone)::

    git clone https://github.com/Githhub_Account/idaes-pse

4. The clone command should create a new idaes-pse subdirectory with a local repository.

IDAES Location
""""""""""""""
In the instructions that follow ``idaes_dir`` will refer to the directory containing the IDAES files.

Compiling ASL
^^^^^^^^^^^^^
The AMPL Solver Library (ASL) is required to compile some user-defined functions used
in parts of the IDAES framework (mainly some property packages).

1. Open the MSYS2 MinGW 64-bit terminal (go to: start menu/MSYS2 64Bit/MSYS2 MinGW 64Bit).
2. Create a directory for complied source code in a convenient location, which will be
   referred to as ``src`` in these instructions.  For example (obviously change the
   user name and ``/c`` is the location of the C: drive in Windows) ``mkdir /c/Users/jeslick/src``.
3. Go to the source directory (again replace src with the actual directory)::

    cd src

4. Download the ASL and compile the ASL::

    wget https://ampl.com/netlib/ampl/solvers.tgz
    tar -zxvf solvers.tgz
    cd solvers
    ./configure
      make

Compiling IDAES AMPL Function Extensions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IDAES uses some additional user defined AMPL functions for various purposes, but
mainly for physical properties.  Before installing IDAES these functions must be
compiled.

1. Open the MSYS2 MinGW 64-bit terminal.

2. Set the ASL_BUILD environment variable (the directory may differ depending on the
   architecture and replace ``.../src`` with the actual location of your src directory)::

    export ASL_BUILD=C:/.../src/solvers/sys.x86_64.MINGW64_NT-10.0

3. Go to the IDAES directory (replace ``/c/idaes_dir`` with the location
   of the IDAES files)::

    cd /c/idaes_dir/idaes_pse/

4. Run: ``make``

If the compile finishes without errors you can proceed to installing IDAES.

Install IDAES
^^^^^^^^^^^^^

1. Open the Anaconda Command prompt
2. Create an ``idaes`` environment and activate it (optional)::

    conda create -n idaes "python>=3.6" pip
    conda activate idaes

.. note::
  If you are using a version of conda older than 4.4 the command on Windows to
  activate a conda environment (for example idaes) is ``activate idaes``.

3. Install requirements::

    pip install -r requirements.txt

4. Install IDAES::

    python setup.py develop

5. (Optional) Install IPOPT::

    conda install -c conda-forge ipopt

Extras
^^^^^^

Building Documentation
""""""""""""""""""""""

Most users do not need to build this documentation, but if necessary you can.  The instructions here use the ``make`` from the MSYS2 installed above.

  1. Open the Anaconda Command prompt, and activate the IDAES environment
  2. Go to the IDAES directory
  3. Go to the docs subdirectory
  4. Add the MSYS2 bin directory to your path temporarily.
     For example, if MSYS2 is installed in the default location::

        set Path=%Path%;C:\msys64\usr\bin

  5. Run make (from MSYS2)::

        make html

The HTML documentation will be in the "build" subdirectory.

Compiling IPOPT
"""""""""""""""

It's not required to compile IPOPT yourself, and these are pretty much the standard
IPOPT compile instructions.  If you have set up MSYS2 as above, you should be able to
follow these instructions to compile IPOPT for Windows.

1. Download IPOPT from https://www.coin-or.org/download/source/Ipopt/, and put the zip file in the ``src`` directory created above.
2. Open the MSYS2 MinGW 64-bit terminal (go to: start menu/MSYS2 64Bit/MSYS2 MinGW 64Bit).
3. Unzip Ipopt (the ``*`` here represents the portion of the file names with the Ipopt
   version information)::

    unzip Ipopt*.zip
    cd Ipopt*

4. Get third party libraries::

    cd ThirdParty/ASL
    ./get.ASL
    cd ../Blas
    ./get.Blas
    # and so on for all the other subdirectories except HSL.
    # If you have an HSL license follow the instructions in the HSL directory

5. Go to the IPOPT directory (replace $IPOPT_DIR with the IPOPT directory)::

    cd $IPOPT_DIR
    ./configure
    make

6. The IPOPT AMPL executable will be in ./Ipopt/src/Apps/AmplSolver/ipopt.exe, you
   can move the executable to a location in the path (environment variable).
   See :ref:`modify_path_env`.

.. _modify_path_env:

Modifying the Path Environment Variable
"""""""""""""""""""""""""""""""""""""""

The Windows ``Path`` environment variable provides a search path for executable code
and dynamically linked libraries (DLLs).  You can temporarily modify the path in a
command window session or permanently modify it for the whole system.

**Changing Path Via the Control Panel**

This method will modify the path for the whole system.  Running programs especially
open command windows will need to be restarted for this change to take effect.

A. Any version of Windows

    1. Press the "Windows Key."
    2. Start to type "Control Panel"
    3. Click on "Control Panel" in the start menu.
    4. Click "System and Security."
    5. Click "System."
    6. Click "Advanced system settings."
    7. Click "Environment Variables."

B. In Windows 10

    1. Press the "Windows Key."
    2. Start to type "Environment"
    3. Click on "Edit the system environment" in the start menu.
    4. Click "Environment Variables."

**Temporary Change in Command Window**

This method temporarily changes the path in just the active command window.
Once the command window is closed the change will be lost.

Just set the Path variable to include any additional directories you want to add to
the path.  Replace "added_directory" with the directory you want to add::

    set Path=%Path%;added_directory

.. _install_docker:

Installation using Docker
-------------------------
One way to install the IDAES PSE Framework is by using
the pre-built Docker_ image.

A Docker image is essentially an embedded
instance of Linux (even if you are using Windows or Mac OSX)
that has all the code for the IDAES PSE framework
pre-installed. You can run commands and Jupyter Notebooks in that
image. This section describes how to set up your system, get the
Docker image, and interact with it.

Install Docker on your system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. Install the community edition (CE) of Docker_ (website: https://docker.io).
#. Start the Docker daemon. How to do this will depend on your operating system.

      OS X
         You should install `Docker Desktop for Mac`_.
         Docker should have been installed to your Applications directory. Browse to it and click on it from there.
         You will see a small icon in your toolbar that indicates
         that the daemon is running.

      Linux
         Install Docker using the package manager for your OS. Then
         start the daemon. If you are using Ubuntu or a Debian-based Linux distro,
         the Docker daemon will start automatically once Docker is installed.
         For CentOS, start Docker manually, e.g., run ``sudo systemctl start docker``.

      Windows
        You should install `Docker Desktop for Windows`_.
        Docker will be started automatically.

.. _Docker Desktop for Mac: https://docs.docker.com/docker-for-mac/install/
.. _Docker Desktop for Windows: https://docs.docker.com/docker-for-windows/install/

Get the IDAES Docker image
^^^^^^^^^^^^^^^^^^^^^^^^^^
You need to get the ready made Docker image containing the source
code and solvers for the IDAES PSE framework. This image is available
for download at a URL like "https://s3.amazonaws.com/idaes/idaes-pse/idaes-pse-docker-``VERSION``.tgz",
where ``VERSION`` is the release version. See the Releases_ page on GitHub
for information about what is different about each version.

If you want the latest version, simply use the tag "latest" as the version number.
Thus, **clicking on this link will start a download of the latest version**:
`https://s3.amazonaws.com/idaes/idaes-pse/idaes-pse-docker-latest.tgz
<https://s3.amazonaws.com/idaes/idaes-pse/idaes-pse-docker-latest.tgz>`_.

.. _Releases: https://github.com/IDAES/idaes-pse/releases

Load the IDAES Docker image
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The image you downloaded needs to be loaded into your local Docker Installation
using the `Docker load`_ command, which from the command-line looks like
this:

    docker load < idaes-pse-docker-latest.tgz

.. _Docker load: https://docs.docker.com/engine/reference/commandline/load/

Run the IDAES Docker image
^^^^^^^^^^^^^^^^^^^^^^^^^^

To start the Docker image, use a graphical user interface or a console or shell
command-line interface.

From the command-line, if you want to start up the Jupyter Notebook server, e.g.
to view and run the examples and tutorials, then run this command:

.. code-block:: console

      $ docker run -p 8888:8888 -it idaes/idaes_pse
      ... <debugging output from Jupyter>
      ...
      Copy/paste this URL into your browser when you connect for the first time,
      to login with a token:
          http://(305491ce063a or 127.0.0.1):8888/?token=812a290619211bef9177b0e8c0fd7e4d1f673d29909ac254

Copy and paste the URL provided at the end of the output into a browser window
and you should get a working Jupyter Notebook. You can browse to the examples
directory under ``/home/idaes/examples`` and click on the Jupyter Notebooks to
open them.

To interact with the image directly from the command-line (console), you can run the
following command:

.. code-block:: console

      $ docker run -p 8888:8888 -it idaes/idaes_pse /bin/bash
      jovyan@10c11ca29008:~$ cd /home/idaes
      ...

