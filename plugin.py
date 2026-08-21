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

###
# Replace — a sed-style correction snarfer for Limnoria.
#
#   s/old/new/        Corrects the sender's last message in the channel,
#                      replacing the first occurrence of "old" with "new".
#   s/old/new/g       Replaces all occurrences (global).
#   s/old/new/i       Case-insensitive match.
#   @s/old/new/       Also accepted (the leading @ is stripped).
#
# The corrected line is posted back with a note of who corrected what.
# Works for any user (not just the bot owner).
###
import re

import supybot.conf as conf
import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring
_ = PluginInternationalization('Replace')


# Regex for the s/old/new/ syntax. We allow any non-slash delimiter? No,
# keep it simple: slash-delimited, with optional trailing flags (g/i).
REPLACE_RE = re.compile(
    r'^@?s/(?P<old>.+?)/(?P<new>.*?)/(?P<flags>[gi]*)$'
)


class Replace(callbacks.Plugin):
    """sed-style message correction (s/old/new/).

    When a user sends a message of the form 's/old/new/' (optionally prefixed
    with @), the bot takes that user's previous message in the channel,
    replaces the first occurrence of 'old' with 'new', and posts the
    corrected line along with a note of who corrected it.

    Flags: 'g' replaces all occurrences, 'i' is case-insensitive.
    """

    threaded = False
    priority = 100

    def __init__(self, irc):
        super().__init__(irc)
        # buffer of last message per (network, channel, nick)
        self._last = {}

    def _store_last(self, irc, msg):
        if not msg.channel or not msg.nick:
            return
        key = (irc.network, msg.channel, msg.nick)
        # Don't store the s/.../ command itself.
        text = msg.args[1] if len(msg.args) > 1 else ''
        if REPLACE_RE.match(text):
            return
        self._last[key] = text

    def doPrivmsg(self, irc, msg):
        """Handles incoming PRIVMSGs: stores the last message for each user
        and performs sed-style corrections when a message matches s/old/new/.
        """
        # Always remember the last normal message (for correction).
        self._store_last(irc, msg)

        if not msg.channel:
            return
        text = msg.args[1] if len(msg.args) > 1 else ''
        m = REPLACE_RE.match(text)
        if not m:
            return

        old = m.group('old')
        new = m.group('new')
        flags = m.group('flags')
        global_replace = 'g' in flags
        case_insensitive = 'i' in flags

        key = (irc.network, msg.channel, msg.nick)
        last = self._last.get(key)
        if not last:
            irc.reply(_('I haven\'t seen a previous message from you to '
                         'correct.'), to=msg.nick, private=False)
            return

        # Perform the replacement.
        if case_insensitive:
            pat = re.compile(re.escape(old), re.IGNORECASE)
        else:
            pat = re.compile(re.escape(old))
        count = 0 if global_replace else 1
        corrected, n = pat.subn(new, last, count)

        if n == 0:
            irc.reply(_('No occurrence of %s found in your last message.') % old,
                      to=msg.nick, private=False)
            return

        # Reply with the corrected line + who corrected.
        irc.reply(_('<%s> %s  (corrected by %s)') % (msg.nick, corrected, msg.nick),
                  to=msg.channel, private=False)

    doPrivmsg = wrap(doPrivmsg)

    def die(self):
        super().die()


Class = Replace

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
