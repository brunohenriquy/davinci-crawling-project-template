
r"""

   ___      _   ___         _
  / _ \___ | | / (____ ____(_)
 / // / _ `| |/ / / _ / __/ /
/____/\_,_/|___/_/_//_\__/_/

"""

__title__ = 'Django DaVinci Crawler {{ project_name }}'
__version__ = '0.1.0'
__author__ = 'Javier Alperte'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018-2019 PreSeries Tech S.L.'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'

default_app_config = '{{project_name}}.apps.DaVinciCrawler{{ project_name }}Config'
