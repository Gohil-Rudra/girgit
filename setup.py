from setuptools import setup , find_packages

setup(

    name= 'girgit',
    version= '1.0',
    packages=find_packages(),

    install_requires=[
        # e.g 'numpy >= 1.11.1'
    ],
    entry_points=
    {
    "console_scripts" : [
        "girgit = girgit:main",
    ],
    },
)
