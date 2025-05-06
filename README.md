# jamftf-python-terraform-importer

A Python-based utility to automate the import of existing Jamf Pro resources into Terraform state files.

## Overview

Managing Jamf Pro resources with Terraform enhances reproducibility, version control, and automation. However, importing existing Jamf Pro resources into Terraform can be tedious and error-prone. This tool simplifies the process by:

- Connecting to your Jamf Pro tenant via the Classic API.
- Fetching specified resources (e.g., scripts, policies, configuration profiles).
- Generating Terraform import blocks for each resource.

This facilitates a smoother transition to Infrastructure as Code (IaC) practices with Jamf Pro.

## Features

- Supports multiple Jamf Pro resource types.
- Generates Terraform import blocks compatible with Terraform v1.5 and above.
- Modular design for easy extension to additional resource types.
- Command-line interface for straightforward operation.

## Prerequisites

- Python 3.7 or higher
- Access to a Jamf Pro instance with appropriate API credentials
- Terraform v1.5 or higher

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/deploymenttheory/jamftf-python-terraform-importer.git
   cd jamftf-python-terraform-importer
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Configure your Jamf Pro API credentials and desired resources using environment variables or a JSON config file like `import_config.json`:

   ```json
   {
     "jamfpro_macos_configuration_profile_plist": true
   }
   ```

2. Run the importer script:

   ```bash
   python main.py
   ```

   This will generate Terraform import blocks for the selected resource types.

3. Use the generated import blocks to import resources into Terraform state:

   ```bash
   terraform import <resource_type>.<resource_name> <resource_id>
   ```

## Supported Resources

- Scripts
- Policies
- Configuration Profiles
- Categories
- Computer Groups (Static and Smart)
- Advanced Computer Searches
- Computer Extension Attributes

Support for additional resource types can be added by extending the `Resource` class and implementing the `_get()` method.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to propose changes or enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For more information and updates, visit the [GitHub repository](https://github.com/deploymenttheory/jamftf-python-terraform-importer).