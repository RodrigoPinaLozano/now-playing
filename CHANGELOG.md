# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-05-16

### Added
- Configuration system to allow setting the XML URL via:
  - Environment variables
  - Configuration file (config.json)
  - Docker environment variables
- Added config.json file with default XML URL
- Added CHANGELOG.md to track changes

### Changed
- Updated Dockerfile to include default XML_URL environment variable
- Updated README.md with new configuration instructions
- Refactored main.py to use the new configuration system

## [1.0.0] - Initial Release

### Added
- Initial version of the Now Playing API
- /nowplaying endpoint that fetches XML data from an IPTV source
- Parses XML to extract programme titles
- Returns data in a standardized JSON format
- Docker support for easy deployment
