#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil
import sys
from io import open

from setuptools import find_packages, setup
import traceback

extra_params = {}
setup_requires = [
    'sphinx==2.2.0',
    'sphinxcontrib-inlinesyntaxhighlight==0.2']

try:
    from pip._internal import main
    main(['install'] + setup_requires)
    setup_requires = []
except Exception:
    # Going to use easy_install for
    traceback.print_exc()


def read(f):
    return open(f, 'r', encoding='utf-8').read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

from sphinx.setup_command import BuildDoc

cmdclass = {
    'docs': BuildDoc
}

version = get_version('{{ project_name | lower }}')
name = 'davinci-crawling-{{ project_name | lower }}'

if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('davinci-crawling-{{ project_name | lower }}.egg-info')
    sys.exit()

setup(
    name=name,
    version=version,
    url='http://buildgroupai.com',
    license='MIT',
    description='Django DaVinci Crawler {{ project_name }}.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Javier Alperte',
    author_email='xalperte@buildgroupai.com',  # SEE NOTE BELOW (*)
    packages=find_packages(where="src", exclude=['tests*']),
    package_dir={"": "src"},
    include_package_data=True,
    cmdclass=cmdclass,
    command_options={
        'docs': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', name),
            'source_dir': ('setup.py', 'docs'),
            'build_dir': ('setup.py', '_build_docs')}},
    setup_requires=setup_requires,
    install_requires=[
        'psycopg2-binary>=2.7.5',
        'python-dateutil>=2.7.5',
        'solrq>=1.1.0',
        'gunicorn>=19.9.0',
        'dse-driver>=2.6',
        # 'cassandra-driver>=3.15.0',
        'django_compressor>=2.2',
        'django-configurations==2.1',
        'django-davinci-crawling==0.1.5-SNAPSHOT',
        #'pyscaffoldext-django==0.1b1',
        #'sphinx==2.2.0',
        #'sphinxcontrib-inlinesyntaxhighlight==0.2',
    ],
    tests_require=[
        'django-debug-toolbar>=1.10.1',
        'django-extensions>=2.1.3',
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    dependency_links=[
        "git+ssh://git@github.com/buildgroupai/django-davinci-crawling.git"
        "@clients-support_external-systems#"
        "egg=django-davinci-crawling-0.1.5-SNAPSHOT",
    ],
)

# (*) Please direct queries to the discussion group, rather than to me directly
#     Doing so helps ensure your question is helpful to other users.
#     Queries directly to my email are likely to receive a canned response.
#
#     Many thanks for your understanding.
