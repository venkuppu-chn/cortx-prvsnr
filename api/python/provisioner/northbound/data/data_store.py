# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
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

"""North Bound Interface Data layer."""

from abc import ABC, abstractmethod
from provisioner.vendor import attr
from provisioner.commands import PillarSet
from .mapping import key_mapping
from cortx.utils.conf_store import Conf
from provisioner.commands import PillarGet


class DataStore(ABC):
    """Abstract data Storage Interface"""

    @abstractmethod
    def store_data(self, obj):
        """Store object into data store

            :param obj: Data object for storing into DS

        """
        pass

    @abstractmethod
    def get_data(self, model_name):
        """Get odata from data store

            :param model_name: Get data from DS using model_name

        """
        pass


class PillarStore(DataStore):
    """Pillar data store inteface."""

    def store_data(self, obj):
        data = attr.asdict(obj)
        result = True
        for key, value in data.items():
            try:
                PillarSet().run(key_mapping[key]['pillar_key'], value, local=True)
            except Exception:
                result = False
                break
        return result

    def get_data(self, key):
        result = True
        try:
            result = PillarGet().run(key_mapping[key]['pillar_key'], local=True)
        except Exception:
            result = False
        return result


class ConfStore(DataStore):
    """Confstore data store inteface."""
    _index = 'srvnode-0'
    _location = 'json:///etc/cortx/srvnode-0.conf'

    def get_location(self):
        return self._location

    def __init__(self):
        try:
            Conf.load(self._index, self._location)
        except Exception as exc:
            err = str(exc)
            if 'already exists' not in err: 
                raise
    
    def store_data(self, obj):
        data = attr.asdict(obj)
        result = True
        
        for key, value in data.items():
            try:
                Conf.set(self._index, key_mapping[key]['confstore_key'], value)
            except Exception:
                result = False
                break
        Conf.save(self._index)
        return result

    def get_data(self, index_name):
        return Conf.get(self._index, index_name)