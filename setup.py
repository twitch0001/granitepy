from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = "granitepy",
    packages = ['andesite'],
    version = "0.0.13a",
    description = "A library for the lavalink like audio provider called andesite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = "twitch#7443",
    author_email = "twitch@trenchbot.xyz",
    url = "https://github.com/twitch0001/granitepy",
    keywords = ['andesite'],
    install_requires=['websockets>=6.0,<7.0', 'aiohttp', 'discord.py'],
    classifiers = [
        "Framework :: AsyncIO",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet"
    ]

)

