with import <nixpkgs> {};
let
  
  # TODO combine those two
  mysage = sage.override { 
   	extraPythonPackages = ps: with ps; [ 
	 	prettytable 
		scipy
		sphinx
		furo
		pip
	]; 
	requireSageTests = false;
  };

  my-python = pkgs.python3;
  python-with-my-packages = my-python.withPackages (p: with p; [
	prettytable
	scipy
	sphinx
	furo
	pip
	sage
  ]);
in
{ pkgs ? import <nixpkgs> {} }:

stdenv.mkDerivation {
  name = "cryptographic_estimators";
  src = ./.;

  buildInputs = [ 
  	python-with-my-packages
	mysage
	ripgrep
    nodePackages.pyright
	tree
  ];
}
