{ pkgs ? import <nixpkgs> {} }:
let
  myPython = pkgs.python311;
  pythonPackages = pkgs.python311Packages;
  pythonWithPkgs = myPython.withPackages (pythonPkgs: with pythonPkgs; [
    # This list contains tools for Python development.
    # You can also add other tools, like black.
    #
    # Note that even if you add Python packages here like PyTorch or Tensorflow,
    # they will be reinstalled when running `pip -r requirements.txt` because
    # virtualenv is used below in the shellHook.
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
    clang
  ];
in
import ./python-shell.nix { 
    extraBuildInputs=extraBuildInputs; 
    # extraLibPackages=extraLibPackages; 
    myPython=myPython;
    pythonWithPkgs=pythonWithPkgs;
  }

