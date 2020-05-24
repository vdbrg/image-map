with import <nixpkgs> {};
with pkgs.python36Packages;

stdenv.mkDerivation {
  name = "img_to_tile_layer";
  buildInputs = [ 
    python36Full
    python36Packages.pip
    mypy
    python36Packages.Wand
  ];
}
