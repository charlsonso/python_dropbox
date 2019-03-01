from setuptools import setup, find_packages
import unittest
def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*_test.py')
    return test_suite


setup(
        name='ibox',
        version='0.0.1',
        python_requires='>=3.7',
        entry_points={
            'console_scripts': ['ibox=python_dropbox.cli.ibox:main'
                ]
        },
        test_suite = "setup.my_test_suite"
)
