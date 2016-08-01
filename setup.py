from distutils.core import setup
import versioneer

description = "A python package for analyzing artificial grammar strings"

setup(
    name='aglcheck',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=['aglcheck', 'aglcheck.tests'],
    package_data={'aglcheck': ['datafiles/*.yaml']},
    url='',
    license='BSD',
    author='Gabriel Beckers ',
    author_email='g.j.l.beckers@uu.nl',
    description=description, requires=['numpy', 'matplotlib', 'yaml', 'pandas']
)
