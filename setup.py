from setuptools import setup

setup(
    name='GraphSpotify',
    packages=['GraphSpotify'],
    include_package_data=True,
    install_requires=[
        'flask',
        'spotipy',
        'lastfm'
    ],
)
