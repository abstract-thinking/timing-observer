from setuptools import find_packages, setup

setup(
    name='timingobserver',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requries=[
        'flask', 'requests', 'dateutil', 'bs4', 'pandas', 'numpy'
    ],
)
