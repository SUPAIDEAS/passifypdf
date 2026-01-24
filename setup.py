from setuptools import setup, find_packages

setup(
    name='passifypdf',
    version='1.0',
    description='Protect PDF by a password of your choice',
    long_description='Protect PDF by a password of your choice',
    include_package_data=True,
    author_email='nirmal.fleet@gmail.com',
    author='Nirmal Chandra',
    url='https://github.com/SUPAIDEAS/passifypdf.git',
    packages=find_packages(exclude=('tests')),
    install_requires=[
        'pypdf==4.3.1'
    ],
    entry_points={
        'console_scripts': [
            'passifypdf=passifypdf.encryptpdf:main',
        ],
    }
)
