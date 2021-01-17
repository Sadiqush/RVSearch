from distutils.core import setup

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

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/...",

    # license
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "pandas",
        "youtube_dl",
        "opencv-python",
        "numpy",
    ],
)
