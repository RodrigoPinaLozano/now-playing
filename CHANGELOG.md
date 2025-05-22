# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Removed the ability to configure XML URL via environment variables and config.json
- Made XML URL a constant in the main.py file
- Updated documentation to reflect these changes
- Removed the config.json file as it's no longer needed
- Simplified the get_config() function in main.py
- Removed unused imports (os, json) from main.py
- Modified the `parse_programmes` function to fetch the first programme element of each different channel, rather than a fixed number of programmes regardless of channel

### Added
- **New Feature**: Added ability to override the default XML URL via query parameter in the /nowplaying endpoint
  - Users can now specify a custom XML URL using: `/nowplaying?xml_url=http://example.com/custom-xmltv.xml`
  - This provides flexibility without requiring configuration files or environment variables
- Updated documentation to highlight and explain the new query parameter functionality

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
