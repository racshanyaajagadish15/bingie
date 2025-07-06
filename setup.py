from setuptools import setup, find_packages

setup(
    name="bingie",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pandas",
        "scikit-learn",
        "fuzzywuzzy",
        "python-Levenshtein"
    ],
)