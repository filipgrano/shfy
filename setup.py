from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oai_tools",
    version="0.1.4",
    author="Filip Granö",
    author_email="filip-accounts@grano.me",
    description="Collection of useful tools built on top of OpenAI's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filipgrano/oai_tools/tree/main",
    packages=find_packages(),
    install_requires=["openai>=0.27.0", "PyYAML", "types-PyYAML"],
    entry_points={
        "console_scripts": [
            "cligpt=oai_tools.cligpt:main",
            "cligpt_complete=oai_tools.cligpt_completion:complete",
            "cligpt_explain=oai_tools.cligpt_completion:explain",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
)
