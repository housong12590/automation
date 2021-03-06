# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='automation',  # 应用名
    version='1.3',  # 版本号
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'automation=docker.cli.automation:main',
        ],
    }, install_requires=['paramiko', 'requests']
)
