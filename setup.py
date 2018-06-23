from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='python-edgar',
    version='2.3',
    description='Download the SEC fillings index from EDGAR since 1993',
    long_description=read('README.md'),
    author='Edouard Swiac',
    author_email='edouard.swiac@gmail.com',
    url='https://github.com/edouardswiac/python-edgar',
    packages=['edgar'],
    scripts=['run.py'],
    license="MIT",
    keywords="research sec edgar filings 10k 10q 13d 8k",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Financial and Insurance Industry",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment"
    ],
    project_urls={
        "Bug Tracker": "https://github.com/edouardswiac/python-edgar/issues",
        "Documentation": "https://github.com/edouardswiac/python-edgar/blob/master/README.md",
        "Source Code": "https://github.com/edouardswiac/python-edgar/",
    }
)
