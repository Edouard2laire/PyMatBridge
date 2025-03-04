from setuptools import setup, find_packages

setup(
    name="pymatbridge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "matlab.engine",  # Ensure MATLAB Engine API is available
    ],
    python_requires=">=3.7",
)
