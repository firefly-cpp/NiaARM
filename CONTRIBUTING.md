# Contributing to NiaARM
:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

## Code of Conduct
This project and everyone participating in it is governed by the [NiaARM Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [iztok.fister1@um.si](mailto:iztok.fister1@um.si).

## How Can I Contribute?

### Reporting Bugs
Before creating bug reports, please check existing issues list as you might find out that you don't need to create one. When you are creating a bug report, please include as mAll details as possible in the [issue template](.github/templates/ISSUE_TEMPLATE.md).

### Suggesting Enhancements

Open new issue using the [feature request template](.github/templates/FEATURE_REQUEST.md).

### Pull requests

Fill in the [pull request template](.github/templates/PULL_REQUEST.md) and make sure your code is documented.

## Setup development environment

### Requirements

* uv: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

After installing uv and cloning the project from GitHub, you should
run the following command from the root of the cloned project:

```sh
uv sync --dev
```

All the project's development dependencies should be installed and the project ready for further development.

### Dependencies

| Package      | Version  | Platform |
|--------------|:--------:|:--------:|
| niapy        | \>=2.6.1 |   All    |
| numpy        | \>=2.3.5 |   All    |
| pandas       | \>=2.3.3 |   All    |
| nltk         | \>=3.9.2 |   All    |
| scikit-learn | \>=1.8.0 |   All    |
| plotly       | \>=6.5.0 |   All    |

#### Development dependencies

| Package         |  Version  | Platform |
|-----------------|:---------:|:--------:|
| pytest          | \>=9.0.0  |   All    |
| pytest-cov      | \>=7.0.0  |   All    |
| pytest.randomly | \>=4.0.1  |   All    |
| pre-commit      | \>=4.5.0  |   All    |
| ruff            | \>=0.14.9 |   All    |

#### Documentation Dependencies

| Package              | Version  | Platform |
|----------------------|:--------:|:--------:|
| sphinx               | \>=8.2.3 |   All    |
| sphinx-rtd-theme     | \>=3.0.2 |   All    |
| sphinxcontrib-bibtex | \>=2.6.5 |   All    |

## Testing

Manually run the tests:

```sh
uv run pytest
```

## Documentation

Build the documentation:

```sh
uv sync --group docs
uv run sphinx-build ./docs ./docs/_build
```
