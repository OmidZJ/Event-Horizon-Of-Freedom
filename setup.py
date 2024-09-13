from setuptools import setup, find_packages

setup(
    name='myproxy',
    version='0.1',
    description='A tool for testing and configuring VLESS links with Xray.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'speedtest-cli',
    ],
    entry_points={
        'console_scripts': [
            'myproxy = myproxy.__main__:main',
        ],
    },
)
