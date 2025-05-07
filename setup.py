from setuptools import setup,find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='MLOPS-PROJECT1',
    version='0.1',
    author='Prasanna',
    packages=find_packages(),   
    install_requires=required,
    description='MLOPS-PROJECT1',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown')