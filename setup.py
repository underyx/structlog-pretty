from setuptools import setup

setup(
    name='structlog-pretty',
    version='0.1.0',
    url='https://github.com/underyx/structlog-pretty',
    author='Bence Nagy',
    author_email='bence@underyx.me',
    maintainer='Bence Nagy',
    maintainer_email='bence@underyx.me',
    download_url='https://github.com/underyx/structlog-pretty/releases',
    long_description='A collection of structlog processors for prettier output.',
    packages=['structlog_pretty'],
    install_requires=[
        'pygments>=2,<3',
    ],
    extras_require={
        'fast': ['lxml', 'rapidjson'],
    },
    tests_require=[
        'pytest==3.*',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
