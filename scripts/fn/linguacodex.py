#!/usr/bin/python3
# ==============================================================================
#
#          FILE:  linguacodex.py
#
#         USAGE:  ./scripts/fn/linguacodex.py
#
#   DESCRIPTION: _[eng-Latn] Command line to process language codes
#                Install dependencies with
#                    pip install langcodes[data]
#                [eng-Latn]_
#                Trivia:
#                - lingua cōdex
#                  - https://en.wiktionary.org/wiki/lingua#Latin
#                  - https://en.wiktionary.org/wiki/codex#Latin
#
#       OPTIONS:  ---
#
#  REQUIREMENTS:  - python3
#                   - langcodes
#                     - https://github.com/rspeer/langcodes
#          BUGS:  ---
#         NOTES:  ---
#       AUTHORS:  Emerson Rocha <rocha[at]ieee.org>
# COLLABORATORS:  <@TODO: put additional non-anonymous names here>
#       COMPANY:  EticaAI
#       LICENSE:  Public Domain dedication OR Zero-Clause BSD
#                 SPDX-License-Identifier: Unlicense OR 0BSD
#       VERSION:  v0.5
#       CREATED:  2021-11-20 10:37 UTC v0.1 name langcodescli.py
#       CHANGED:  2021-11-21 04:59 UTC v0.5 renamed as linguacodex.py
# ==============================================================================
"""
python3 -m doctest ./scripts/fn/linguacodex.py
python3 -m doctest -v ./scripts/fn/linguacodex.py


>>> LinguaCodex(de_codex='pt').quid()
'{"de_codex": "pt", "de_codex_norma": "BCP47"}'
"""
import sys
import argparse
from pathlib import Path
import json
from dataclasses import dataclass, InitVar
from typing import (
    Any,
    Dict,
    Iterable,
    Optional,
    List,
    TextIO,
    Type,
    Union,
)

import langcodes


description = "_[eng-Latn]Command line to process language codes[eng-Latn]_"
epilog = """

ABOUT LANGUAGE-TERRITORY INFORMATION
(--speaking-population, --writing-population)
    The estimates for "writing population" are often overestimates,
    as described in the CLDR documentation on territory data.
    In most cases, they are derived from published data about literacy rates
    in the places where those languages are spoken.
    This doesn't take into account that many literate people around the
    world speak a language that isn't typically written,
    and write in a different language.
    See https://unicode-org.github.io/cldr-staging/charts/39/supplemental
    /territory_language_information.html

""".format(sys.argv[0])

# DATA_EXTERNAL = __file__ .
DATA_EXTERNAL = str(Path(__file__).parent.resolve()) + '/data-external'
DATA_EXTERNAL_CLDR_JSON = 'https://raw.githubusercontent.com/unicode-org/' + \
    'cldr-json/main/cldr-json/'

# print('HXLTM_SYSTEMA_DIR', HXLTM_SYSTEMA_DIR)

# TODO: https://stackoverflow.com/questions/39142778
#       /python-how-to-determine-the-language

parser = argparse.ArgumentParser(
    description=description,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=epilog
)
parser.add_argument(
    'language_code',
    help='The language code. Requires at least one option, like --info')
parser.add_argument(
    '--de_codex', action='store', help="""
    The main natural language to inspect using some well know language code.
    """)
# This is just in case we start to add new code standards
parser.add_argument(
    '--de_codex_norma', action='store', default='BCP47', help="""
    When using the code, specify the coding standard used. Defaults to BCP47
    """)
parser.add_argument(
    '--de_nomen', action='store', help="""
    The main natural language to inspect using the title of the language
    in some natural language.
    """)
parser.add_argument(
    '--info', action='store_true',
    help='General information (JSON output) [default]')
parser.add_argument(
    '--info-in-lang', help='Same as --help, ' +
    'but requires a language parameter to in which language return ' +
    ' the description. (JSON output)')
parser.add_argument(
    '--info-in-autonym', action='store_true',
    help='Same as --info-in-lang, but defaults language_code, e.g. autonym ' +
    '(JSON output)')
