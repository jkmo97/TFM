# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []





import json
import random
from typing import Any, List, Dict, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class Coger_Intent(Action):
    def name(self) -> Text:
        return "Coger_Intent"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obtener el intent reconocido en el mensaje del usuario
        recognized_intent = tracker.latest_message.get("intent", {}).get("name")
        
        # Variable para almacenar la respuesta encontrada
        selected_response = None

        # Ruta del archivo JSON específico para Telefónica
        telefonica_json = "/Users/kevinmafla/tfm/data/data_telefonica.json"
        bbva_json = "/Users/kevinmafla/tfm/data/data_bbva.json"
        inditex_json = "/Users/kevinmafla/tfm/data/data_inditex.json"
        santander_json= "/Users/kevinmafla/tfm/data/data_santander.json"

        if recognized_intent == "preguntar_precio_accion_telefonica":
            with open(telefonica_json, "r", encoding="utf-8") as file:
                context_dict = json.load(file)
            
            target_phrase = "11,92 euros por acción"
            available_contexts = context_dict.get("por_acción_telefonica", [])
            selected_context = next((context for context in available_contexts if target_phrase in context), None)

            if selected_context:
                dispatcher.utter_message(selected_context)
                return []

        if recognized_intent == "dividendos_telefonica":
            with open(telefonica_json, "r", encoding="utf-8") as file:
                context_dict = json.load(file)
            
            target_phrase = "En términos de dividendo"
            available_contexts = context_dict.get("por_acción_telefónica", [])
            selected_context = next((context for context in available_contexts if target_phrase in context), None)

            if selected_context:
                dispatcher.utter_message(selected_context)
                return []
        if recognized_intent == "preguntar_precio_accion_santander":
            with open(santander_json, "r", encoding="utf-8") as file:
                context_dict = json.load(file)
            
            target_phrase = "5,48 euros"
            available_contexts = context_dict.get("por_acción_santander", [])
            selected_context = next((context for context in available_contexts if target_phrase in context), None)
            if selected_context:
                dispatcher.utter_message(selected_context)
                return []           

        if recognized_intent == "dividendos_santander":
            with open(santander_json, "r", encoding="utf-8") as file:
                context_dict = json.load(file)
            
            target_phrase = "Política de dividendos"
            available_contexts = context_dict.get("por_acción_santander", [])
            selected_context = next((context for context in available_contexts if target_phrase in context), None)
            
            if selected_context:
                dispatcher.utter_message(selected_context)
                return []

        if recognized_intent == "dividendos_inditex":
            with open(inditex_json, "r", encoding="utf-8") as file:
                context_dict = json.load(file)
            
            target_phrase = "dividendo de 0,75 euros"
            available_contexts = context_dict.get("por_acción_inditex", [])
            selected_context = next((context for context in available_contexts if target_phrase in context), None)

            if selected_context:
                dispatcher.utter_message(selected_context)
                return []

        if recognized_intent == "preguntar_precio_accion_inditex":
            # Cargar el diccionario desde el archivo JSON
            with open(inditex_json, "r", encoding="utf-8") as file:
                context_dict = json.load(file)
            target_phrase = "28,87 euros por acción"    
            available_contexts = context_dict.get("por_acción_inditex", [])
            selected_context = next((context for context in available_contexts if target_phrase in context), None)

            if selected_context:
                dispatcher.utter_message(selected_context)
                return []


        # Si no se encontró la respuesta en el archivo específico, continuar con la búsqueda en los demás archivos
        json_files = [
            "/Users/kevinmafla/tfm/data/data_bbva.json",
            "/Users/kevinmafla/tfm/data/data_santander.json",
            "/Users/kevinmafla/tfm/data/data_inditex.json",
            "/Users/kevinmafla/tfm/data/data_telefonica.json"]
       
        if selected_response is None:
            responses = []
            for json_file in json_files:
                with open(json_file, "r", encoding="utf-8") as file:
                    context_dict = json.load(file)
                    if recognized_intent in context_dict:
                        responses.extend(context_dict[recognized_intent])

            # Si se encontraron respuestas, seleccionar aleatoriamente una respuesta
            if responses:
                selected_response = random.choice(responses)

        # Enviar la respuesta al usuario
        if selected_response:
            dispatcher.utter_message(selected_response)
        else:
            dispatcher.utter_message("""Lo siento, no tengo una respuesta para eso que has preguntado. Puedes intentar hacer otra pregunta.
            Recuerda que poseo información de los informes anuales de Telefónica en 2014, BBVA en 2016, Santander en 2017 e Inditex en 2017.
            Para Telefónica tengo la siguiente información:
                - sostenibilidad y medio ambiente
                - Política social y educación
                - Número de empleados
                - Indicadores financieros: OIBDA, beneficio neto, dividendos, cotización
            
            Para Santander tengo la siguiente información:
                - sostenibilidad y medio ambiente
                - Política social y educación
                - Número de empleados
                - Indicadores financieros: beneficio ordinario antes de impuestos, beneficio atribuido, beneficio ordinario atribuido, dividendos
            
            Para BBVA tengo la siguiente información:
                - sostenibilidad y medio ambiente
                - Política social y educación
                - Número de empleados
                - Indicadores financieros: beneficio atribuido, cotización, dividendos
                - Donaciones

            Para Inditex tengo la siguiente información:
                - sostenibilidad y medio ambiente
                - Política social y educación
                - Número de empleados
                - Indicadores financieros: beneficio, ebitda, dividendos, cotización

    
            """)

        return []





from rasa_sdk import Action
from rasa_sdk.events import SlotSet


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionProporcionarInfoEntidad(Action):
    def name(self) -> Text:
        return "action_info_entidad"


    def run(self, dispatcher, tracker, domain):
        # Obtener la entidad detectada en el mensaje
        entity = tracker.latest_message.get('entities', [{}])[0].get('entity')

        # Mapea la empresa con la entidad
        if entity == 'BBVA':
            entidad = 'BBVA'
        elif entity == 'Santander':
            entidad = 'Santander'
        elif entity == 'Inditex':
            entidad = 'Inditex'
        elif entity == 'Telefónica':
            entidad = 'Telefónica'
        else:
            dispatcher.utter_message("¿Podrías repetir la pregunta?")

        # Genera la pregunta
        pregunta = f"Qué te gustaría saber sobre {entidad}?"

        # Envía la pregunta al usuario y llena el slot "entidad"
        dispatcher.utter_message(pregunta)

        # Llena el slot "entidad" con el valor correspondiente
        return [SlotSet("entidad", entidad)]
