from ollama import chat, ChatResponse


class Agent_AI:
    def __init__(self,model='qwen3.5:0.8b',systemprompt="",available_functions={},tools=[],format=None):
        self.options={}
        self.model=model
        self.systemprompt=systemprompt
        self.messages=[]
        self.tools=tools
        self.format=format
        if systemprompt !="":
            self.messages.append({'role': 'system', 'content': systemprompt})
        self.available_functions=available_functions

    def add_messages(self,role="user",content=None,images=None):
        if content:
            item= {}
            item['role'] = role
            item['content']=content
            if images :
                item['images']=images
            self.messages.append(item)

    def query_stream(self,message="",temperature=0.1,top_p=0.1,top_k=20,min_p=0,presence_penalty=0,seed=42,think=True,parallel_tool_calls=True):
        
        if message !="":
            self.messages.append({'role': 'user', 'content': message})
       
        #Boucle d'itération de l'IA
        # tools_list = list(self.available_functions.values()) if self.available_functions else None
        while True:
            response: ChatResponse = chat(
                model=self.model,
                messages= self.messages,
                options= {
                        "temperature": temperature,
                        "top_p":top_p, 
                        "seed": seed,
                        'top_k':top_k,
                        'min_p':min_p,
                        'presence_penalty':presence_penalty},
                tools=self.tools,
                stream=True,
                think= think,
                format=self.format,
            )
            thinking = ''
            content = ''
            tool_calls = []

            done_thinking = False
            # accumulate the partial fields
            for chunk in response:
                if chunk.message.thinking:
                    thinking += chunk.message.thinking
                    print(chunk.message.thinking, end='', flush=True)
                if chunk.message.content:
                    if not done_thinking:
                        done_thinking = True
                        print('\n')
                    content += chunk.message.content
                    print(chunk.message.content, end='', flush=True)
                if chunk.message.tool_calls:
                    tool_calls.extend(chunk.message.tool_calls)
                    print(chunk.message.tool_calls)

            # append accumulated fields to the messages
            if thinking or content or tool_calls:
                self.messages.append({'role': 'assistant', 'thinking': thinking, 'content': content, 'tool_calls': tool_calls})

            if not tool_calls:
                break

            for tc in tool_calls:
                # if call.function.name == 'get_temperature':
                #     result = get_temperature(**call.function.arguments)

                if tc.function.name in self.available_functions:
                    print(f"Calling {tc.function.name} with arguments {tc.function.arguments}")
                    result = self.available_functions[tc.function.name](**tc.function.arguments)
                    args={'role': 'tool', 'tool_name': tc.function.name, 'content': str(result["text"])}
                    print(f"Result: \n")
                    print(result["text"])
                    if result.get("images",None):
                        args['images'] = result["images"]
                    self.messages.append(args)
                else:
                    self.messages.append({'role': 'tool', 'tool_name': tc.function.name, 'content': 'Unknown tool'})

        return content
        