{ pkgs }: {
  deps = [
    pkgs.glibcLocales
    pkgs.replitPackages.prybar-python310
    pkgs.replitPackages.stderred
  ];
}