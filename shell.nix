{ pkgs ? import <nixpkgs> {} }:

let
  libs = [
    pkgs.gcc.cc.lib
    pkgs.zlib
    pkgs.libGL
    pkgs.glib.out
    pkgs.gtk2.dev
  ];
in
pkgs.mkShell {
  buildInputs = [
    pkgs.uv
    pkgs.python312
    pkgs.python312Packages.numpy
    pkgs.python312Packages.tkinter
     (pkgs.python312Packages.opencv4.override {
      enableGtk2 = true;
      enableFfmpeg = true;
    })
  ] ++ libs;
  shellHook = ''
    for lib in ${pkgs.lib.concatStringsSep " " (map (p: "${p}/lib") libs)};
    do
      export LD_LIBRARY_PATH="$lib:$LD_LIBRARY_PATH"
    done
    echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH" >> .venv/bin/activate
    echo "export QT_QPA_PLATFORM_PLUGIN_PATH=$QT_QPA_PLATFORM_PLUGIN_PATH" >> .venv/bin/activate

  '';

} 
