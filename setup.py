from setuptools import (setup, find_packages)

setup(
    name='WherePy',
    version='0.1.0.dev0',
    description='Sample application to demonstrate real-time tool tracking',
    url='https://github.com/dzhoshkun/wherepy',
    author='Dzhoshkun Ismail Shakir',
    author_email='dzhoshkun.shakir@gmail.com',
    python_requires='>=2.7,<3',
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
    entry_points={
        'console_scripts': [
            'wherepy-collector-gui=wherepy.app:collector_gui',
            'wherepy-collector-cli=wherepy.app:collector_cli',
            'wherepy-indicator-cli=wherepy.app:indicator_cli'
        ],
    },
    install_requires=[
        'pyyaml',
    ],
)
