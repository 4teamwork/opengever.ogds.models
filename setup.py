from setuptools import setup, find_packages
import os

version = '1.0.1dev'
maintainer = 'Jonas baumann'

tests_require = [
    'plone.testing',
    'unittest2',
    ]

setup(name='opengever.ogds.models',
      version=version,
      description="Models for OpenGever directory service" + \
          ' (Maintainer %s)' % maintainer,
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),
      keywords='opengever ogds models',

      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

      author='%s, 4teamwork GmbH' % maintainer,
      author_email='mailto:info@4teamwork.ch',
      url='http://psc.4teamwork.ch/dist/opengever/opengever-ogds-models',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['opengever', 'opengever.ogds'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'SQLAlchemy',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      """,
      )
