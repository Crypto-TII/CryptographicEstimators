{ pkgs ? import <nixpkgs> {}
, extraBuildInputs ? []
, myPython ? pkgs.python3
, extraLibPackages ? []
, pythonWithPkgs? myPython
 }:
let
  buildInputs  = with pkgs; [
      clang
      llvmPackages_16.bintools
      rustup
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
  
        # unfortunately needed because of messing with LD_LIBRARY_PATH below
        pkgs.git
        pkgs.openssh
        pkgs.rsync
    ] ++ extraBuildInputs;
    shellHook = ''
        # Allow the use of wheels.
        SOURCE_DATE_EPOCH=$(date +%s)
        # Augment the dynamic linker path
        export "LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${lib-path}:${pkgs.stdenv.cc.cc.lib}/lib/"
        if test ! -d .venv; then
          virtualenv .venv
        fi
        source .venv/bin/activate
        export PYTHONPATH=$PYTHONPATH:`pwd`/$VENV/${myPython.sitePackages}/
    '';
  };
in shell
