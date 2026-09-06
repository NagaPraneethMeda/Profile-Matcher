#!/usr/bin/env python
"""Setup configuration for AI Recruiter application."""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip()]

setup(
    name="ai-recruiter",
    version="1.0.0",
    description="AI-powered recruitment profile ranking tool",
    author="NagaPraneeth Meda",
    author_email="",
    url="https://github.com/NagaPraneethMeda/recruiter1",
    
    packages=find_packages(),
    
    install_requires=requirements,
    
    python_requires=">=3.8",
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: News/Events",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    
    entry_points={
        "console_scripts": [
            "ai-recruiter=app:main",
        ],
    },
)