parser.add_argument(
    '--bcp47', action='store_true',
    help='Standardize the language code to BCP47 if already not is'
    '(string output) as BCP47')
parser.add_argument(
    '--is-valid-syntax', action='store_true',
    help='Check if is valid. Return 0 plus error code if so wrong ' +
    'that is not even recognizable')
parser.add_argument(
    '--speaking-population', action='store_true',
    help='Estimated speaking population. ')
parser.add_argument(
    '--writing-population', action='store_true',
    help='Estimated writing population')

parser.add_argument('--version', action='version', version='1.0.0')


class LinguaCodex:
    """
    _[eng-Latn]
    Command line to process language codes

    Trivia:
    - lingua cōdex
        - https://en.wiktionary.org/wiki/lingua#Latin
        - https://en.wiktionary.org/wiki/codex#Latin

    [eng-Latn]_
    """
    de_codex: str = None
    de_nomen: str = None
    de_exemplum: str = None
    de_codex_norma: str = 'BCP47'
    # nomen_lingua: str = None

    def __init__(
            self, de_codex: str = None,
            de_nomen: str = None,
            de_exemplum: str = None,
            de_codex_norma: str = 'BCP47'
    ):
        """LinguaCodex initiāle
        """
        if de_codex:
            self.de_codex = de_codex
        if de_nomen:
            self.de_nomen = de_nomen
        if de_exemplum:
            self.de_exemplum = de_exemplum
        if de_codex_norma:
            self.de_codex_norma = de_codex_norma

    # def quid(self):
    #     return LinguaCodexQuid.in_textum_json(self.__dict__)

    def quid(self, language_code, info_in_lang=False):
        result = langcodes.Language.get(language_code)
        if info_in_lang:
            if info_in_lang == 'autonym':
                result_item = result.describe(language_code)
            else:
                result_item = result.describe(info_in_lang)
        else:
            result_item = result.describe()

        result_item['bcp47'] = langcodes.standardize_tag(language_code)
        result_item['autonym'] = langcodes.Language.get(
            language_code).autonym()
        result_item['speaking_population'] = result.speaking_population()
        result_item['writing_population'] = result.writing_population()
        result_item['is_valid_syntax'] = langcodes.tag_is_valid(language_code)

        print(json.dumps(result_item))
        # print('ooi', result)


@dataclass
class LinguaCodexQuid:
    """LinguaCodexQuid

    Trivia:
        - fōrmātum, https://en.wiktionary.org/wiki/formatus#Latin
    [extended_summary]
    """
    lingua_codex: InitVar[Type['LinguaCodex']] = None

    def __init__(self, lingua_codex: Type['LinguaCodex']):
        """LinguaCodexQuid initiāle
        """
        self.lingua_codex = lingua_codex

    @staticmethod
    def in_textum_json(
            rem: Any,
            formosum: Union[bool, int] = None,
            clavem_sortem: bool = False,
            imponendum_praejudicium: bool = False
    ) -> str:
        """Trānslātiōnem: rem in textum JSON

        Trivia:
          - rem, https://en.wiktionary.org/wiki/res#Latin
          - in, https://en.wiktionary.org/wiki/in#Latin
          - json, https://www.json.org/
          - fōrmōsum, https://en.wiktionary.org/wiki/formosus
          - impōnendum, https://en.wiktionary.org/wiki/enforcier#Old_French
          - praejūdicium, https://en.wiktionary.org/wiki/praejudicium#Latin
          - sortem, https://en.wiktionary.org/wiki/sors#Latin
          - clāvem, https://en.wiktionary.org/wiki/clavis#Latin

        Args:
            rem ([Any]): Rem

        Returns:
            [str]: Rem in JSON textum

        Exemplōrum gratiā (et Python doctest, id est, testum automata):

>>> rem = {"b": 2, "a": ['ت', 'ツ', '😊']}

>>> LinguaCodexQuid.in_textum_json(rem)
'{"b": 2, "a": ["ت", "ツ", "😊"]}'

# >>> LinguaCodexQuid.in_textum_json(rem, clavem_sortem=True)
# '{"a": ["ت", "ツ", "😊"], "b": 2}'
#
# >>> LinguaCodexQuid.in_textum_json(rem, imponendum_praejudicium=True)
# '{"b": 2, "a": ["\\\u062a", "\\\u30c4", "\\\ud83d\\\ude0a"]}'
#
# >>> LinguaCodexQuid.in_textum_json(rem, formosum=True)
# '{\\n    "b": 2,\\n    \
# "a": [\\n        "ت",\\n        "ツ",\\n        "😊"\\n    ]\\n}'

        """

        # print = json.dumps()

        if formosum is True:
            formosum = 4

        json_textum = json.dumps(
            rem,
            indent=formosum,
            sort_keys=clavem_sortem,
            ensure_ascii=imponendum_praejudicium
        )

        return json_textum


