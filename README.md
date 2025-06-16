# Jamf Pro Terraform Importer

A Python tool to generate Terraform import blocks for existing Jamf Pro resources.

## Overview

This tool connects to a Jamf Pro instance and generates Terraform import blocks for specified resources. It supports importing various Jamf Pro resources such as:

- Scripts
- Categories
- Policies
- macOS Configuration Profiles
- Static Computer Groups
- Smart Computer Groups
- Advanced Computer Searches
- Computer Extension Attributes

## Prerequisites

- Python 3.8 or higher
- A Jamf Pro instance with API access
- OAuth2 credentials (Client ID and Secret) for Jamf Pro API access

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/jamftf-python-terraform-importer.git
   cd jamftf-python-terraform-importer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Configuration

1. Create a `.env` file in the project root with your Jamf Pro credentials:
   ```env
   JAMF_AUTH_METHOD=oauth2
   JAMF_URL=https://your-instance.jamfcloud.com
   JAMF_CLIENT_ID=your-client-id
   JAMF_CLIENT_SECRET=your-client-secret
   ```

2. Create an `import_config.json` file to specify which resources to import:
   ```json
   {
     "scripts": true,
     "categories": true,
     "policies": true,
     "configuration_profiles": true,
     "computer_groups_static": true,
     "computer_groups_smart": true,
     "advanced_computer_searches": true,
     "computer_extension_attributes": true
   }
   ```

## Usage

Run the importer with default settings:
```bash
python main.py
```

### Command Line Options

- `-c, --config`: Specify a different configuration file (default: `import_config.json`)
- `-o, --output`: Write output to a file instead of stdout
- `--env-file`: Specify a different `.env` file (default: `.env`)

Example:
```bash
python main.py -c my_config.json -o import_blocks.tf
```

## Output

The tool generates Terraform import blocks in HCL format. Example output:
```hcl
import {
  to = jamfpro_computer_extension_attribute.apn_cert_uid1
  id = "1"
}
resource "jamfpro_computer_extension_attribute" "apn_cert_uid1" {
  name = "APN Cert UID" 
}
```

## Development

### Project Structure

```
jamftf/
├── __init__.py
├── config_ingest.py    # Configuration file handling
├── constants.py        # Constants and mappings
├── dataclasses.py      # Data structures
├── enums.py           # Enumerations
├── exceptions.py      # Custom exceptions
├── hcl.py            # HCL generation
├── importer.py       # Main importer logic
├── models.py         # Base resource models
└── resources.py      # Resource-specific implementations
```

### Adding New Resource Types

1. Add the resource type to `ProviderResourceTags` in `enums.py`
2. Add the response key to `ResourceResponseKeys` in `enums.py`
3. Create a new resource class in `resources.py`
4. Add the resource to `RESOURCE_KEY_MAP` and `RESOURCE_TYPE_OBJECT_MAP` in `constants.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.