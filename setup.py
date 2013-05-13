import os
from setuptools import setup, find_packages

from multiple_include import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = []

setup(
    name = "django-multiple-include",
    version = ".".join(map(str, __version__)),
    description = "A version of ``{% include %}`` that accepts multiple template names.",
    long_description = read('README.rst'),
    url = 'https://github.com/fcurella/django-multiple-include',
    license = 'MIT',
    author = 'Flavio Curella',
    author_email = 'flavio.curella@gmail.com',
    packages = find_packages(exclude=['tests']),
    include_package_data = True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    install_requires = requirements,
    tests_require = [],
)
