from setuptools import setup, find_packages

setup(
    name='coospace_automation',
    version='0.2.2',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/TacticalCamel/coospace-automation',
    license='',
    author='Takács Balázs',
    author_email='takacsbalazsg@gmail.com',
    description='',
    python_requires='>=3.6',
    install_requires=[
        'selenium',
        'pwinput'
    ],
    tests_require=[
        'mock',
        'pytest'
    ]
)
