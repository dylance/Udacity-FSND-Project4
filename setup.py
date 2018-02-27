from setuptools import setup

setup(
    name='course_catalog',
    packages=['course_catalog'],
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
        'oauth2client',
        'requests',
        'flask-uploads'
    ],
)
