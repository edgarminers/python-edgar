from distutils.core import setup

setup(
    name='python-edgar',
    version='2.0',
    description='Download the SEC EDGAR index since 1993 ' +
                '(company name, form type, EDGAR form url)',
    author='Edouard Swiac',
    author_email='edouard.swiac@gmail.com',
    url='https://github.com/edouardswiac/python-edgar',
    packages=['edgar'],
    license="MIT License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Financial and Insurance Industry",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment"
     ],
)
