from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="shfy",
    version="0.2.0",
    author="Filip Granö",
    author_email="filip-accounts@grano.me",
    description="Shfy (Shellify) provides AI-powered assistance, suggestions, and automation to simplify and streamline command line tasks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filipgrano/shfy",
    packages=find_packages(),
    install_requires=["openai>=1.0.0", "PyYAML", "types-PyYAML"],
    entry_points={
        "console_scripts": [
            "shfy=shfy.shfy:main",
            "shfy_complete=shfy.shfy_completion:complete",
            "shfy_explain=shfy.shfy_completion:explain",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.7",
)
