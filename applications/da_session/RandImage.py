# -*- coding: latin1 -*-
from publica.utils.packages.pil.PIL import Image
from publica.utils.packages.pil.PIL import ImageDraw
from publica.utils.packages.pil.PIL import ImageColor
from publica.utils.packages.pil.PIL import ImageFont
from random import choice, randint
from string import digits, ascii_uppercase, ascii_lowercase
from os import listdir
import glob
from os.path import dirname, join
from StringIO import StringIO

class RandImage:


    def __init__(self, fontpath):
        self.fontpath = fontpath

    def ger_rand_text(self, c):
        caracteres = list('ABCDEFGHKMNPQRSTUVWXYZ23456789')
        resultado = []
        for i in range(c):
            resultado.append(choice(caracteres))
        return "".join(resultado)

    def get_new_image(self, c = 5, insensitive = 1): #sessao,#sessao,
        """ gera uma imagem com texto aleatorio no tamanho de 90x19 com o
        numero 'c' de caracteres e guarda uma variavel na session
        @param c: numero de caracteres que a imagem tera
        @type c: int
        @param insensitive: se vier True o texto setado na session sera
        todo em minusculo
        @param REQUEST: recebe o REQUEST do contexto para guardar o texto
        na session
        @type REQUEST: dicionario
        @since: 14/06/2005 """
        imgsize = (125, 35)
        #img = Image.new('RGB', imgsize, color = (228, 245, 250))
        img = Image.new('RGB', imgsize, color = (255, 2121, 250))
        #raise str(choice(glob.glob(self.fontpath+'*.ttf')))
        #Sorteia um ttf aleatorio do diretorio informado
        fonts = glob.glob(self.fontpath+'/*.ttf')
        if(not(fonts)):
            raise 'Não existe fontes no direotiro solicitado: %s ' % self.fontpath+'/*.ttf'
        fontf = join(self.fontpath, choice(fonts))
        #fontf = join(self.fontpath, choice(listdir(self.fontpath)))
        #fontf = join(self.fontpath, "cour.ttf")
        # linhas do fundo
        draw = ImageDraw.Draw(img)
        for i in range(0, imgsize[0] + 50, 5):
            draw.line((i, 0, 0, i), fill = (255, 255, 255))

        # borda da imagem
        draw.rectangle((0, 0, imgsize[0]-1, imgsize[1]-1),
                        outline = (146, 214, 251))

        # desenha o texto randomico
        texto = self.ger_rand_text(c)
        textop = " ".join(list(texto))
        if insensitive:
            texto = texto.lower()

        fontt = ImageFont.truetype(fontf, 20)
        #Ellipse´s
        for i in range(0, 128):
            color = (randint(150, 255), randint(150, 255), randint(150, 255))
            pos   = (randint(0, imgsize[0]),
                     randint(0, imgsize[1]),
                     randint(0, imgsize[0]),
                     randint(0, imgsize[1]))
            p1   = (randint(0, imgsize[0]),
                    randint(0, imgsize[1]))
            draw.ellipse(pos, fill = color)
        #line´s
        for i in range(0, 32):
            color = (randint(150, 255), randint(150, 255), randint(150, 255))
            pos   = (randint(0, imgsize[0]),
                     randint(0, imgsize[1]),
                     randint(0, imgsize[0]),
                     randint(0, imgsize[1]))
            p1   = (randint(0, imgsize[0]),
                    randint(0, imgsize[1]))
            draw.line(pos, fill = color)
        draw.text((8, 1), textop, fill = (40, 40, 40, 40), font = fontt)

        img2 = StringIO()
        img.save(img2, 'PNG')
        img2.seek(0)
        return [img2.read(),texto]


