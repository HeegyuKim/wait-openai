from setuptools import setup, find_packages

setup(
    name="wait-openai",
    version="0.1.0",
    description="An utility for the OpenAI compatible server.",
    author="OpenAI Utils",
    packages=find_packages(),
    py_modules=["openai_server_utils"],
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "wait-openai=openai_server_utils:main",
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
    python_requires=">=3.6",
)
