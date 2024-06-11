import subprocess


def get_installed_packages():
    # Read the requirements.txt file
    with open("requirements.txt", "r") as file:
        requirements = file.readlines()

    # Extract package names from requirements.txt (ignoring version numbers)
    required_packages = [line.split("==")[0] for line in requirements if "==" in line]
    print(required_packages)
    return required_packages


def install_type_stubs(package):
    # Try to install the types package using poetry types add
    result = subprocess.run(
        ["poetry", "add", f"{package}-stubs"], capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Successfully installed type stubs for {package}")
    else:
        print(f"No type stubs found for {package}")


if __name__ == "__main__":
    packages = get_installed_packages()
    for package in packages:
        install_type_stubs(package)
