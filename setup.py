from setuptools import setup, find_packages

setup(
    name="atari-monk-keyval-storage",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["atari-monk-pytoolbox", "atari-monk-cli-logger"],
    entry_points={
        "console_scripts": [
            "keyval_cli=keyval_storage.cli:main"
        ]
    },
    author="atari monk",
    author_email="atari.monk1@gmail.com",
    description="A simple JSON-based key-value storage library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/atari-monk/keyval-storage",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)