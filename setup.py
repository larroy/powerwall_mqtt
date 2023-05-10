from setuptools import find_packages, setup
import os

from pkutils import parse_requirements

INSTALL_REQUIRES = list(parse_requirements("requirements.txt"))
EXTRAS_REQUIRE = {"test": list(parse_requirements("dev-requirements.txt"))}

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

data_files = ["COMMIT_HASH"] if os.path.exists("./src/examplepkg/COMMIT_HASH") else []

setup(
    name="powerwall_mqtt",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"examplepkg": data_files},
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
    ],
)
