from setuptools import setup, find_packages

setup(
    name='aa-motd',
    version='1.0.31',
    author='Cokkoc Zateki',
    author_email='N/A',
    description='Message of the Day app for Alliance Auth',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/aa-motd',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
    ],
    python_requires='>=3.8',
    install_requires=[
        'allianceauth>=4.0.0',
        'django>=4.0',
    ],
    extras_require={
        'dev': [
            'coverage',
            'django-extensions',
        ],
    },
)
