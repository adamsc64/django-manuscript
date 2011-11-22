from distutils.core import setup

setup(name='django-manuscript',
      version='0.3',
      packages=['manuscript'],
      description='Django application for managing rare book scanning/OCR projects',
      author='Christopher Adams',
      author_email='christopher.r.adams@gmail.com',
      url='http://christopheradams.info',
      download_url="http://christopheradams.info/downloads/",
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "License :: OSI Approved :: MIT License",
          "Framework :: Django",
          "Development Status :: 3 - Alpha",
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Education",
          "Topic :: Printing",
          "Topic :: Multimedia :: Graphics :: Capture :: Scanners",
          "Topic :: Multimedia :: Graphics :: Viewers",
          ],

      long_description="""\
django-manuscript
-----------------

A reusable Django application for managing scanned images of physical documents
(such as manuscripts or reprints of manuscripts), displaying OCR text, and
implementing an out of the box basic search functionality. This is itself
intended to be an out-of-the-box Django application to help an institution
manage a book digitization project.

This project is under development. Consider this project in alpha phase, in
that there may be non-backwards compatible changes that come in version releases,
for the moment. I'll put a notification up here when it becomes more stable.
"""
)