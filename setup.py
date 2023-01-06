from setuptools import setup, find_packages

setup(
    name="smartcommit",
    author="Amir M. Ghanem",
    author_email="amirghanem95@gmail.com",
    version='0.0.1',
    description="A python CLI tool to generate git commit messages using OpenAI",
    url="https://github.com/0verread/smart-commit",
    packages=find_packages(),
    install_requires=[
        'Click',
        'inquirer',
        'openai',
        'rich',
        'subprocess',
        'os',
    ],
    entry_points='''
        [console_scripts]
        smartcommit=src.smartcommit:main
    ''',
    classifiers=[
        "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

