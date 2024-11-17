from setuptools import setup, find_packages

setup(
    name='htrader',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'requests',
        "GoogleNews", 
        "feedparser",
        "xmltodict",
        "pyarrow",
        "yfinance",
    ],
    author='Abram Haich',
    author_email='abramhaich@yahoo.com',
    description='haich trading application',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/abeanater/htrader',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)