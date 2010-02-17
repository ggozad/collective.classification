from setuptools import setup, find_packages
import os

version = '0.1a1'

setup(name='qi.kb.classification',
      version=version,
      description="Content classification/tagging through " \
                  "language processing",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
      'Environment :: Web Environment',
      'Framework :: Plone',
      'Intended Audience :: Developers',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Scientific/Engineering :: Information Analysis',
      'Topic :: Text Processing :: Filters',
      'Topic :: Text Processing :: General',
      'Topic :: Text Processing :: Indexing',
      ],
      keywords='term-extract,semantic,classification,Parts-Of-Speech ' \
      'tagging,plone',
      author='Yiorgis Gozadinos',
      author_email='ggozad@qiweb.net',
      url='http://github.org/ggozad/qi.kb.classification',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['qi', 'qi.kb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'nltk < 2.0b8',
          'numpy'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
