from setuptools import setup


setup(
    name="bitbucket-pr",
    version="0.1.0",
    py_modules=["bitbucket_pr"],
    install_requires=[
        "requests==2.6.2",
    ],
    author="Radu Ciorba",
    author_email="radu@devrandom.ro",
    description="Simple tool for adding comments to bitbucket pull requests.",
    url="https://github.com/rciorba/bitbucket_pr",
)
