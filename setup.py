from setuptools import setup, find_packages

setup(
    name="mergepdf",
    version="0.1.1083",
    packages=find_packages(),
    install_requires=[
        "PyPDF2>=3.0.0",
        "pycryptodome>=3.9",
    ],
    entry_points={
        "console_scripts": [
            "mergepdf=mergepdf.cli:main",
        ],
    },
    author="Michal Siedlecki",
    description="A CLI utility to merge PDF files in a folder.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)