# Public API

Even though there's no real privacy in Python, we want to try and make it clear to the user which parts of the API are _public_, _experimental_ and _private_.

## What "public" means

The **public API** is the set of names we commit to support across releases:

* **Import paths:** Names explicitly documented and re-exported at the package root or first-level submodules (e.g., `from pkg import run`, `from pkg.foo import bar`).

    !!! warning

        Being importable alone doesn’t make something public; anything underscored or undocumented is considered private.

* **Versioning contract:** Breaking changes to public API occur only in a major version bump (semantic versioning style).
  This means signatures, return types, and semantics won’t change except in a major release.
* **Deprecation first:** when something must change, we announce it in the docs/CHANGELOG and emit a `DeprecationWarning`.
  In exceptional cases where there is not straightforward deprecation pathway, we will also clearly announce this in the CHANGELOG, and provide a migration guide and/or tool along with an alpha release of the next major version.

## What "experimental" means

In some cases, we want to add a new feature and document its usage, but still leave room for changes to the API based on user feedback.
Such features will be **experimental** until declared stable.
Every section documenting such a feature will start with a clear warning that it is experimental and what this means:

1. the API might change between _minor_ releases, with **no deprecation window**.
2. the feature can be considered stable between _patch_ releases.

## What "private" means

Everything else is **private**, even though Python can technically import it:

* Any name or module **prefixed with `_`** (e.g. `pkg._internal`, `pkg._helpers`).
* Anything **not documented** or **not re-exported** from the package root or first-level submodules.
* Private code may change or disappear **without notice** between even patch releases, with **no deprecation window**.

## Conventions we follow

* **Underscore = private.** Any `_name` or `_module` is internal.
* **`__all__` as a whitelist.** Public modules define `__all__` to make intended exports explicit.
* **Root re-exports.** We re-export key classes/functions at first-level submodules so users get stable import paths.
* **No wildcard imports** in our docs/examples; they obscure what’s public.
* **Minimal surface.** We avoid exposing transitive dependencies or implementation details.

## Deprecation steps

1. Mark in docs/CHANGELOG with migration guidance and/or tool for automating migration.
2. Emit `warnings.DeprecationWarning` at call/import sites in case there is a deprecation pathway.
3. Remove for the next major release.
4. Provide an alpha/beta release so users can adapt while still supporting the previous major release for a reasonable amount of time.
