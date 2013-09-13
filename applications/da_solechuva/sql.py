# -* encoding: LATIN1 -*-
#
# Copyright 2009 Prima Tech.
#
# Licensed under the Environ License, Version 1.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.intip.com.br/licenses/ENVIRON-LICENSE-1.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
select_previsao  = ("SELECT cidade, data, tempo, precipitacao, temperatura_minima, temperatura_maxima "
                    "FROM rschemar.previsao "
                    "WHERE cidade=%(cidade)s and data=%(data)s LIMIT %(limit)i")

delete_previsao  = ("DELETE FROM rschemar.previsao WHERE cidade=%(cidade)s")

insert_previsao  = ("INSERT INTO rschemar.previsao (cidade, data, "
                    "tempo, precipitacao, temperatura_minima, temperatura_maxima) VALUES "
                    "(%(cidade_id)s, %(data)s, %(tempo)s, %(precipitacao)s, "
                    "%(temperatura_minima)s, %(temperatura_maxima)s)")

permissions = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT ON rschemar.previsao TO %(user)s;
"""

permissions_admin = """
  GRANT USAGE ON SCHEMA rschemar TO %(user)s;
  GRANT SELECT, INSERT, UPDATE, DELETE ON rschemar.previsao TO %(user)s;
"""

structure = """
  CREATE SCHEMA rschemar;

  CREATE TABLE rschemar.previsao (
    cidade VARCHAR NOT NULL,
    data DATE NOT NULL,
    tempo VARCHAR NOT NULL,
    precipitacao VARCHAR NOT NULL,
    temperatura_minima VARCHAR NOT NULL,
    temperatura_maxima VARCHAR NOT NULL
  );
  CREATE INDEX rschemar_previsao_cidade_index ON rschemar.previsao USING btree (cidade);
  CREATE INDEX rschemar_previsao_data_index ON rschemar.previsao USING btree (data);
  CREATE INDEX rschemar_previsao_cidade_data_index ON rschemar.previsao USING btree (cidade, data);
"""
