from glob import glob

from setuptools import find_packages, setup

package_name = "py_node_template"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.launch.py")),
        (f"share/{package_name}/config", glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Calin Prutean",
    maintainer_email="calin.prutean@gmail.com",
    description="Python ROS 2 node that exchanges String messages with the C++ node.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "py_node = py_node_template.py_node:main",
        ],
    },
)
