from setuptools import setup, find_packages


setup(
    name='ud4d',
    version='0.1.0',
    description='USB Device Detector for Docker usage. Support Linux only.',
    author='williamfzc',
    author_email='fengzc@vip.qq.com',
    url='https://github.com/doringland/ud4d',
    packages=find_packages(),
    install_requires=[
        'logzero',
        'docker',
        'flask'
    ]
)
