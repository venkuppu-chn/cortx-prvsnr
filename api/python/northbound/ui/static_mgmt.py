#!/usr/bin/env python
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
#
from .form_window import FormWindow
from provisioner.northbound.data.models import MgmtNetworkModel
from ..data.data_store import PillarStore


class StaticMGMTNetworkWindow(FormWindow):

    data = {
            'Interfaces Mgmt': {
                      'default': 'eth0',
                      'pillar_key': 'srvnode-0/network/mgmt/public_ip'
                  },
            'Ip Mgmt': {
                      'default': '10.10.10.12',
                      'validation': 'ipv4',
                      'pillar_key': 'srvnode-0/network/mgmt/public_ip'
                  },
            'Netmask Mgmt': {
                           'default': '1.255.255.252',
                           'validation': 'ipv4',
                           'pillar_key': 'srvnode-0/network/mgmt/netmask'
                       },
            'Gateway Mgmt': {
                           'default': '198.162.0.2',
                           'validation': 'ipv4',
                           'pillar_key': 'srvnode-0/network/mgmt/gateway'
                       }
           }
    component_type = 'Management Network'


    def action(self):
        content = {'_'.join(key.split(" ")): val['default'] for key, val in self.data.items()}
        mgmt_network = MgmtNetworkModel(**content)
        PillarStore().store_data(mgmt_network)
        result = True
        err = None
        try:
            print()
            #set_ntp()
            #print("test")
        except Exception as exc:
            result = False
            err = str(exc)
        return result, err