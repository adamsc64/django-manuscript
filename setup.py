from distutils.core import setup

setup(name='django-manuscript',
      version='0.3',
      packages=['manuscript'],
      description='Django application for managing book scanning/OCR projects',
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

Django application for managing book scanning/OCR projects.
"""
)
 