from setuptools import setup, find_packages

install_requires = [
        'setuptools',
        'Django',
]
 
setup(name="saaskit-tracker",
           version="0.1",
           description="group keywords and setup keywords per tracker/channel",
           author="CrowdSense",
           author_email="admin@crowdsense.com",
           packages=find_packages(),
           include_package_data=True,
           install_requires = install_requires,
           entry_points="""
           # -*- Entry points: -*-
           """,
           dependency_links = ['http://dist.repoze.org',],
)
