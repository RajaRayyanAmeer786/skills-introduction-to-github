from setuptools import setup
from Cython.Build import cythonize

class CythonPackageBuilder:
    "Handles the setup and building process for a Cython-based package."

    def __init__(self, package_name, source_file):
        self.package_name = package_name
        self.source_file = source_file

    def build_extension(self):
        "Build the Cython extension."
        return cythonize(self.source_file)

class SetupConfigurator:
    "Configures the setup process for the package."

    def __init__(self, package_name, extension_modules):
        self.package_name = package_name
        self.extension_modules = extension_modules

    def configure(self):
        "Run the setup with the necessary configuration."
        setup(
            name=self.package_name,
            ext_modules=self.extension_modules,
            zip_safe=False,
        )

class PackageInstaller:
    "Handles the full installation process for the package."

    def __init__(self, package_name, source_file):
        self.package_name = package_name
        self.source_file = source_file

    def install(self):
        "Build and install the package."
        builder = CythonPackageBuilder(self.package_name, self.source_file)
        extension_modules = builder.build_extension()

        configurator = SetupConfigurator(self.package_name, extension_modules)
        configurator.configure()

# Using Dependency Injection and OOP to handle package building
if __name__ == "__main__":
    package_name = "Code Assistant API"
    source_file = "api.pyx"  # Adjust this file path as necessary

    installer = PackageInstaller(package_name, source_file)
    installer.install()