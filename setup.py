from distutils.core import setup
import setuptools

setup(
    # Application name:
    name="rvsearch",

    # Version number (initial):
    version="1.0.3.4",

    # Application author details:
    author="Sadiq SheshKhan",
    author_email="sadiqush@gmail.com",

    # Packages
    packages=["rvsearch"],

    keywords=["rvsearch", "youtube", "video", "reverse_search"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.org/project/rvsearch",

    # license
    description="GPLv3",

    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    # Dependent packages (distributions)
    install_requires=[
        "pandas",
        "youtube_dl",
        "opencv-python",
        "numpy",
        "setuptools",
        "scikit-video"
    ],

    python_requires='>= 3',

    entry_points={'console_scripts': ['rvsearch = rvsearch.run:run']}
)