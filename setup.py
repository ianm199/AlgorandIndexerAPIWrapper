from setuptools import setup


with open("requirements.txt") as f:
    INSTALL_REQUIRES = [l.strip() for l in f.readlines() if l]

setup(
    name="algo-indexer-api",
    version="1.0",
    long_description="Wrapper around the AlgoExplorer Indexer API",
    install_requires=INSTALL_REQUIRES,
    license="MIT License",
    entry_points={
        "console_scripts":
            ["indexer-api = algo_indexer_api_v2.py"]
    }
)