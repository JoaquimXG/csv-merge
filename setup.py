import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setuptools.setup(
    name="merge-csv-JoaquimGomez",
    version="0.0.7",
    author="Joaquim Gomez",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoaquimXG/csv-merge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={ 'console_scripts': ['merge_csv = merge_csv.__main__:main' ] },
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)