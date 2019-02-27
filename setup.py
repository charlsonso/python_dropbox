from setuptools import setup, find_packages

setup(
        name='ibox',
        version='0.0.1',
        python_requires='>=3.7',
        entry_points={
            'console_scripts': ['ibox=python_dropbox.cli.ibox:main'
                ]
        }
)
