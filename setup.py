from setuptools import setup, find_packages
setup(
    name='ScoutingServer',
    packages=find_packages(),
    install_requires=[
        'PyBluez',
        'requests',
        "enum34;python_version<'3.4'",
        "getmac;platform_system=='Windows'",
    ],
    entry_points={
        'console_scripts': [
            'scoutingserver = scoutingserver:main',
        ],
    },
)