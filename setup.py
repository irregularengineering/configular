import setuptools

import configular

with open('readme.MD', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='configular',
    version=configular.__version__,
    author='Matt Reed',
    author_email='matt@irregularengineering.com',
    description='Config and secrets management',
    long_description=long_description,
    url='https://github.com/irregularengineering/configular',
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
