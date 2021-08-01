# This file is part of Scanarium https://scanarium.com/ and licensed under the
# GNU Affero General Public License v3.0 (See LICENSE.md)
# SPDX-License-Identifier: AGPL-3.0-only

import json
import logging
import os

from .Localizer import Localizer

logger = logging.getLogger(__name__)


class LocalizerFactory(object):
    def __init__(self, localization_dir_abs, config=None):
        super(LocalizerFactory, self).__init__()
        self._localization_dir_abs = localization_dir_abs
        self._config = config
        self._instances = {}

    def get_localizer(self, language=None):
        try:
            ret = self._instances[language]
        except KeyError:
            translations = {}

            if language is not None:
                json_file_abs = os.path.join(
                    self._localization_dir_abs, f'{language}.json')
                if os.path.isfile(json_file_abs):
                    with open(json_file_abs, 'r') as file:
                        translations = json.load(file)
            ret = Localizer(translations, self._config)
            self._instances[language] = ret

        return ret
