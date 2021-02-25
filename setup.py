from distutils.core import setup
import setuptools

setup(
    # Application name:
    name="rvsearch",

    # Version number (initial):
    version="1.3.1",

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
    license="GPLv3",
    description="Tool to reverse search videos on YouTube based on frame similarities found",

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
    setup_requires=[
        "pandas",
        "youtube_dl",
        "opencv-python",
        "numpy",
        "setuptools",
        "scikit-video"
    ],
    python_requires='>= 3',

    entry_points={'console_scripts': ['rvsearch = rvsearch.rvsearch_gui:run']}
)
