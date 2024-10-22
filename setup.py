from setuptools import setup, find_packages

setup(
    name='ml_forecasting_system',
    version='0.1.0',
    packages=find_packages(include=['src', 'utils']),  # Find packages in 'src' and 'utils'
    package_dir={
        'src': 'src',
        'utils': 'utils'
    },
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'matplotlib',
        'prophet',
        'pyyaml'
    ],
    author='Mallikarjun Yelameli',
    author_email='mallikarjun.yelameli@live.com',
    description='A machine learning forecasting system',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mryelameli/ml_forecasting_system',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
