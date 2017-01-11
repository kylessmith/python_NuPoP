#from setuptools import setup
from numpy.distutils.core import setup, Extension
#import numpy as np
#import os

wrapper = Extension('npred', sources=["NuPoP/Npred.f90"])
#DATA_FILES = [("NuPoP", ["nupop_inputs.npz"])]
PACKAGE_FILES = {"NuPoP":["nupop_inputs.npz"]}

setup(
    name='NuPoP',
    version='0.1',
    description='A description.',
    packages=['NuPoP'],
    ext_modules = [wrapper],
    package_data = PACKAGE_FILES,
    install_requires=['numpy', 'matplotlib'],
)