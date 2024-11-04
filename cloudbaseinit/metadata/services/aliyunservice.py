# Copyright 2024 Youfu Zhang
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log as oslo_logging

from cloudbaseinit import conf as cloudbaseinit_conf
from cloudbaseinit.metadata.services import base

CONF = cloudbaseinit_conf.CONF
LOG = oslo_logging.getLogger(__name__)


class AliyunService(base.BaseHTTPMetadataService):
    _metadata_version = '2016-01-01'

    def __init__(self):
        super(AliyunService, self).__init__(
            base_url=CONF.aliyun.metadata_base_url,
            https_allow_insecure=CONF.aliyun.https_allow_insecure,
            https_ca_bundle=CONF.aliyun.https_ca_bundle)
        self._enable_retry = True

    def load(self):
        super(AliyunService, self).load()

        try:
            self.get_host_name()
            return True
        except Exception as ex:
            LOG.exception(ex)
            LOG.debug('Metadata not found at URL \'%s\'' %
                      CONF.aliyun.metadata_base_url)
            return False

    def get_host_name(self):
        return self._get_cache_data('%s/meta-data/hostname' %
                                    self._metadata_version, decode=True)

    def get_instance_id(self):
        return self._get_cache_data('%s/meta-data/instance-id' %
                                    self._metadata_version, decode=True)

    def get_user_data(self):
        return self._get_cache_data('%s/user-data' %
                                    self._metadata_version)
