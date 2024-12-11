# Changelog

## [0.0.1] - 05/12/2024
### Added
- Initial commit & creation of repository file structure

## [0.0.2] - 07/12/2024
### Added
- Initiated apps for each component
- Created models for each component
- Created serializers for each component
- Created admin account handling using Django authenticate library

## [0.0.3] - 09/12/2024
### Added
- Created unary relationship between applicants for applicant-household member relationships
### Updated
- Updated accounts component to allow logout

## [0.0.4] - 09/12/2024
### Added
- Created people table for all individuals as a parent of applicants & household member 
### Updated
- Updated applicants component to replace unary relationship between applicants with a separate household member table to prevent household members being treated as applicants

## [0.0.5] - 10/12/2024
### Added
- Redefined handling of scheme fields to make validation easier
- Created logic for schemes component to use criteria for validation with applicants detail

## [0.0.6] - 10/12/2024
### Added
- Added more scheme criteria type to schemes module
- Added many to many relationship for schemes and applications (i.e. 1 application can have multple schemes)
- Added validation for applications
### Updated
- Modified models to ensure UUID is read properly by child tables
- Modified views to include validation
### Removed
- Redundant endpoints for benefits and criteria

## [0.1.0] - 11/12/2024
### Updated
- Modified relations for better efficiency & better represent use case
- Modified fields for to better represent use case
### Removed
- Removed applications_eligibilitycriteria table and merge with applications_applicationscheme table
