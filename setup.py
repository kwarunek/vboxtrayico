from setuptools import setup


setup(
    name="vboxtray",
    packages=['vboxtray'],
    version="0.1.5",
    author="kwarunek",
    author_email="kalmaceta@gmail.com",
    description="Virtualbox tray tool - list/start/stop VMs",
    license="MIT",
    keywords="virtualbox tray pysidel",
    url="https://github.com/kAlmAcetA/vboxtray",
    long_description='Virtualbox icon tray. Quick access start/stop VMs',
    entry_points={
        'console_scripts': ['vboxtray = vboxtray.core:main']
    },
)
