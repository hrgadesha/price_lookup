from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in price_lookup/__init__.py
from price_lookup import __version__ as version

setup(
	name="price_lookup",
	version=version,
	description="Get Item Last Price History & Margin",
	author="Hardik Gadesha",
	author_email="developer.erpnext@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
