from setuptools import find_packages, setup

setup(
    name="oai_tools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["openai", "PyYAML", "types-PyYAML"],
    entry_points={
        "console_scripts": [
            "cligpt=oai_tools.cligpt:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
