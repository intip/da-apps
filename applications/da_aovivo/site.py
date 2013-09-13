# -*- encoding: LATIN1 -*-
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


class Site(object):
    """
    """

    def _getTags(self, id_conteudo, text=None):
        """
        """
        portal = Portal(id_site=self.id_site,
                        request=self.request)
        for i in portal._getTags(env_site=self.id_site,
                                 id_conteudo=int(id_conteudo),
                                 schema=self.schema,
                                 text=None):
            yield i["tag"]

    # Hurdle

    def list_jogos(self):
        """ Retorna lista de jogos publicados
        """
        data = strftime('%Y-%m-%d %H:%M')
        return self.execSql('app', 'select_jogos_publicados', data=data)


    def get_jogo_placar(self, id_jogo):
        """
        """
        return self.execSql('app', 'select_jogo_placar', id_jogo=int(id_jogo)).next()


    def get_jogo_imagem(self, id_jogo):
        """
        """
        return self.execSql('app', 'select_jogo_imagem', id_jogo=int(id_jogo)).next()


    def get_jogo_dados(self, id_jogo):
        """
        """
        dados = self.execSql('app', 'select_jogo_dados', id_jogo=int(id_jogo)).next()
        h,m,s = dados['min'].split(':')
        m = int(h) * 60 + int(m)       
 
        dados['minutos'] = '%.2i' % m
        dados['segundos'] = '%.2i' % int(s)
        return dados


    def get_jogo_tempos(self, id_jogo):
        """
        """
        return self.execSql('app', 'select_jogo_tempos', id_jogo=int(id_jogo))

    
    def get_jogo_tempo_lance(self, id_tempo):
        """
        """
        return self.execSql('app', 'select_jogo_tempo_lance', id_tempo=int(id_tempo))


    def get_jogo_ficha(self, id_jogo):
        """
        """
        descricao = Jogo.get(int(id_jogo)).descricao
        cft = '<img src="%(arquivo)s" alt="" border="0"/>'
        index = 1

        for i in self.get_jogo_fotos(id_jogo):
            cfti = cft % {'arquivo' : self.retornarUrl(i.arquivo, id_site=self.id_site)}
            descricao = descricao.replace('[FOTO%s]' % index, cfti)
            index += 1

        return descricao
         

    def get_jogo_fotos(self, id_jogo):
        """
        """
        return Foto.select(Foto.q.id_jogo==int(id_jogo))


    def get_jogo_video(self, id_jogo):
        """
        """
        return Jogo.get(int(id_jogo)).html_videos


    def get_jogo_times(self, id_jogo):
        """
        """
        return self.execSql('app', 'select_jogo_times', id_jogo=int(id_jogo)).next()


    def get_jogo_titulares(self, id_time):
        """
        """
        return Escalacao.select(AND(Escalacao.q.id_time==int(id_time), Escalacao.q.titular==True))


    def get_jogo_reservas(self, id_time):
        """
        """
        return Escalacao.select(AND(Escalacao.q.id_time==int(id_time), Escalacao.q.titular==False))


