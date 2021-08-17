import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='aces-high',
    version='1.0.0',
    author='Team 6',
    author_email='asmitty92@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3'
    ]
)