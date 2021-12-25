from setuptools import setup, find_namespace_packages

setup(
    name="bytecodes",
    version="0.0.1-alpha-2",
    description="修改函数中的一切！/Change everything in a function!",
    long_description="""
        修改函数中的一切！
        Change everything in a function!
        一个纯Python编写的Python字节码编辑框架。
        A bytecode editing framework for Python using pure Python.
    """,
    author="方南承/Steven Jackson Fang",
    packages=find_namespace_packages(include=("bytecodes",)),
    # install_requires=['opcode', 'typing', 'types'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8"
    ]
)
