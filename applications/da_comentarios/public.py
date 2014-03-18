# coding: utf-8
#
# Copyright 2009 Prima Tech Informatica Ltda.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.cmspublica.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from publica.core.portal import Portal
from datetime import datetime
from rauth_wrapper.oauth_manager import TwitterConnect

TWITTER_OAUTH_COOKIE_NAME = 'oauth_verifier'


class Public(object):

    @property
    def _session_data(self):
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        dados = portal._getApp(env_site=self.id_site,
                               schema=self.schema)
        return dados["dados"]

    def _get_twitter_connect(self):
        return TwitterConnect(self._session_data['twitter_consumer_key'],
                              self._session_data['twitter_consumer_secret'])

    def twitter_authorize_url(self):
        t = self._get_twitter_connect()
        t.get_request_token()
        return {'twitter_auth_url': t.get_authorize_url()}

    def twitter_callback_url(self, oauth_verifier):
        name_host = self._session_data["site"]
        expires = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.request.setCookie(
            name=TWITTER_OAUTH_COOKIE_NAME,
            value=oauth_verifier,
            host=name_host,
            expires=expires)

    def twitter_get_userinfo(self):
        oauth_verifier = self.request.getCookie(TWITTER_OAUTH_COOKIE_NAME)
        t = self._get_twitter_connect()
        session = t.get_session(oauth_verifier)
        userinfo = session.get('account/verify_credentials.json')
        return {'userinfo': userinfo}

