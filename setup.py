"""Artist-listener models package setup file."""

from setuptools import find_packages
from setuptools import setup


def read_requirements(path):
    """Read requirements from file."""
    requirements = []
    with open(path, 'r') as fd:
        requirements = [
            req.strip() for req in fd.readlines() if not req.startswith('-')]
        return requirements


setup(
    name='artist_listener_models',
    version='1.0',
    description='Package for creating artist-listener models',
    packages=find_packages(),
    install_requires=list(read_requirements('requirements.txt')),
    entry_points=dict(
        console_scripts=[
            'artist_listener_train = artist_listener_models.train:main',
            'artist_listener_insights = artist_listener_models.insights:main',
            'artist_listener_upload = artist_listener_models.upload:main']))
