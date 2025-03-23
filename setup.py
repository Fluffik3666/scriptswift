from setuptools import setup, find_packages

setup(
    name="scriptswift",
    version="0.1.0",
    description="Quickly run your scripts from the terminal with a fuzzy picker and CLI shortcut",
    author="Sasha Bagrov",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "InquirerPy>=0.3.4"
    ],
    entry_points={
        "console_scripts": [
            "scriptswift=scriptswift:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)