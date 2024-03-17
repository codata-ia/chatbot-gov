from openai import OpenAI

class ia:
       
    historico = []
    
    def __init__(self, openai_key, contexto, model='gpt-3.5-turbo', temperature = 0.75):        
        self.client = OpenAI(api_key= openai_key)
        self.historico.append( contexto )
        self.model = model
        self.temperature = temperature
       
                
    def responder(self, mensagem):
        
        self.historico.append({"role": "user", "content": mensagem })

        response = self.client.chat.completions.create(
            model= self.model,
            messages= self.historico,
            temperature = self.temperature,
            stream=True
        )

        self.historico.append({"role": "assistant", "content": "" })
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                self.historico[-1]["content"] = self.historico[-1]["content"] + chunk.choices[0].delta.content
                yield self.historico[-1]["content"]