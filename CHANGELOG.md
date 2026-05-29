# Changelog

## v3.0.0a4

### 💥 Breaking changes

* Units: switch to QE-native units for outputs [[31640ae](https://github.com/aiidateam/qe-tools/commit/31640ae1532d986d7175aa3849fc157918e7eec8)]

### 📚 Documentation

* `pint`: add pint extra to default installation + notes [[ef23e7c](https://github.com/aiidateam/qe-tools/commit/ef23e7c472b103d7a8f955fb1ebc994fd958c5da)]
* Getting started: update content for latest release [[51d056e](https://github.com/aiidateam/qe-tools/commit/51d056e225fa2831089a4e32b7a4a29fec7764eb)]

## v3.0.0 - alpha

> [!WARNING]
> This is the alpha release (now at `3a`) of the new `qe-tools` package.
> The API is getting more stable, but will _very_ likely still have breaking changes.
> Not all commits are shown below, only updates since re-scaffolding the package.
> Due to the large revamp and almost-empty previous `qe-tools`, no migration guide or summary of the changes will be provided: the documentation will serve that purpose.

### 💥 Breaking changes

* `outputs`: Migrate fields to `Annotated[T, Spec(...)]` [[d72a645](https://github.com/aiidateam/qe-tools/commit/d72a645cc7d04e92c9606fb5fa7750cb84624769)]

### 📦 Dependency updates

* extras: add optional depedencies for supported converter libraries [[8e74393](https://github.com/aiidateam/qe-tools/commit/8e743931f9e2936a311ca172f8711d2175dd7b23)]
* Remove `scipy` dependency [[3c6ba79](https://github.com/aiidateam/qe-tools/commit/3c6ba79be19ea616f48e6fb6518278f937c98a57)]

### ❌ Deprecations

* `_elements.py`: remove module [[2b6e4c7](https://github.com/aiidateam/qe-tools/commit/2b6e4c7c2ae330150f028d4dcce124cfb1845d7f)]
* Remove old empty "qe converter" module [[0df5e81](https://github.com/aiidateam/qe-tools/commit/0df5e81fb58036aad00b66ec0b322b39c794c7e3)]
* ASE: remove old converter code [[73b87cc](https://github.com/aiidateam/qe-tools/commit/73b87cc2b72a0cba3ee0d6b41ac64e6d8b8aac21)]
* Scope: drop support for QE versions <7.0 [[c631f8a](https://github.com/aiidateam/qe-tools/commit/c631f8a9ecc925d28254ec90c53bc1a57e92c356)]

### ✨ New features

* `PwOutput`: Parse `ecutwfc` and `ecutrho` from stdout as fallback [[f5edffc](https://github.com/aiidateam/qe-tools/commit/f5edffce456d599195d6b40f5c0e118e6a1a8ca1)]
* `PwOutput`: Parse `forces` from stdout as fallback [[269ac9d](https://github.com/aiidateam/qe-tools/commit/269ac9d15f2263e1f19eb62238472da8dddd6e45)]
* `PwOutput`: Parse k-points from stdout as fallback [[22237a1](https://github.com/aiidateam/qe-tools/commit/22237a1aa19a069d48008e4613af4011bcf961c1)]
* `PwOutput`: add `wall_time` and `volume` outputs [[c61b81f](https://github.com/aiidateam/qe-tools/commit/c61b81f0517b52f12d074a1b2f75a477a6dc3665)]
* `BandsOutput`: parse `.dat.gnu` for cumulative k-path distances [[feb1437](https://github.com/aiidateam/qe-tools/commit/feb143754cc0cc1bce8f002673a8f852b30aef02)]
* `PwOutput`: gate `total_energy` on the calculation type [[2097eff](https://github.com/aiidateam/qe-tools/commit/2097eff215332ccec92755ea0a3af9af5d2f19c0)]
* `ProjwfcOutput`: add output class for projwfc.x [[4e4885f](https://github.com/aiidateam/qe-tools/commit/4e4885f1022153983fcc4ead2d541319945c93de)]
* `BandsOutput`: add output class for bands.x [[02f6d96](https://github.com/aiidateam/qe-tools/commit/02f6d960e4c68f81f1d90f4587aaf88c5b9a2728)]
* `PwOutput`: add Specs for bands, magnetism, and HOMO/LUMO [[0aba951](https://github.com/aiidateam/qe-tools/commit/0aba951f4a5c00c55122b9b473b597a4003e7bee)]
* `outputs`: Annotate fields with `Unit` markers [[365eaaf](https://github.com/aiidateam/qe-tools/commit/365eaaf633dd7411b05b407e877daee43c908953)]
* `PwOutput`: Add `parameters` sub-mapping of run settings [[5ff26ad](https://github.com/aiidateam/qe-tools/commit/5ff26ad46f77aedfebda28dc44af820c63c7d745)]
* `BaseOutput`: Add `SubMapping` for nested output namespaces [[a686eda](https://github.com/aiidateam/qe-tools/commit/a686edab0cd221564cc18edb2b466e12a384c97f)]
* `PwOutput`: Add k-point outputs [[abe6a00](https://github.com/aiidateam/qe-tools/commit/abe6a00f011dbabb6426e1ed1dda31c5e6456223)]
* `PwOutput`: Add `number_of_bands` [[ed3813d](https://github.com/aiidateam/qe-tools/commit/ed3813df22ace93ef615d7d75ed9153a3b292396)]
* `PwOutput`: Add `fermi_energy_up` and `fermi_energy_down` [[80662eb](https://github.com/aiidateam/qe-tools/commit/80662ebc60182e1b3160221ed295de02294f8e57)]
* `PwOutput`: add total energy output [[e17811a](https://github.com/aiidateam/qe-tools/commit/e17811a1752d9107a2988d01ed2f59213b63df4e)]
* `PwXMLParser`: add `qes_250521.xsd` for QE 7.5 [[7e667a6](https://github.com/aiidateam/qe-tools/commit/7e667a6e7acc11e8ded9b9a713f4548dc3bb314e)]
* `BaseOutput`: add the `get_output_dict` method [[685120f](https://github.com/aiidateam/qe-tools/commit/685120f348cdd168e4fe43da3cbeb6040650e951)]
* `AiiDAConverter`: add `full_dos` conversion [[4a012d5](https://github.com/aiidateam/qe-tools/commit/4a012d5cab6d8df7e6cc72effcdc54926188c14c)]
* `DosOutput`: add first version [[fb70654](https://github.com/aiidateam/qe-tools/commit/fb706544b0f41dbbb6fc1d14d63d8566a0d53b71)]
* `PwOutput`: add `forces` and `stress` outputs [[3f9ae23](https://github.com/aiidateam/qe-tools/commit/3f9ae23e30b954f89db25dedc6c0bb68bd03b3c7)]
* `BaseOutput`: add `outputs` namespace [[0fcc35d](https://github.com/aiidateam/qe-tools/commit/0fcc35d6d61341e19a470e0f72627ffd2a3cc2f9)]
* `BaseOutput`: add `list_outputs` method [[1e3b38c](https://github.com/aiidateam/qe-tools/commit/1e3b38cf3a4f58c9af529f70bc4418961c6372bb)]
* Parsers: make classes stateless [[516b724](https://github.com/aiidateam/qe-tools/commit/516b7240d4d640aa529688d80338428ce4726ace)]
* `BaseOutput`: add `get_output_from_spec` method [[252ffea](https://github.com/aiidateam/qe-tools/commit/252ffea63898fd39e798f0951bbcb812ba9e9d82)]
* Converters: add basic design implementation [[1303e77](https://github.com/aiidateam/qe-tools/commit/1303e77575bcdfbf9a13ed62dff949ab847dd79f)]
* `PwOutput`: add `from_files` method [[9433796](https://github.com/aiidateam/qe-tools/commit/9433796a885190c7358ddd23a4c6d9de1fec4960)]
* 🧪 Add missing `qes-1.0.xsd` schema and XML parsing tests [[907187a](https://github.com/aiidateam/qe-tools/commit/907187aa56b8d9723212f37f45ad8d68bf46d1fc)]
* Add basic `stdout` parsing functionality [[13664f3](https://github.com/aiidateam/qe-tools/commit/13664f3ebcb762b5c8e35bf77266b933fd3be04e)]
* First draft of `PwParser` [[aafcd28](https://github.com/aiidateam/qe-tools/commit/aafcd2805e58b4dd34fd7f2df939157f8388b822)]
* Add conversion constants for a.u. to GPa [[cf00438](https://github.com/aiidateam/qe-tools/commit/cf0043865a7d3d64a9edb8aa11ac2e70c6c423ef)]

### 👌 Improvements

* `BaseOutput`: narrow `to` type + improve docstrings [[91aae42](https://github.com/aiidateam/qe-tools/commit/91aae42b70af21ddbc656a26aa50e5b36e0ef6b6)]
* `BaseOutput`: Add typing + doc to outputs namespace [[0aaa634](https://github.com/aiidateam/qe-tools/commit/0aaa634257564fbf668fe965346cbe626cd7173c)]
* `PwOutput`: convert `fermi_energy` to eV [[74eabcb](https://github.com/aiidateam/qe-tools/commit/74eabcb79e2f6b71fa302da7aafbb7d4c23a4338)]
* `BaseOutput`: add `only_available` argument to `list_outputs` [[913ddec](https://github.com/aiidateam/qe-tools/commit/913ddec02c676474436a249fd36e0048becfcada)]
* Extras: improve/add error messages when extra is not installed [[3649b9b](https://github.com/aiidateam/qe-tools/commit/3649b9bf3f1c77e0372faa77482f65fb02d833d2)]
* `PwOutput`: improve signature/docstring of `get_output` [[1da984a](https://github.com/aiidateam/qe-tools/commit/1da984af46f57d680da0b9f89ca3ef48ddc6f9bf)]
* `PwXMLParser`: improve error message for XML parsing failure [[50befd8](https://github.com/aiidateam/qe-tools/commit/50befd8f8cd0c1b2d5798d9f040f6619840d1df6)]
* `PwOutput`: move `stdout` into separate key in `raw_output` [[c501943](https://github.com/aiidateam/qe-tools/commit/c501943711c2c514796cf32e123613b66c09cb15)]
* `BaseConverter`: remove `numpy` dependency [[e7e042a](https://github.com/aiidateam/qe-tools/commit/e7e042ae348694968d3c950bd3460cc02042767b)]
* `BaseOutput`: rename `outputs` to `raw_outputs` [[a831529](https://github.com/aiidateam/qe-tools/commit/a8315293292f779473fdea02be40afae3abe01f5)]
* `BaseOutputFileParser`: expand `from_file` `file` types [[e968246](https://github.com/aiidateam/qe-tools/commit/e9682466ae7ccb16cb1d72739356a07432cbf60f)]
* `PwOutput`: add to `outputs.__all__` [[ba3ab41](https://github.com/aiidateam/qe-tools/commit/ba3ab4199c6207adf1c9cc9ebcf1b7ea708603df)]
* Remove the `executable` input from the output classes [[4d2885d](https://github.com/aiidateam/qe-tools/commit/4d2885d6e9e10d5629c42a0a13c5832e97f21a5d)]
* `PwOutput`: Small changes to code [[4e2354e](https://github.com/aiidateam/qe-tools/commit/4e2354e64dc9d9d08c8884bf27d700ce13b829b6)]
* `CHANGELOG.md`: remove superfluous title [[11f7a92](https://github.com/aiidateam/qe-tools/commit/11f7a9227ec5d4873375147a43fb107ad095a5e2)]

### 🐛 Bug fixes

* `PwOutput`: fix `StopIteration` error when XML is missing [[235edf6](https://github.com/aiidateam/qe-tools/commit/235edf6ebf9e250e719ccc32ac367df2f4dc3718)]
* `BaseOutput.get_output`: properly return base output [[e72c652](https://github.com/aiidateam/qe-tools/commit/e72c652f2b9abe159b0ca8a96ad077eb2f7b9432)]
* Converters: fix atomic species spec [[17c6258](https://github.com/aiidateam/qe-tools/commit/17c625878cfeb2ab2f5ebff50d5506a988397f42)]
* `ELEMENTS`: make available from root import [[36be03c](https://github.com/aiidateam/qe-tools/commit/36be03cb00a351c11a63b8e0d28564a3e6c0c88b)]
* `PwOutput.from_dir`: improve XML path finding [[99854b2](https://github.com/aiidateam/qe-tools/commit/99854b268f985b369f761efc3cdd3664a842af2d)]

### 📚 Documentation

* `docs/design/outputs`: fix link to `dough` design docs [[71fe097](https://github.com/aiidateam/qe-tools/commit/71fe097e39a9a6cdd2e2eb18eb59e1cab8ac160e)]
* `docs/design`: Rewrite outputs page for post-dough split [[d717d29](https://github.com/aiidateam/qe-tools/commit/d717d291e0feb08f0e20d6e6c6c2de8e89ef4456)]
* Design: remove outdated available note [[8ccf3c9](https://github.com/aiidateam/qe-tools/commit/8ccf3c9615b5416576de4c049014da0a603a7d35)]
* Getting started: clean up and remove input content [[06cde32](https://github.com/aiidateam/qe-tools/commit/06cde3230451ec62160641cd571987ddde54cfbc)]
* `BaseOutput`: improve docstrings [[06e6d3d](https://github.com/aiidateam/qe-tools/commit/06e6d3dae3708b2f2676d2e968fb5d74faf16e18)]
* Design: update "user interface" [[3aa19f0](https://github.com/aiidateam/qe-tools/commit/3aa19f0097608754ed2e49300effe6adcaae8984)]
* Scope: reorganise and polish [[80a523e](https://github.com/aiidateam/qe-tools/commit/80a523ee3ca07ea19a1ffccf348889be093e36a7)]
* Getting started: add some notes/warnings + polish [[3d24dec](https://github.com/aiidateam/qe-tools/commit/3d24dec6105e09c7afa4a0cde6c3f699c875f089)]
* Design: add page with some basic notes on units [[50e715f](https://github.com/aiidateam/qe-tools/commit/50e715f49deff677697acacb2b0e30d756861e65)]
* Design: reorder pages [[4b960a5](https://github.com/aiidateam/qe-tools/commit/4b960a533c2823b9de9e3b7bfe64f9fa8f230e70)]
* Road map: update priorities [[6e874e2](https://github.com/aiidateam/qe-tools/commit/6e874e2ccd47b428371d28ee28e017d1d31cbe9a)]
* Getting started: update and polish text [[99df788](https://github.com/aiidateam/qe-tools/commit/99df7887776626572edac2e1cbd11684750f7fd5)]
* Design: polish outputs discussion [[bd68c18](https://github.com/aiidateam/qe-tools/commit/bd68c18b9b1645bfdc084dcafa7bb4bfec016039)]
* Move some smaller notes into issues [[c89602f](https://github.com/aiidateam/qe-tools/commit/c89602f21f5a1b46fe21d335b496a05ef1ae9d3a)]
* Design: add two quick notes [[7d89aa3](https://github.com/aiidateam/qe-tools/commit/7d89aa399aaf48bb1f3ca5d498e6247444894477)]
* Design: Improve/update quick notes [[4f4e7c2](https://github.com/aiidateam/qe-tools/commit/4f4e7c2a44f4ab2159c17c9d863f62bde6f28f88)]
* Scope: add page and move quick notes [[146932e](https://github.com/aiidateam/qe-tools/commit/146932ec1cbc0b5a028bdb635b76ceca806d0e9a)]
* Developer: add warning and correct `<GITHUB REPO>` [[8b10ac1](https://github.com/aiidateam/qe-tools/commit/8b10ac1e62ea887e194a18c391985f0f231d1211)]
* Design: add notes on public/private API [[067ab11](https://github.com/aiidateam/qe-tools/commit/067ab11c670c454a237adbcacab66565ef6df563)]
* `README.md`/landing: add very rough priorities "road map" [[40936af](https://github.com/aiidateam/qe-tools/commit/40936afea9b68fb1d68cb7c3be6edb937d57df63)]
* Inputs: update link to input "prototype" [[9671b1a](https://github.com/aiidateam/qe-tools/commit/9671b1ad1a9fc9ed1cd4120cf787d4e98806d2aa)]
* Install/quick start: update and add warnings [[9392d68](https://github.com/aiidateam/qe-tools/commit/9392d68544a96ee0b846c86d3569e6a14cb422c2)]
* Add `nav` to MkDocs configuration [[a56cd7e](https://github.com/aiidateam/qe-tools/commit/a56cd7e6839faefb90ec7bec128b585574fc6278)]
* Improve/reorganise design docs [[b97d970](https://github.com/aiidateam/qe-tools/commit/b97d9702e1bf792227f9c76c1a88f9853f2c7155)]
* [WIP] Add some basic documentation and design notes [[785f32c](https://github.com/aiidateam/qe-tools/commit/785f32ce9f9f0694367fa5abed8ff882a28357e2)]

#### Developer

🔄 Refactor

* `outputs`, `converters`: Consume base machinery from `dough` [[f9aa26d](https://github.com/aiidateam/qe-tools/commit/f9aa26d8d17aa54753a2759f5b2a9bcb21c0ef96)]
* `parsers`: Extract `BaseStdoutParser` to dedicated module [[1fbce19](https://github.com/aiidateam/qe-tools/commit/1fbce19f9380500646eab181b0d9610098c9af41)]
* `BaseOutput`: Make converter dispatch QE-agnostic [[9fe220b](https://github.com/aiidateam/qe-tools/commit/9fe220b35ae23f581431411754ec5cbc885eebf9)]
* `PwOutput`: use `CONSTANTS.hartree_to_ev` for forces [[c4bd3a7](https://github.com/aiidateam/qe-tools/commit/c4bd3a731b466f7d304a7514b5a0d3061c7b6656)]
* `PwOutput`: move `get_output` to parent class [[157ca95](https://github.com/aiidateam/qe-tools/commit/157ca956b74ca86bc28b6969e320c6106871fba4)]
* Outputs: separate extraction from conversion [[9babaf4](https://github.com/aiidateam/qe-tools/commit/9babaf4a1e43abed9a0125642d3bd8d12fe77924)]

🧪 Tests

* `tests`: Delegate shared fixtures to `dough.testing` plugin [[bda3e2b](https://github.com/aiidateam/qe-tools/commit/bda3e2bed9efbcdb677ea9f014138bcdd559a5fc)]
* `test_default_xml`: use `get_output_dict()` method [[2c562c9](https://github.com/aiidateam/qe-tools/commit/2c562c9edeb13f8f51ce4f9167fd071bbbccdafd)]
* `PwXMLParser`: add tests for QE 7.5 [[062bea2](https://github.com/aiidateam/qe-tools/commit/062bea2dcfbc2301e3b84e882a2791cf89a86648)]
* `BaseOutput`: use minimal test class instead of `PwOutput` [[3373c92](https://github.com/aiidateam/qe-tools/commit/3373c9226299886db6b833e7a7d3e7abc5a6ee5b)]
* `PwOutput`: adapt regression so base outputs are located [[e7bc432](https://github.com/aiidateam/qe-tools/commit/e7bc4328632c4d9a7a5d937a86c8bdfb58b4569e)]
* Clean up test docstrings [[ca70082](https://github.com/aiidateam/qe-tools/commit/ca70082ab363ed2fcc9af9f39e8d3b787bb74f34)]
* Remove empty `parsers/test_pw.py` file [[113dc25](https://github.com/aiidateam/qe-tools/commit/113dc25e39edaf03798e5e6f541b8d29651f6a14)]
* `json_serializer`: extend functionality and reach [[86eb03e](https://github.com/aiidateam/qe-tools/commit/86eb03ec262012be34bc2985c1ff40dcd1c97eac)]
* `PwOutput`: add tests for structure and Fermi energy [[f4f8144](https://github.com/aiidateam/qe-tools/commit/f4f81443d4487bfbc3be8236a57cb11d9d1d968d)]

🔧 DevOps

* `copier`: update package template to v0.16.0 [[fcad0d3](https://github.com/aiidateam/qe-tools/commit/fcad0d34211dd8d867fa2a2396ca2a60f0a8624c)]
* `.gitignore`: Ignore `local/` scratch directory [[b5a8d00](https://github.com/aiidateam/qe-tools/commit/b5a8d002b7b7834807217f9c9c78e1b57b251551)]
* pre-commit: Enable `mypy` type-check on `outputs` [[2629559](https://github.com/aiidateam/qe-tools/commit/262955988ff813d8db364bb296af20394eb91e02)]
* `copier`: update package template to v0.12.1 [[3ea6fd6](https://github.com/aiidateam/qe-tools/commit/3ea6fd6f919b351d5b28eced9f1f148ce761b817)]
* `copier`: update package template to v0.12.0 [[508203b](https://github.com/aiidateam/qe-tools/commit/508203b475bd5fea116ed7186b4ee385f202175f)]
* `copier`: update package template to v0.11.1 [[c4ee179](https://github.com/aiidateam/qe-tools/commit/c4ee179a04fe2d84d398c30cc2a6bf02eb6c9fc5)]
* Clean up old linting comments [[e180576](https://github.com/aiidateam/qe-tools/commit/e180576fecc60632a3d103d807d418f12fed61fc)]
* Add `.jupytext-sync-ipynb` to `.gitignore` [[d4b0ebe](https://github.com/aiidateam/qe-tools/commit/d4b0ebebc9abe81e07c9baa5ff2eded871622952)]
* Update package template to v0.10.0 [[e69b38d](https://github.com/aiidateam/qe-tools/commit/e69b38de928b865657c95018f241d8e821ef9a42)]
* Update package template to v0.9.0 [[386d3d0](https://github.com/aiidateam/qe-tools/commit/386d3d0426a68ac4f2177e8fd6650c77aef19e80)]
* Update package template to v0.8.0 [[a30b7b3](https://github.com/aiidateam/qe-tools/commit/a30b7b3a5e2849a03235665107e32a188cfffe36)]
* Run new Hatch `precommit` setup [[2f3b6a3](https://github.com/aiidateam/qe-tools/commit/2f3b6a3354653efc80aca0a4b332142f739ff6da)]
* Sync package devops to `python-copier` template [[c4ea572](https://github.com/aiidateam/qe-tools/commit/c4ea57208ade680990a4720741ab009df3aeea90)]
* Update dependencies; fix `pre-commit` & tests [[f2b60c7](https://github.com/aiidateam/qe-tools/commit/f2b60c7a0ec72494bfa94114f64ac9b4c0185cc9)]
* Drop Python 3.8 support; add Python 3.12, 3.13 [[84d5a02](https://github.com/aiidateam/qe-tools/commit/84d5a02cf227b923da99024146fcc7cc31c6ba4a)]
* Add `update_changelog.py` script [[5d7f7f1](https://github.com/aiidateam/qe-tools/commit/5d7f7f11754434cba2565e9bb3c1dc0622822498)]
* Devops: Switch to `ruff` for linting/formatting [[f447512](https://github.com/aiidateam/qe-tools/commit/f4475124ac61684d090a3d7b70c8520cc376dff2)]

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
