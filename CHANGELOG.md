# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- add `argon2-cffi` and `bcrypt` packages to project template.
- add `djplusconfig` command to generate config file called `djplus.json`.
- add `status` field to `User` model.
### Changed
- change `Session` model.
- rename `register` to `signup`.
### Backwards incompatible changes
- rename named url called `register` to `signup`.
- change `Session` model.
  1. run `python manage.py migrate auth 0001`
  2. update `djplus`
  3. run `python manage.py migrate`

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

[1.1.1]: https://github.com/githashem/djplus/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/githashem/djplus/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/githashem/djplus/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/githashem/djplus/releases/tag/v0.1.0
