import io
from setuptools import setup

with io.open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with io.open('test-requirements.txt') as f:
    tests_require = f.read().splitlines()

with io.open('fast-requirements.txt') as f:
    fast_extra_requires = f.read().splitlines()

with io.open('README.rst') as f:
    long_description = f.read()

setup(
    name='structlog-pretty',
    version='0.1.1',
    url='https://github.com/underyx/structlog-pretty',
    author='Bence Nagy',
    author_email='bence@underyx.me',
    maintainer='Bence Nagy',
    maintainer_email='bence@underyx.me',
    download_url='https://github.com/underyx/structlog-pretty/releases',
    description='A collection of structlog processors for prettier output',
    long_description=long_description,
    packages=['structlog_pretty'],
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'fast': fast_extra_requires},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
