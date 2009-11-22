from setuptools import setup, find_packages

install_requires = [
        'setuptools',
        'Django',
        'pysolr',
]

dependency_links = [
        'http://pypi.saaskit.org/pysolr/',
        'http://dist.repoze.org',
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
           dependency_links = dependency_links,
)
