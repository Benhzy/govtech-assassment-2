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
