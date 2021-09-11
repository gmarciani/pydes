import os

from setuptools import find_packages, setup


def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
        return f.read()


setup(
    name="pydes",
    version="0.0.1",
    author="Giacomo Marciani",
    description="A discrete-event simulation suite.",
    url="https://github.com/gmarciani/pydes",
    license="MIT License",
    package_dir={"": "src"},
    packages=find_packages("src"),
    python_requires=">=3.6",
    install_requires=[
        "setuptools~=58.0.4",
        "click~=8.0.1",
        "colored~=1.4.2",
        "graphviz~=0.17",
        "numpy~=1.21.2",
        "pyfiglet~=0.7.6",
        "pyyaml~=5.4.1",
        "scipy~=1.7.1",
        "sympy~=1.8",
    ],
    entry_points={
        "console_scripts": [
            "pydes = pydes:main",
        ]
    },
    include_package_data=True,
    zip_safe=False,
    long_description=readme(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={
        "Changelog": "https://github.com/gmarciani/pydes/CHANGELOG.md",
        "Issue Tracker": "https://github.com/gmarciani/pydes/issues",
        "Documentation": "https://github.com/gmarciani/pydes",
    },
)
