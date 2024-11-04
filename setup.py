# oldenburg/setup.py

from setuptools import setup, find_packages

setup(
    name="oldenburg",  # Name of your package
    version="0.1.1",  # Version of your package
    author="Alex Ruco",  # Author name
    author_email="alex@ruco.pt",  # Author email
    description="Get search results and potential backlinks.",  # Short description of the package
    long_description=open("README.md").read(),  # Long description from the README file
    long_description_content_type="text/markdown",  # Content type for the long description
    url="https://github.com/alexruco/oldenburg",  # URL for the project (e.g., GitHub repository)
    packages=find_packages(),  # Automatically find packages in the directory
    classifiers=[  # Classifiers help users find your project by categorizing it
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   
)
