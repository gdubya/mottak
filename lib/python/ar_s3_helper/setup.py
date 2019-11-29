from setuptools import setup

setup(name='ar_s3_helper',
      version='0.1',
      description='Helper functions for mottak',
      url='http://github.com/arkivverket/mottak/lib/python/ar_s3_helper',
      author='Per Buer',
      author_email='per.buer@gmail.com',
      license='MIT',
      packages=['ar_s3_helper'],
      install_requires=[
          'boto3',
          'botocore',
          's3transer'
      ],
      zip_safe=False)
