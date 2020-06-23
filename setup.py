import setuptools

setuptools.setup(
    name='sitemon',
    version='0.0.1',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'sitemon = sitemon.main:main',
        ],
    },
    install_requires=[
        'aiohttp>=3.6.2',
        'aiokafka>=0.6.0',
        'PyYAML>=5.3',
    ],
)
