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
import cgi
from publica.core.portal import Portal
from publica.utils.decorators import jsoncallback
from rauth_wrapper.oauth_manager import TwitterConnect

TWITTER_TOKEN_COOKIE_NAME = 'request_token'
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

    def _set_cookie(self, name, value):
        name_host = self.get_name_host()
        self.request.setCookie(name=name, value=value, host=name_host,
                               expires="")

    def get_name_host(self):
        return 'da.intip.com.br'

    @jsoncallback
    def twitter_authorize_url(self):
        t = self._get_twitter_connect()
        t.get_request_token()
        request_token = "%s|%s" % (t.request_token, t.request_token_secret)
        try:
            self._set_cookie(TWITTER_TOKEN_COOKIE_NAME, request_token)
        except Exception as e:
            return {'erro': e}
        return {'twitter_auth_url': t.get_authorize_url()}

    @jsoncallback
    def twitter_callback_url(self, oauth_verifier):
        try:
            request_token, request_secret = self.request.getCookie(
                TWITTER_TOKEN_COOKIE_NAME).split('|')
            t = self._get_twitter_connect()
            res = t.service.get_raw_access_token(
                request_token, request_secret,
                params={'oauth_verifier': oauth_verifier})
            content = cgi.parse_qs(res.content)
            access_token = "%s|%s" % (content['oauth_token'][0],
                                      content['oauth_token_secret'][0])
            self._set_cookie('access_token', access_token)
        except Exception as e:
            return {'erro': e}
        return {'ok': True}

    @jsoncallback
    def twitter_get_userinfo(self):
        try:
            token = self.request.getCookie('access_token').split('|')
            t = self._get_twitter_connect()
            session = t.service.get_session(token)
            userinfo = session.get('account/verify_credentials.json')
            return {'userinfo': userinfo.json()}
        except Exception as e:
            return {'erro': e}
