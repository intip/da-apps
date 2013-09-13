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
from app import title, meta_type
from publica.utils.util import convertascii

## search information
schema = ()


def searchFields(data):

    return {"published": data["publicado_em"],
            "meta_type": meta_type,
            "schema": data["schema"],
            "id_site": data["id_site"],
            "id_cinema": data["id_cinema"],
            "id_content": data["id_content"],
            "id_treeapp": data["id_treeapp"],
            "id_aplicativo": data["id_aplicativo"]}
