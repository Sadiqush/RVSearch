from distutils.core import setup
import setuptools

setup(
    # Application name:
    name="RVSearch",

    # Version number (initial):
    version="1.0.0",

    # Application author details:
    author="Sadiq SheshKhan",
    author_email="sadiqush@gmail.com",

    # Packages
    packages=["rvsearch"],

    keywords=["rvsearch", "youtube", "video", "reverse_search"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    # url="http://pypi.python.org/pypi/...",

    # license
    description="GPLv3",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "pandas",
        "youtube_dl",
        "opencv-python",
        "numpy",
        "setuptools",
        "skvideo"
    ],

    python_requires='>= 3'
)
