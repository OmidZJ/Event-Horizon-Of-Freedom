from setuptools import setup, find_packages

setup(
    name='eventhorizon',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'speedtest-cli',
    ],
    entry_points={
        'console_scripts': [
            'eventhorizon = eventhorizon.core:main',
        ],
    },
    description='A tool for scanning domains for Fastly, G Core, Cloudflare, and other services.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/OmidZJ/Event-Horizon-Of-Freedom',  # Update this with your actual repository URL
    author='Omid',
    author_email='zamanijamshidi.omid@gmail.com',
    license='MIT',
)
