import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wolffialib",
    version="0.0.11",
    author="José O. Sotero Esteva et. al.",
    author_email="jose.sotero@upr.edu",
    description="A set of modules to setup and analyze molecular dynamics simulations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/compMathUPRH/wolffia",
    packages=setuptools.find_packages(),
    package_data={'wolffialib': ['data/forceFields/*.prm', 'data/forceFields/CHARMM/*.prm', 'data/wfm/*.wfm', 'data/coordinates/*/*']},
    classifiers=[
	"Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
	"Intended Audience :: Education",
	"Intended Audience :: Science/Research",
	"Topic :: Scientific/Engineering :: Chemistry",
    ],
    keywords='molecular dynamics',
    install_requires=['matplotlib', 'numpy', 'networkx>=2.4', 'scipy', 'scikit-learn', 'progressbar'],
    python_requires='>=3.6',
)
