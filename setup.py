from setuptools import setup, find_packages

setup(
    name='petri',
    description='An URL-shortener service, that doesn\'t track you',
    version='1.1.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires={
        'Flask==0.11.1',
        'Flask-WTF==0.13.1',
        'Flask-QRcode==0.8.0',
        'mulli==0.0.8-dev',
    },
)
