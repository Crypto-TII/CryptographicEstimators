{ pkgs ? import <nixpkgs> {} }:
let
  myPython = pkgs.python313;
  pythonPackages = pkgs.python313Packages;
  pythonWithPkgs = myPython.withPackages (pythonPkgs: with pythonPkgs; [
    ipython
    pip
    setuptools
    virtualenv
    wheel
    black
    prophet
  ]);

  extraBuildInputs = with pkgs; [
    pythonPackages.pandas
    pythonPackages.numpy
    pythonPackages.prettytable
    pythonPackages.scipy
    pythonPackages.pytest
    pythonPackages.sympy
  ];
in
let
  buildInputs  = with pkgs; [
    clang
  ] ++ extraBuildInputs;
  lib-path = with pkgs; lib.makeLibraryPath buildInputs;
  shell = pkgs.mkShell {
    buildInputs = [
       # my python and packages
        pythonWithPkgs
        
        # other packages needed for compiling python libs
        pkgs.readline
        pkgs.libffi
        pkgs.openssl
        # needed for flint
        pkgs.ninja      
        pkgs.meson
        pkgs.pkg-config
        pkgs.gmp
        pkgs.mpfr
        pkgs.flint

  
        # unfortunately needed because of messing with LD_LIBRARY_PATH below
        pkgs.git
        pkgs.openssh
        pkgs.rsync
    ] ++ extraBuildInputs;
    shellHook = ''
        # Allow the use of wheels.
        SOURCE_DATE_EPOCH=$(date +%s)
        # Augment the dynamic linker path
        export "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${lib-path}"
        if test ! -d .venv; then
          virtualenv .venv
        fi
        source .venv/bin/activate
        export PYTHONPATH=$PYTHONPATH:`pwd`/$VENV/${myPython.sitePackages}/
        make install
    '';
  };
in shell
