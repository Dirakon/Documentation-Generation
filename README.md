# Documentation generation

## Init repo

```bash
./scripts/init.sh
```

## Dependencies

Dependencies (namely python, jdk and node) are specified through nix, so you can use it to get all the requirements. `nix develop` or `direnv allow`.

Alternatively, you could manually install these (note the specific versions used in flake.nix and flake.lock for better reproducability)

Javascript-level dependencies are specified normaly through npm, and their automatic local installation is already done in `./scripts/init.sh`

## How to use

### Setting up source code

First, you have setup source EO file. Replace the contents of `app.eo` with whatever code you want to document. Setup some placeholders in places where you want to generate documentation. Unless you want to modify the python scripts, the placeholder should be exactly `<STRUCTURE-BELOW-IS-TO-BE-DOCUMENTED>` (like it currently is in the example `app.eo`).

### Setting up prompts

Next, see already existing `./runs` folder. You can delete already existing folders there if you are not intrested in my specific prompts. Create a folder for each prompt you want to try, and place a file there (`prompt.txt`). `{code}` string will be replaced with the input EO code when sending requests to LLMs, but otherwise the prompt is sent as-is. You can create multiple folders for one prompt by adding a numeric suffix to (e.g., `_1`, `_2`, etc) - in the final grades this suffix will be discarded. Any folders/subfolders in `./runs` starting with dot (`.`) will be ignored when running scripts - this way you can "comment out" prompts, etc.

### Setting up models

By default, the scripts are setup to work with [openrouter.ai](https://openrouter.ai/). You need to modify `./scripts/llms_run.py` to specifiy the models you want to use (see `MODELS` variable). If you want to configure something other than openrouter, you need to modify the script accordingly.

### Generate documentations

If you want to proceed with the default Openrouter setup, you will need to have environmental variable `OPENROUTER_API_KEY` initialized before you attempt any generation. Afterwards, just run `./scripts/llms_run.py` and the configuration you specified in steps above will be respected. The outputs will be placed in the runs folder with respect to your specified structure (`runs/*prompt_folder*/*model_folder*/mapping.json`).

### Run doctests

By default, the program expects LLMs to provide outputs in the format: 
```
<explanation>
...SOME TEXT...
</explanation>
<doctest-code>
...SOME TEXT...
</doctest-code>
<doctest-stdin>
...SOME TEXT...
</doctest-stdin>
<doctest-output>
...SOME TEXT...
</doctest-output>
```

This is the format that you should ask LLMs to comply with. If you wish to run any extracted doctests (while providing specified corresponding stdin into them):

1. run `./scripts/doctests_generate.py` to extract the doctests into a ready-to-run structure. As output, in folders `runs/*prompt_folder*/*model_folder*/*index_of_place_in_code*/` the following files might be created (depending on which section were filled in the LLM outputs): `expected.txt`, `stdin.txt`, `app.eo`.
2. run `./scripts/doctests_run.py` to actually run the doctests. The outputs will be placed in the runs folder with respect to your specified structure (`runs/*prompt_folder*/*model_folder*/*index_of_place_in_code*/actual.txt`).

### Grade doctests

Run `./scripts/doctests_grade.py`. The outputs will be placed in the runs folder with respect to your specified structure (`runs/*prompt_folder*/*model_folder*/*index_of_place_in_code*/grade/doctest.txt`).

### Manually evaluate the quality of documentation

You can obviously grade manually without any scripts. The expected structure of grade files and their locations can be found in the scripts `./scripts/manual_grading.py`.

Or you can utilize the script. Modify it to use the editor of your choice. Run the script afterwards.

The outputs will be placed in the runs folder with respect to your specified structure (`runs/*prompt_folder*/*model_folder*/*index_of_place_in_code*/grade/manual.txt`).

### Collect grades

Run `./scripts/grades_collect.py`. The outputs will be placed in `./grade.csv`.
