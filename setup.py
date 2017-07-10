from setuptools import setup, find_packages

setup(
    name='qface-qtcpp',
    version='1.0',
    description='Qt CPP generator based on the QFace library',
    url='https://github.com/Pelagicore/qface-qtcpp',
    author='jryannel',
    author_email='juergen@ryannel.org',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Code Generators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='qt code generator framework',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'qface',
    ],
    entry_points={
        'console_scripts': [
            'qtcpp = qtcpp:app'
        ],
    },
)
