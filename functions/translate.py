import os
import sys

FILE_DIR_ABS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, FILE_DIR_ABS)
from translate.LocalizerFactory import LocalizerFactory
del sys.path[0]

LOCALIZER_FACTORY = None


def get_localizer(language):
    global LOCALIZER_FACTORY
    if LOCALIZER_FACTORY is None:
        localization_dir = os.path.join(
            FILE_DIR_ABS, 'translate', 'localizations')
        LOCALIZER_FACTORY = LocalizerFactory(localization_dir)
    return LOCALIZER_FACTORY.get_localizer(language)

def translate(file, state, args):
    localizer = get_localizer(file['properties']['language'])
    ret = None
    len_args = len(args)
    if len_args == 1:
        ret = localizer.localize_template(args[0])
    elif len_args == 2:
        ret = localizer.localize_parameter(args[0], args[1])
    else:
        raise RuntimeError(
            f'Unexpected length length {len_args} of argument list')

    return ret

def dumpLanguageMatrix(file, state, args):
    l10ns = file['properties']['build_localizations'].split(',')
    lst = [];
    for ui_l10n in l10ns:
        localizer = get_localizer(ui_l10n)
        for target_l10n in l10ns:
            value = localizer.localize_parameter('language', target_l10n)
            lst.append(f'{ui_l10n}-{target_l10n}:{value}')
    return ','.join(lst)
