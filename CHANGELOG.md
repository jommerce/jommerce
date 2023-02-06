# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [3.0.0] - 2023-2-3
### Added
- Add initial djplus project.
- Add `ip` field to `Session` model.
- Add `status` field to `User` model.
### Fixed
- Executable command line without `tomllib` library.
### Changed
- Rename `djplus` command line to `dj`.
- Rename `djplusconfig` command line to `djonfig`.
### Breaking Change
- Change the name of the package from `djplus` to `dj`.


## [2.1.0] - 2022-10-27
### Added
- add initial app called `blog`.
- add `expire_date` and `data` fields to `Session` model.
### Changed
- Use `djplus.toml` file instead of `djplus.json` file to manage configurations.


## [2.0.0] - 2022-07-25
### Added
- add `argon2-cffi` and `bcrypt` packages to project template.
- add `djplusconfig` command to generate config file called `djplus.json`.
- Implement `login`, `logout` and `signup` views in `auth` app.
### Breaking Change
- Change `User` model from `auth` app.
- Change `Session` model from `auth` app.
- Remove all migration files and create another one.


## [1.1.1] - 2022-06-29
### Fixed
- Fixed the error of uninstalled packages with the help of `requirements` in the project template.
### Changed
- Default `DEFAULT_AUTO_FIELD` to `AutoField` in the project template.
- Run the server with local settings in the project template.


## [1.1.0] - 2022-06-25
### Added
- add initial app called `auth`
    - Customizable password hashers
    - Customizable password validators
    - Customizable username validators


## [1.0.0] - 2022-04-12
### Added
- add `djplus` command to generate the project.


## [0.1.0] - 2022-04-09
Initial release


[2.1.0]: https://github.com/githashem/djplus/compare/v2.1.0...v3.0.0
[2.1.0]: https://github.com/githashem/djplus/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/githashem/djplus/compare/v1.1.1...v2.0.0
[1.1.1]: https://github.com/githashem/djplus/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/githashem/djplus/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/githashem/djplus/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/githashem/djplus/releases/tag/v0.1.0
