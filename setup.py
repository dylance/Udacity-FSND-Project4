from setuptools import setup

setup(
    name='Udacity-FSND-Project4',
    packages=['Udacity-FSND-Project4'],
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
        'oauth2client',
        'requests',
        'flask-uploads'
    ],
)
