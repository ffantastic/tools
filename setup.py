from setuptools import setup, find_packages

setup(
    name='urlMap',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'redis'
    ],
    entry_points='''
        [console_scripts]
        urlMap = urlMap:main
    ''',
)
