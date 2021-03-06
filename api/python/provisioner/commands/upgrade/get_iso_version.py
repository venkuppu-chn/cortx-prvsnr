#
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.
#
import logging
from typing import Type, Union

from packaging import version
from provisioner import inputs
from provisioner.commands import CommandParserFillerMixin, RunArgsEmpty
from provisioner.vendor import attr

from .get_swupgrade_info import GetSWUpgradeInfo

from provisioner.commands.release import GetRelease

from provisioner.errors import ProvisionerError

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class GetISOVersion(CommandParserFillerMixin):
    """
    Base class that provides API for getting ISO Version information.
    """

    input_type: Type[inputs.NoParams] = inputs.NoParams
    _run_args_type = RunArgsEmpty

    @staticmethod
    def run() -> Union[str, None]:
        """
        Implementation of `get_iso_version` command.

        Returns
        -------
        Union[str, None]:
            Return string with SW upgrade ISO version if it is higher then
            release version. Return None if SW upgrade ISO version is equal
            to release version. Raise exception otherwise

        """

        release_ver = GetRelease.cortx_version()
        upgrade_ver = GetSWUpgradeInfo.cortx_version()

        if upgrade_ver is None:
            return None  # There are no configured upgrade repos

        release_ver_parsed = version.parse(release_ver)
        upgrade_ver_parsed = version.parse(upgrade_ver)

        if upgrade_ver_parsed > release_ver_parsed:
            return str(upgrade_ver)
        elif upgrade_ver_parsed == release_ver_parsed:
            return None
        else:  # upgrade_ver < release_ver
            raise ProvisionerError(
                "Upgrade version is lower than currently installed one"
            )
