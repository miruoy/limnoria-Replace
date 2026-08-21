# Replace

A Limnoria plugin that adds sed-style message correction, safe for all
users (no shell, no network access, no command-prefix required).

## What it does

When a user sends a message of the form `s/old/new/`, the bot takes that
user's **previous message in the channel**, replaces the first occurrence of
`old` with `new`, and posts the corrected line back with a note of who
corrected it.

Flags:
- `g` — replace **all** occurrences (global)
- `i` — case-**insensitive** match

Examples (all valid):
```
s/teh/the/        # correct "teh" to "the" in your last message
s/iet/iets/g      # replace every "iet" with "iets"
@s/de/te/i        # @-prefixed also works; case-insensitive
```

The leading `@` is optional — both `s/.../` and `@s/.../` are accepted.

## Notes

- The correction applies to **the sender's own last message** in that
  channel (any user can correct their own messages).
- The bot remembers only the most recent message per user/channel, so
  corrections must follow shortly after the original message.
- This is a **snarfer**, not a command — you do not need a command prefix
  (though `@` is tolerated).

## Installation

### Via git (copy into plugins dir)
```bash
cp -r limnoria-Replace /path/to/your/bot/plugins/
rm -rf /path/to/your/bot/plugins/limnoria-Replace/__pycache__
# in the bot:
load Replace
```

### Via pip (from the git repo)
```bash
pip3 install git+https://github.com/miruoy/limnoria-Replace.git
# then in the bot:
load Replace
```

If you are replacing a previously loaded copy and the bot keeps running old
code, remove the `__pycache__` directory and `touch` the `.py` files (or
unload, delete, re-copy under a new name, then load) before reloading — a
stale `.pyc` will keep the old code live.

## License

Licensed under the GNU General Public License v2 (GPL-2.0). See the
`LICENSE` file for the full text.
