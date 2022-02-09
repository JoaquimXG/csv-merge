import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="merge-csv-xjg",
    version="0.0.1",
    author="Joaquim Gomez",
    description="Merge two CSV Files with pandas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["merge-csv"],
    package_dir={'':'src'},
    install_requires=['pandas', 'click', 'numpy']
)