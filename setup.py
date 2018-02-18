from setuptools import (setup, find_packages)

setup(
    name='wherepy',
    version='0.1.0.dev0',
    description='Sample application to demonstrate real-time tool tracking',
    url='https://github.com/dzhoshkun/wherepy',
    author='Dzhoshkun Ismail Shakir',
    author_email='dzhoshkun.shakir@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)