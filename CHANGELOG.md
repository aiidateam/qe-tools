## `v2.3.0` - 2024-11-21

### ✨ New features

* ✨ Add conversion constants for a.u. to GPa [[cf00438](https://github.com/aiidateam/qe-tools/commit/cf0043865a7d3d64a9edb8aa11ac2e70c6c423ef)]

### 👌 Improvements

* 👌 `CHANGELOG.md`: remove superfluous title [[11f7a92](https://github.com/aiidateam/qe-tools/commit/11f7a9227ec5d4873375147a43fb107ad095a5e2)]

### 🔧 Maintenance

* 🔧 Add `update_changelog.py` script [[5d7f7f1](https://github.com/aiidateam/qe-tools/commit/5d7f7f11754434cba2565e9bb3c1dc0622822498)]
* 🔧 Devops: Switch to `ruff` for linting/formatting [[f447512](https://github.com/aiidateam/qe-tools/commit/f4475124ac61684d090a3d7b70c8520cc376dff2)]


## `v2.2.0` - 2024-02-02

### Features
- Add marda-extractors support for PW and CP input files [[8c50b4c]](https://github.com/aiidateam/qe-tools/commit/8c50b4c6e203b1ccea7dd90f384c2e365e74dd5c)

### Fixes
- Fix the regex `NUMBER_PATTERN` in `_input_base.py`` [[c0e3c51]](https://github.com/aiidateam/qe-tools/commit/c0e3c516be16731923d8152ea1b08318a32b7aed)
- Fix input parser for cell parameters with integers [[efe4472]](https://github.com/aiidateam/qe-tools/commit/efe4472eef52caa9c9e87a58f7777ac20bb6ed96)

### Dependencies
- Pin `pytest~=7.0` [[d0f8124]](https://github.com/aiidateam/qe-tools/commit/d0f8124d5a48c85ae07296c37e93aa58fa35bcbe)


## `v2.1.0` - 2023-09-27

### Fixes
- Allow for empty strings in `str2val` [[379c8c0]](https://github.com/aiidateam/qe-tools/commit/379c8c0047f21e04e54c206a6279e467a3403dd5)

### Dependencies
- Add support for Python 3.10 and 3.11 [[5f1f458]](https://github.com/aiidateam/qe-tools/commit/5f1f458230e7c6db4bae5df254c67a7c0a606914)
- Drop support for Python 3.6 and 3.7 [[09d9e7a]](https://github.com/aiidateam/qe-tools/commit/09d9e7a71d8294b5191110118b58a6f6129ac8eb)
- Dependencies: Update `pylint~=2.16.0` [[7a42f10]](https://github.com/aiidateam/qe-tools/commit/7a42f10b58b602f85522266cf49f699106323ed5)

### Devops
- Update the `setup-python` action for CI and CD [[e77d6dd]](https://github.com/aiidateam/qe-tools/commit/e77d6ddeb6d0f435f6abe3128a62f75c796c9433)
- Update `isort==5.12.0` requirement [[3accb27]](https://github.com/aiidateam/qe-tools/commit/3accb27f7435485b030a9978a7cd2c358e5268bc)
