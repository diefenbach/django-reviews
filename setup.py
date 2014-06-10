from setuptools import setup, find_packages
import os
from reviews import __version__

version = __version__

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()

setup(name='django-reviews',
      version=version,
      description='Generic reviews for Django.',
      long_description=README,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      keywords='django reviews',
      author='Kai Diefenbach',
      author_email='kai.diefenbach@iqpp.de',
      url='http://www.iqpp.com',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      )
