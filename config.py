# Copyright (C) 2026  Youri Matthys (miruoy)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <https://www.gnu.org/licenses/>.

### Replace — configuration
import supybot.conf as conf
import supybot.utils as utils
from supybot.i18n import PluginInternationalization, internationalizeDocstring
_ = PluginInternationalization('Replace')

Replace = conf.registerPlugin('Replace')
# No configuration variables are needed for this plugin.
