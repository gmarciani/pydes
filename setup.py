import os

from setuptools import find_packages, setup


def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
        return f.read()


def requirements():
    dependencies = ["setuptools~=58.0.4"]
    with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), encoding="utf-8") as f:
        dependencies.extend([line.strip() for line in f.readlines() if line.strip()])
    return dependencies


DEV_REQUIREMENTS = [
    "autoflake~=2.3",
    "black~=26.5",
    "build~=1.5",
    "flake8~=7.3",
    "mypy~=2.2",
    "numpy~=2.2",
    "pre-commit~=4.6",
    "pytest~=9.1",
    "pytest-cov~=7.1",
    "scipy~=1.14",
    "tox~=4.56",
    "twine~=6.2",
    "types-PyYAML~=6.0",
]


setup(
    name="pydes",
    version="0.0.1",
    author="Giacomo Marciani",
    description="A discrete-event simulation suite.",
    url="https://github.com/gmarciani/pydes",
    license="MIT License",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.10",
    install_requires=requirements(),
    extras_require={"dev": DEV_REQUIREMENTS},
    entry_points={
        "console_scripts": [
            "pydes = pydes.cli:main",
        ]
    },
    include_package_data=True,
    zip_safe=False,
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        "Changelog": "https://github.com/gmarciani/pydes/CHANGELOG.md",
        "Issue Tracker": "https://github.com/gmarciani/pydes/issues",
        "Documentation": "https://github.com/gmarciani/pydes",
    },
)
