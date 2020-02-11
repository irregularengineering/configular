# Configular

Config and secrets management

All files use INI format, as in:

```
[Section]
param1 = abc
param2 = 123
```

Read config parameter or secret with the following hierarchy:

  1. Environment variables, if available (defined as `{section}_{param}`)
  2. Override file, if available (typically stored outside of project)
  3. Config file (typically stored in project)

If a parameter is not found, `ParameterNotFoundException` is thrown, unless disabled in call to constructor.

## Install

```bash
pip install git+ssh://git@github.com/irregularengineering/configular.git
```

## Develop

### Install Requirements

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
pytest tests
```

### Run Linter

```bash
pylint configular
```
