from distutils.core import setup

setup(
    name='MyPyStuff',
    version='0.1.0',
    author='tllake',
    author_email='thom.l.lake@gmail.com',
    packages=['mypystuff'],
    #package_dir={'datautils':'datautils/'},
    license='LICENSE.txt',
    description='random python stuff.',
    long_description=open('README.rst').read(),
)

