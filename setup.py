import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-private-media',
    version = '0.1.2',
    packages = find_packages(),
    include_package_data = True,
    license = 'BSD License',
    description = """Private media for Django. Check the user's authorization before serving files at PRIVATE_MEDIA_URL, uploaded to PRIVATE_MEDIA_ROOT.""",
    long_description = README,
    keywords = "private media xsendfile",
    url = 'https://github.com/RacingTadpole/django-private-media',
    author = 'Arthur Street',
    author_email = 'arthur@racingtadpole.com',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe = False,
)
