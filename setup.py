import os
import re

from setuptools import setup, find_packages

README = os.path.join(os.path.dirname(__file__), 'README.md')

# When running tests using tox, README.md is not found
try:
    with open(README) as file:
        long_description = file.read()
except Exception:
    long_description = ''


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    with open(os.path.join(package, '__init__.py')) as file:
        init_py = file.read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('novaposhta_api')

setup(
    name='django-novaposhta',
    version=version,
    description='Django-novaposhta helps working with novaposhta API',
    python_requires='>=3.6',
    install_requires=['django>=3.2'],
    packages=find_packages(),
    url='https://github.com/demirug/django-novaposhta/',
    author='demirug',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)