def info(language_code, info_in_lang=False):
    result = langcodes.Language.get(language_code)
    if info_in_lang:
        if info_in_lang == 'autonym':
            result_item = result.describe(language_code)
        else:
            result_item = result.describe(info_in_lang)
    else:
        result_item = result.describe()

    result_item['bcp47'] = langcodes.standardize_tag(language_code)
    result_item['autonym'] = langcodes.Language.get(language_code).autonym()
    result_item['speaking_population'] = result.speaking_population()
    result_item['writing_population'] = result.writing_population()
    result_item['is_valid_syntax'] = langcodes.tag_is_valid(language_code)

    print(json.dumps(result_item))
    # print('ooi', result)


def is_valid_syntax(language_code):
    if langcodes.tag_is_valid(language_code):
        print(1)
        sys.exit(0)
    else:
        print(0)
        sys.exit(1)


def bcp47(language_code):
    print(json.dumps(langcodes.standardize_tag(language_code)))


def speaking_population(language_code):
    result = langcodes.Language.get(language_code)
    print(json.dumps(result.speaking_population()))


def writing_population(language_code):
    result = langcodes.Language.get(language_code)
    print(json.dumps(result.writing_population()))


def run_cli(args):
    if args.bcp47:
        return bcp47(args.language_code)
    if args.is_valid_syntax:
        return is_valid_syntax(args.language_code)
    if args.speaking_population:
        return speaking_population(args.language_code)
    if args.writing_population:
        return writing_population(args.language_code)
    if args.info_in_lang:
        return info(args.language_code, args.info_in_lang)
    if args.info_in_autonym:
        return info(args.language_code, 'autonym')
    if args.info:
        return info(args.language_code)

    # parser.print_help()
    # sys.exit(1)
    return info(args.language_code)


def run_cli(args):
    if args.bcp47:
        return bcp47(args.language_code)
    if args.is_valid_syntax:
        return is_valid_syntax(args.language_code)
    if args.speaking_population:
        return speaking_population(args.language_code)
    if args.writing_population:
        return writing_population(args.language_code)
    if args.info_in_lang:
        return info(args.language_code, args.info_in_lang)
    if args.info_in_autonym:
        return info(args.language_code, 'autonym')
    if args.info:
        return info(args.language_code)

    # parser.print_help()
    # sys.exit(1)
    return info(args.language_code)

# TODO: create a class just to simulate the cli interface
#       @see https://stackoverflow.com/questions/50886471
#       /simulating-argparse-command-line-arguments-input-while-debugging


# def linguacodex_cli(args):
# https://en.wiktionary.org/wiki/simulatio#Latin

# https://stackoverflow.com/questions/50886471
# /simulating-argparse-command-line-arguments-input-while-debugging
# /50886791#50886791


def linguacodex(argumenta: str):
    parts = 'linguacodex.py' + ' '.split(argumenta)
    sys.argv = parts
    args = parser.parse_args()
    print(run_cli(args))


if __name__ == '__main__':

    args = parser.parse_args()

    if len(sys.argv) > 1:
        run_cli(args)
    else:
        parser.print_help()
        sys.exit(1)
