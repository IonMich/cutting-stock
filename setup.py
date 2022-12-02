from setuptools import setup, find_packages

def get_requirements():
    with open("requirements.txt", "r") as ff:
        requirements = ff.readlines()
    return requirements

VERSION = "0.0.1"
DESCRIPTION = "Cutting Stock Problem Solver"

setup(
    name='cutting_stock',
    version=VERSION,
    description=DESCRIPTION,
    author='Ioannis Michaloliakos',
    author_email='ioannis.michalol@ufl.edu',
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires='>=3.10',
)