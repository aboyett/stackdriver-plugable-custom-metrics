#from setuptools import setup
import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=uuid.uuid1())
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='stackdriver-custom-metrics',
    version='0.1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=reqs
)
