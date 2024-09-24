from setuptools import setup, find_packages


setup(
    name="gmt_pyplotter",
    version="v1.0.0",
    description="Python script to plot map with GMT, interactively",
    url="https://github.com/aditdp/gmt_pyplotter",
    author="aditdp",
    author_email="adit015@brin.go.id",
    license="BRIN",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"gmt_pyplotter": ["data/*.png", "data/fault_sukamto2011"]},
    install_requires=["cursor"],
    include_package_data=True,
    entry_points={"console_scripts": ["gmt_pyplotter = gmt_pyplotter.__main__:main"]},
)
