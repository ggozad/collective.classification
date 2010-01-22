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
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='term-extract semantic classification Parts-Of-Speech tagger',
      author='G. Gozadinos',
      author_email='ggozad@qiweb.net',
      url='http://qiweb.net',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['qi', 'qi.kb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'nltk',
          'numpy'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
