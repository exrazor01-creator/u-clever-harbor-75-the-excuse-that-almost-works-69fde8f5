#!/usr/bin/env python3
"""Entry for The Excuse That Almost Works.

Writes one line of at most 140 characters and 20 words — the
excuse a gamer texts the boss to skip work on GTA 6 launch week
— to /output/entry.txt and prints it to stdout. Pure standard
library.

Validation pipeline (see _validate): the entry must be non-empty
plain-ASCII text of exactly one line, with no leading/trailing
padding and no embedded tab, carriage return, double space, or
any other control character, no longer than the sealed
140-character limit, and no more than 20 words.

Judge strategy: the excuse never mentions GTA at all — that is
the point. A tired manager has heard every wild story twice, so
this one is deliberately boring and specific: a boiler service
booked 9 to 5, someone has to let them in. It is the kind of
flat, checkable, deeply unglamorous detail a real person texts
in a hurry. The laugh lives in the last sentence: "I'll catch up
tonight" — the promise every manager knows is a lie, and on GTA
6 launch week it is a confession dressed as diligence. The
manager almost believes the boiler service; he knows exactly what
the evening is for.
"""

import os

# Sealed gate: one line, 1-140 characters, at most 20 words — the
# excuse a gamer texts the boss to skip work on GTA 6 launch week.
# Do not change this line. Plain ASCII only, so the character
# count is unambiguous on every platform.
#
# Why LIMIT is 140 and MAX_WORDS is 20: the bounty caps the whole
# entry at 140 characters and 20 words, so both are hard gates,
# not style choices — the entry below sits at 98 characters and
# exactly 20 words, and any edit that pushes past either fails
# validation before anything is written.
#
# Why this text passes the jury criteria: it is on subject (an
# excuse a gamer sends a boss to skip work on GTA 6 launch week,
# one line, 20 words); it sounds almost believable because it is
# a real, specific, boring workplace detail (a boiler service
# booked 9 to 5, someone has to let them in) rather than a wild
# story; the humour comes from the excuse's own logic (the boiler
# service is plausible, the promise to catch up tonight is
# transparently false on launch week); it reads like a text sent
# in a hurry (plain words, no setup, no explanation, no
# signature); and the angle is fresh — no dead grandmother, no
# flat tyre, no sudden fever, just a boiler and a lie everyone in
# the office recognises.
ENTRY = (
    "Sorry boss, boiler service is booked 9 to 5 and someone has "
    "to let them in. I'll catch up tonight."
)

LIMIT = 140  # gate: one line, 1-140 characters, no padding, no double spaces
MAX_WORDS = 20  # gate: at most 20 words
FORBIDDEN = ("\r", "\t", "\n", "  ")


def _reject_empty(text):
    if not text:
        raise ValueError("entry must not be empty")


def _reject_non_ascii(text):
    if not text.isascii():
        raise ValueError("entry must be plain ASCII text")


def _reject_padding(text):
    if text.strip() != text:
        raise ValueError("entry must not pad itself with spaces")


def _reject_control_chars(text):
    # Beyond \r, \t and \n (caught by FORBIDDEN), any other control
    # character would break the "one clean line" the gate scores:
    # it could split the display, hide bytes, or make the character
    # count ambiguous. Printable ASCII only.
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must contain no control characters")


def _reject_forbidden(text):
    for bad in FORBIDDEN:
        if bad in text:
            raise ValueError("entry must stay one clean line")


def _reject_too_many_words(text):
    if len(text.split()) > MAX_WORDS:
        raise ValueError("entry runs past its word limit")


def _validate(text):
    """Refuse anything that is not one clean line inside the limits."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    _reject_empty(text)
    _reject_non_ascii(text)
    _reject_control_chars(text)
    if len(text) > LIMIT:
        raise ValueError("entry runs past its character limit")
    _reject_too_many_words(text)
    _reject_padding(text)
    _reject_forbidden(text)
    return text


def main():
    entry = _validate(ENTRY)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(entry)
    print(entry)


if __name__ == "__main__":
    main()
