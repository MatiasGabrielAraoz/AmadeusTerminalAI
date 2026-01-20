import ollama
import time
from threading import Thread
from queue import Queue
import sys
import subprocess

from sympy import true

print("Iniciando Amadeus...")

class Amadeusmodel:
    def __init__(self, model="llama3.2:3b-instruct-q4_K_M"):
        self.model = model
        self.system_prompt = self.CreateSystemPrompt()
        self.messages = []
        self.response_queue = Queue()
    def CreateSystemPrompt(self):
        system_prompt = "Eres Amadeus, la IA basada en Kurisu Makise de Steins;Gate. Tu propósito es asistir en programación usando analogías del anime: D-Mails para async, líneas mundiales para Git branches, atravesadores para algoritmos. Explicá conceptos técnicos con la precisión científica de Kurisu. Presentate y ofrecé ayuda con código. Tampoco quiero que hagas rol, quiero q funciones como una ia simplemente de utilidad que da respuestas con algún que otro tono de steins;gate. si escribo 'salir' es el comando para salir de amadeus, simplemente despidete y decí alguna frase relacionada a 'nos veremos en otra linea de tiempo' o algúna referencia, termina siempre con \\n para que se vea bien"
        return system_prompt
    def preloadModel(self):
        try:
            print("precargando modelo")
            ollama.generate(model=self.model, prompt=".", options={'num_predict': 1})
            print("Modelo precargado")
            return True
        except:
            print("Error generando a Amadeus")
            return False
    def sresponse(self, user_input, response_queue):
        try:
            messages_temp = [
                {'role': 'system', 'content':self.system_prompt},
                {'role': 'user', 'content':user_input}]
            stream = ollama.chat(model=self.model, messages=messages_temp,stream=True, options={'num_predict': 1024, 'temperature':0.7, 'top_p':0.9})
            respuesta = ''
            for chunk in stream:
                if 'content' in chunk['message']:
                    contenido = chunk['message']['content']
                    respuesta += contenido
                    response_queue.put(contenido)
            response_queue.put(None)

        except Exception as e:
            self.response_queue.put(f'\n Error: {e}')
    def Chat(self):
        print('='*50 + '\n' + 'Amadeus' + '\n' + '='*50)
        if not self.preloadModel():
            print("Cargando modelo")
        ruta_imagen = "~/Imágenes/Amadeusnf.png"
        subprocess.run(f'kitty +kitten icat --align left {ruta_imagen} ', shell=True, check=True)
        Continuar = True

        while Continuar == True:
            user_input = input("\n Usuario: ")
            if user_input == "salir":
                Continuar = False
            print('Amadeus: ', end='', flush=True )
            self.response_queue = Queue()
            thread = Thread(target=self.sresponse, args=(user_input,self.response_queue))
            thread.daemon = True
            thread.start()

            respuesta_completa = ''
            dots = 0
            ultima_impresión = time.time()
            while True:
                try:
                    chunk = self.response_queue.get(timeout=5.0)

                    if chunk is None:
                        break

                    print(chunk, end='', flush=True)
                    respuesta_completa += chunk
                    ultima_impresion = time.time()

                except:
                    continue

def main():
    modelo = 'llama3.2:3b-instruct-q4_K_M'
    Amadeus = Amadeusmodel(model=modelo)
    Amadeus.Chat()

if __name__ == '__main__':
    main()
