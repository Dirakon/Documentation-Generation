{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
    }: 
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system}; in
        {
        devShells = 
          {
            default = pkgs.mkShell {
              buildInputs = [
                pkgs.nodejs_18
                pkgs.jdk17
                (pkgs.python3.withPackages (python-pkgs: [
                  python-pkgs.flask
                ]))
              ];
            };
          };
      });
}
