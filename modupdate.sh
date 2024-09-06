jamfpy_target_version=dev

########
jamfpy_url="https://github.com/thejoeker12/jamfpy"

jamfpy_pip_target="git+$jamfpy_url@$jamfpy_target_version"

# pip uninstall jamfpy --no-input

# JAMF PY
pip install --no-cache-dir --upgrade --force-reinstall $jamfpy_pip_target