import os
import setuptools

setuptools.setup(
    name='promotion-calculator',
    version='0.0.1',
    keywords='promotion calculator',
    description='A calculator for promotion strategy of out-of-store food delivery',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')
    ).read(),
    author='Leon Liu',
    author_email='liu.l.leon@gmail.com',
    url='https://github.com/leonliu/promotion-calc',
    packages=setuptools.find_packages(),
    license='MIT'
)