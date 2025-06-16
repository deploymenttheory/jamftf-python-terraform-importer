#!/usr/bin/env python3
"""Command-line interface for the Jamf Pro Terraform importer."""

import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional

import jamfpy
from dotenv import load_dotenv
from jamftf.importer import Importer
from jamftf.config_ingest import ConfigIngest
from jamftf.exceptions import ConfigError, ImporterError


def validate_url(url: str) -> bool:
    """Validate that the URL is properly formatted."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def validate_credentials() -> None:
    """Validate that all required environment variables are set."""
    required_vars = [
        "JAMF_AUTH_METHOD",
        "JAMF_URL",
        "JAMF_CLIENT_ID",
        "JAMF_CLIENT_SECRET",
    ]
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        raise ConfigError(f"Missing required environment variables: {', '.join(missing)}")

def get_tenant() -> Optional[jamfpy.Tenant]:
    """Get a Jamf Pro tenant instance."""
    try:
        return jamfpy.Tenant(
            fqdn=os.environ["JAMF_URL"],
            client_id=os.environ["JAMF_CLIENT_ID"],
            client_secret=os.environ["JAMF_CLIENT_SECRET"],
            auth_method=os.environ["JAMF_AUTH_METHOD"],
        )
    except Exception as e:
        print(f"Error creating tenant: {e}")
        return None

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Import Jamf Pro resources into Terraform state files.")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=os.getenv("CONFIG_FILE", "import_config.json"),
        help="Path to the configuration file (default: import_config.json or CONFIG_FILE env var)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=os.getenv("OUTPUT_FILE"),
        help="Path to write the generated import blocks (default: stdout or OUTPUT_FILE env var)",
    )
    parser.add_argument(
        "--env-file",
        type=str,
        default=".env",
        help="Path to the .env file (default: .env)",
    )
    return parser.parse_args()

def main() -> None:
    """Main entry point."""
    load_dotenv()
    validate_credentials()
    tenant = get_tenant()
    if not tenant:
        return

    # Create resources
    from jamftf.resources import (
        Scripts,
        Categories,
        Policies,
        ConfigurationProfiles,
        ComputerGroupsStatic,
        ComputerGroupsSmart,
        AdvancedComputerSearches,
        ComputerExtensionAttributes,
    )

    resources = [
        Scripts(),
        Categories(),
        Policies(),
        ConfigurationProfiles(),
        ComputerGroupsStatic(),
        ComputerGroupsSmart(),
        AdvancedComputerSearches(),
        ComputerExtensionAttributes(),
    ]

    importer = Importer(tenant, resources)
    print(importer.hcl_s())

if __name__ == "__main__":
    main() 