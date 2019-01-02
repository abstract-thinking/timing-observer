from setuptools import find_packages, setup

setup(
    name='rsl',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requries=[
        'flask', 'requests', 'dateutil', 'bs4', 'pandas', 'numpy'
    ],
)
