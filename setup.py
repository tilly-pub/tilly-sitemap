import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as f:
    requirements = [line.strip().split('#')[0] for line in f.read().split('\n') if line.strip().split('#')[0]]

setuptools.setup(
    name="tilly-sitemap",
    version="0.0.6",
    author="Ronald Luitwieler",
    author_email="ronald.luitwieler@gmail.com",
    description="Tilly plugin creating a sitemap.xml",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tilly-pub/tilly-sitemap",
    packages=setuptools.find_packages(),
    py_modules=["tilly_sitemap"],
    install_requires=requirements,
    entry_points={
        "tilly": ["sitemap = tilly_sitemap.main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
