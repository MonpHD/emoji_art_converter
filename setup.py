from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="emoji-art-converter",
    version="1.0.0",
    description="Convert images to colorful emoji art for SMS, messaging, and fun!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deinname/emoji-art-converter",  # optional
    author="MonpHD",
    author_email="deine@email.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="emoji, art, converter, image, ascii, sms",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=9.0.0",
        "numpy>=1.21.0",
        "pyperclip>=1.8.2",
    ],
    extras_require={
        "gui": [],  # tkinter ist in der Standardbibliothek
    },
    package_data={
        "emoji_art_converter": ["data/*.json"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "emoji-art-converter=emoji_art_converter.gui:launch_gui",
        ],
    },
    project_urls={
        "Source": "https://github.com/deinname/emoji-art-converter",
    },
)