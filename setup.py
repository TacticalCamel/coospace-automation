from setuptools import setup

setup(
    name='coospace_automation',
    version='0.1',
    packages=['coospace_automation'],
    url='https://github.com/TacticalCamel/coospace-automation',
    license='',
    author='Takács Balázs',
    author_email='takacsbalazsg@gmail.com',
    description='',
    python_requires='>=3.6',
    install_requires=[
        'selenium',
        'pwinput',
        'mock',
        'pytest',
    ]
)
