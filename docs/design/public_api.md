# Public API

Even though there's no real privacy in Python, we want to try and make it clear to the user which parts of the API are _public_ and _private_.

## What “public” means

The **public API** is the set of names we commit to support across releases:

* **Import paths:** Names explicitly documented or re-exported at the package root, plus documented first-level submodules (e.g., `from pkg import run`, `from pkg.foo import bar`). *Being importable alone doesn’t make something public; anything underscored or undocumented is considered private.*
* **Stable behavior and types:** signatures, return types, and semantics won’t change except in a major release.
* **Deprecation first:** when something must change, we announce it in the docs/CHANGELOG and emit a `DeprecationWarning`.
* **Versioning contract:** breaking changes to public API occur only in a major version bump (semantic versioning style).

## What “private” means

Everything else is **private**, even though Python can technically import it:

* Any name or module **prefixed with `_`** (e.g. `pkg._internal`, `pkg._helpers`).
* Anything **not documented** and **not re-exported** from the package root or documented first-level submodules.
* Private code may change or disappear **without notice** between releases, with **no deprecation window**.

## Conventions we follow

* **Underscore = private.** Any `_name` or `_module` is internal.
* **`__all__` as a whitelist.** Public modules define `__all__` to make intended exports explicit.
* **Root re-exports.** We re-export key classes/functions at first-level submodules so users get stable import paths.
* **No wildcard imports** in our docs/examples; they obscure what’s public.
* **Minimal surface.** We avoid exposing transitive dependencies or implementation details.

## Deprecation steps

1. Mark in docs/CHANGELOG with migration guidance.
2. Emit `warnings.DeprecationWarning` at call/import sites.
4. Remove in the next major release.
