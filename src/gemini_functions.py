import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ServiceUnavailable, ResourceExhausted, NotFound

load_dotenv()

class GeminiChat:
    def __init__(self):
        genai.configure(api_key=os.getenv("AIzaSyBf2Pqw9deB0PKT4vWPsglbrXx-9O10Dd8"))
        
        # Lista de modelos disponíveis (com fallback)
        self.model_names = [             # Versão anterior
            'gemini-2.0-flash'          # Versão mais estável
        ]
        
        self.model = None
        self.chat = None
        self.max_retries = 3
        self.retry_delay = 5
        
        # Tenta inicializar com o primeiro modelo disponível
        self._initialize_model()
    
    def _initialize_model(self):
        """Tenta inicializar com o primeiro modelo disponível"""
        for model_name in self.model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                self.chat = self.model.start_chat(history=[])
                print(f"Modelo inicializado com sucesso: {model_name}")
                return
            except NotFound:
                print(f"Modelo não encontrado: {model_name}")
                continue
        
        raise RuntimeError("Nenhum dos modelos Gemini está disponível")
    
    def send_message(self, message):
        """Envia mensagem com mecanismo de retry automático"""
        if not self.model or not self.chat:
            self._initialize_model()
            
        for attempt in range(self.max_retries):
            try:
                response = self.chat.send_message(message, stream=True)
                return "".join([chunk.text for chunk in response])
            
            except NotFound as e:
                # Se o modelo atual não for encontrado, tenta o próximo
                self._initialize_model()
                if attempt == self.max_retries - 1:
                    return f"⚠️ Modelo não disponível. Por favor, tente novamente mais tarde. (Erro: {str(e)})"
            
            except (ServiceUnavailable, ResourceExhausted) as e:
                if attempt == self.max_retries - 1:
                    return f"⚠️ Serviço indisponível. Por favor, tente novamente mais tarde. (Erro: {str(e)})"
                time.sleep(self.retry_delay * (attempt + 1))
            
            except Exception as e:
                return f"⛔ Erro inesperado: {str(e)}"
    
    def clear_history(self):
        if self.model:
            self.chat = self.model.start_chat(history=[])