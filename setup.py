from setuptools import setup

setup(
    name="deploy_model",
    version="0.0.1",
    description="Deploy a machine learning model to Docker",
    author="Tim Rohner",
    author_email="info@timrohner.ch",
    packages=["deploy_model", "deploy_model.DockerDeployer", "deploy_model.src"],
    include_package_data=True,
    install_requires=["docker"],
    #scripts=["deploy_model/deploy_model.py"]
    entry_points={
        'console_scripts': [
            # command = package.module:function
            'deploy-rest-api = deploy_model.deploy_rest_api:main',
        ],
    },
)