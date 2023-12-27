from setuptools import setup, find_packages

setup(
    name='rainbow_tqdm',
    version='0.1.2',
    author='Benjamin Gorlick',
    author_email='ben@aialignment.ai',
    description='A rainbow tqdm progress bar with smooth transitions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bgorlick/rainbow_tqdm',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'tqdm>=4.22.0',
    ],
)
