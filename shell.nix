with import <nixpkgs> {};
let
  
  # TODO combine those two
  mysage = sage.override { 
   	extraPythonPackages = ps: with ps; [ 
	 	prettytable 
		scipy
		sphinx
		furo
		autopep8
		pip
		pytest
	]; 
	requireSageTests = false;
  };

  my-python = pkgs.python3;
  mypython = my-python.withPackages (p: with p; [
	prettytable
	scipy
	sphinx
	furo
	pip
    autopep8
	sage
	pytest
  ]);
in
{ pkgs ? import <nixpkgs> {} }:

stdenv.mkDerivation {
  name = "cryptographic_estimators";
  src = ./.;

  buildInputs = [ 
    mypython
	mysage
	ripgrep
    nodePackages.pyright
	tree
  ];

  shellHook = ''
    export PIP_PREFIX=$(pwd)/_build/pip_packages
    export PYTHONPATH="$PIP_PREFIX/${mypython.sitePackages}:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    # unset SOURCE_DATE_EPOCH
  '';
}
