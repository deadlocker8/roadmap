from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from blueprints.RoadmapAPI import RoadmapParameters
from logic import Constants

if TYPE_CHECKING:
    from logic.Database import Database

LOGGER = logging.getLogger(Constants.APP_NAME)


class DatabaseMigrator:
    def __init__(self, database: Database):
        self._database = database

    def migrate(self):
        latestVersion = self._database.VERSION
        currentVersion = self._database.get_version()

        while currentVersion < latestVersion:
            self.__migrate_version(currentVersion)
            currentVersion = self._database.get_version()

        if latestVersion == currentVersion:
            LOGGER.debug(f'Database version: {latestVersion} (latest)')
            return

    def __migrate_version(self, currentVersion):
        from logic.Database import FetchType

        if currentVersion == 1:
            LOGGER.debug('Migrating database from version 1 to 2...')

            queryColumnExists = f'SELECT EXISTS (SELECT 1 FROM information_schema.columns ' \
                                f'WHERE table_name=\'roadmaps\' AND column_name=\'{RoadmapParameters.HIDDEN.value}\');'
            exists = self._database._query(queryColumnExists, fetch_type=FetchType.ONE)

            if not exists['exists']:
                query = f'ALTER TABLE "roadmaps" ADD "{RoadmapParameters.HIDDEN.value}" boolean NOT NULL DEFAULT false;'
                self._database._query(query, fetch_type=FetchType.NONE)

            self._database.update_version(2)
            return

        if currentVersion == 2:
            LOGGER.debug('Migrating database from version 2 to 3...')

            queryColumnExists = f'SELECT EXISTS (SELECT 1 FROM information_schema.columns ' \
                                f'WHERE table_name=\'roadmaps\' AND column_name=\'{RoadmapParameters.START_DATE.value}\');'
            exists = self._database._query(queryColumnExists, fetch_type=FetchType.ONE)

            if not exists['exists']:
                query = f'ALTER TABLE "roadmaps" ADD "{RoadmapParameters.START_DATE.value}" date NOT NULL default \'01.01.2000\';'
                self._database._query(query, fetch_type=FetchType.NONE)

            self._database.update_version(3)
            return

        raise ValueError(f'No migration handler for version {currentVersion} defined')
