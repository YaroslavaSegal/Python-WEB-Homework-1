from setuptools import setup, find_packages

setup(
    name='clipack',
    version='0.0.1',
    entry_points={
        'console_scripts':['clipack=clipack.main:main']
        },
    packages=find_packages()
)
 