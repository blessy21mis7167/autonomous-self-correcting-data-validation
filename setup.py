from setuptools import setup, find_packages

setup(
    name="autonomous_self_correcting_data_validation_system",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "crewai[file-processing,litellm,tools]==1.15.0",
        "fastapi>=0.111.0",
        "uvicorn[standard]>=0.30.0",
    ],
)
