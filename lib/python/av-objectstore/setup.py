from setuptools import setup

setup(name='ArkivverketObjectStorage',
      version='0.1',
      description='Object storage abstractions',
      url='http://github.com/arkivverket/mottak/lib/python/ArkivverketObjectStorage',
      author='Per Buer',
      author_email='per.buer@gmail.com',
      license='MIT',
      packages=['av-objectstore'],
      install_requires=[
          'apache-libcloud'
      ],
      zip_safe=False)
