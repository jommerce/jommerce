# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2022-01-30
### Removed
- Removed ```inject_app_default_settings```
- Removed ```auth``` app.

## [1.1.0] - 2022-01-01
### Added
- Customizable email length with ```AUTH_EMAIL_MAX_LENGTH```
- Active the 'coming soon' screen using ```COMING_SOON_MODE=True``` in ```settings.py``` file. (Default: **False**)
- Active the 'maintenance' screen using ```MAINTENANCE_MODE=True```. (Default: **False**)

### Changed
- Use ```AbstractBaseUser``` instead of ```AbstractUser```.
- Renamed ```set_app_settings``` to ```inject_app_default_settings```.

## [1.0.1] - 2021-12-16
### Fixed
- Fixed ```UniqueConstraint``` Error

## [1.0.0] - 2021-12-14
### Changed
- Upgrade ```Django``` to 4.0
- Use **environment variables** to read sensitive data instead of using the ```.secrets``` file.
- The ```email``` field is ```unique``` by default.
- The **project template** has changed.
### Added
- Add ```django-debug-toolbar``` to the development environment.
- Add **PostgreSQL Database Settings** to the production environment.
### Removed
- The ```.secrets``` file has been deleted.

## [0.1.1] - 2021-12-11
### Fixed
- Fixed generate ```SECRET_KEY```
- Fixed 'Page not found' error on ```Home Page```

## [0.1.0] - 2021-12-08
### Added
- Added ```Custom User Model```
- Added ```auth``` app.
- Added ```jommerce``` command.

[2.0.0]: https://github.com/jommerce/jommerce/releases/tag/v2.0.0
[1.1.0]: https://github.com/jommerce/jommerce/releases/tag/v1.1.0
[1.0.1]: https://github.com/jommerce/jommerce/releases/tag/v1.0.1
[1.0.0]: https://github.com/jommerce/jommerce/releases/tag/v1.0.0
[0.1.1]: https://github.com/jommerce/jommerce/releases/tag/v0.1.1
[0.1.0]: https://github.com/jommerce/jommerce/releases/tag/v0.1.0
