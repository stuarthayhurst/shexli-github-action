## Shexli GitHub Action
  - Run [Shexli](https://gitlab.gnome.org/Infrastructure/extensions-web/-/tree/master/shexli/shexli) against a GNOME extension, as a GitHub Action
    - Supports source directories and extension bundles
    - Supports ignoring rules, error thresholds, warnings thresholds and improved formatting
    - Improves compatibility with different configurations and versions

## Usage
  - Include the action in your workflow and tell it where to find the extension:
```
 - name: Run Shexli on the extension
   uses: stuarthayhurst/shexli-github-action@v1
   with:
     path: build/AlphabeticalAppGrid@stuarthayhurst.shell-extension.zip
```
  - By default, the action only fails on errors and uses the pinned Shexli version
  - Optionally configure ignored checks, maximum error count, maximum warning count and other settings

### Required config:
  - `path`: Path to the extension bundle or source directory

> [!NOTE]
> If possible, the built extension bundle (`.zip`) should be used, since this checks the actual package, not the state of the source code

### Optional config:
  - `use-latest-shexli`: Override the pinned version of Shexli with the latest release
    - Defaults to `false`
    - This may cause crashes, or change analysis results between workflow runs if Shexli updates
    - However, this saves updating to the latest `stuarthayhurst/shexli-github-action` to use new checks
  - `acceptable-error-threshold`: Maximum acceptable number of errors before failing the action
    - Defaults to `0`
    - Use `-1` to disable failing the action due to errors
  - `acceptable-warning-threshold`: Maximum acceptable number of warnings before failing the action
    - Defaults to `-1`
    - Use `-1` to disable failing the action due to warnings
  - `ignored-checks`: Space delimited string of rule IDs to ignored
    - Defaults to `""`
    - For example, use `'EGO-M-004 EGO-L-005'` to disable metadata GNOME Shell version checks and owned object release checks
    - A list of checks can be found [here](https://gitlab.gnome.org/Infrastructure/extensions-web/-/blob/master/shexli/shexli/spec.py)

## Examples
  - Check a built extension and fail only on errors:
```
 - name: Run Shexli on the extension
   uses: stuarthayhurst/shexli-github-action@v1
   with:
     path: build/AlphabeticalAppGrid@stuarthayhurst.shell-extension.zip
```
  - Check a built extension and never fail:
```
 - name: Run Shexli on the extension
   uses: stuarthayhurst/shexli-github-action@v1
   with:
     path: build/AlphabeticalAppGrid@stuarthayhurst.shell-extension.zip
     acceptable-error-threshold: -1
```
  - Check a built extension and fail on errors and warnings:
```
 - name: Run Shexli on the extension
   uses: stuarthayhurst/shexli-github-action@v1
   with:
     path: build/AlphabeticalAppGrid@stuarthayhurst.shell-extension.zip
     acceptable-warning-threshold: 0
```
  - Check an extension's source with the latest Shexli, ignoring metadata GNOME Shell version errors:
```
 - name: Run Shexli on the extension
   uses: stuarthayhurst/shexli-github-action@v1
   with:
     path: extension/
     use-latest-shexli: true
     ignored-checks: 'EGO-M-004'
```

## Licence
  - This project uses the MIT licence, found in `LICENCE.txt`
