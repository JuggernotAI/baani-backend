import os
import openai
from dotenv import load_dotenv
import json
from tools import tools
from function.dalle_executor import generate_image
from function.linkedin_executor import make_post_linkedin
from function.twitter_executor import make_post_twitter
from interface.terminal import pretty_print_conversation
from instructions.system_instructions import LLM_INSTRUCTIONS
# from messages_demo import messages

load_dotenv()
client=openai

def add_numbers(num1, num2):
   return num1+num2

def execute_function(function_name, tool_call):
    available_functions = {
        "add_numbers": add_numbers,
        "generate_image": generate_image,
        "make_post_linkedin": make_post_linkedin,
        "make_post_twitter": make_post_twitter
    }
    if function_name: 
        if function_name=="add_numbers":
                        function_to_call = available_functions[function_name]
                        function_args = json.loads(tool_call.function.arguments)
                        function_response = function_to_call(
                            num1=function_args.get("num1"),
                            num2=function_args.get("num2"),
                        )
        if function_name=="generate_image":
                        function_to_call = available_functions[function_name]
                        function_args = json.loads(tool_call.function.arguments)
                        function_response = function_to_call(
                            prompt=function_args.get("prompt"),
                        )
                        pretty_print_conversation(messages=None, message=function_args.get("prompt"))
                        # print(f"Function Response: {function_response}")
        if function_name=="make_post_linkedin":
                        function_to_call = available_functions[function_name]
                        function_args = json.loads(tool_call.function.arguments)
                        function_response = function_to_call(
                            text=function_args.get("linkedin_post"),
                        )
                        pretty_print_conversation(messages=None, message=function_args.get("linkedin_post"))
        if function_name=="make_post_twitter":
                        function_to_call = available_functions[function_name]
                        function_args = json.loads(tool_call.function.arguments)
                        function_response = function_to_call(
                            text=function_args.get("twitter_post"),
                        )
                        pretty_print_conversation(messages=None, message=function_args.get("twitter_post"))
        return function_response
    else:
        return f"function {function_name} not available for calling"
def init_chat():
    #   Create a list to store all the messages for context
    messages = [
    {"role": "system", "content": LLM_INSTRUCTIONS},
  ]
    return messages
def chatbot(messages):

    # message = prompt
    # Add each new message to the list
    # messages.append({"role": "user", "content": message})
    pretty_print_conversation(messages=messages, message=None)

    # Request gpt-3.5-turbo for chat completion
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=messages,
    tools=tools,
    tool_choice="auto"
    )

    # Print the response and add it to the messages list
    # print(response)
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # # Step 2: check if the model wanted to call a function
    if tool_calls:
        tool_messages = messages.copy()
        # Initialise another array for tool content
        tool_messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            pretty_print_conversation(messages=None, message=f"Calling {function_name}")
            function_response = execute_function(function_name, tool_call)
            tool_messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )  # extend conversation with function response
            second_response = client.chat.completions.create(
                model="gpt-4-0613",
                messages=tool_messages,
            )
            final_response = second_response.choices[0].message.content
            # get a new response from the model where it can see the function response
        chat_message = final_response
        # print(chat_message)
        # print(f"Bot: {chat_message}")
        messages.append({"role": "assistant", "content": chat_message})
        pretty_print_conversation(messages=messages, message=None)
        print("Message in main.py: ", messages)
        return messages
        
    else:
        chat_message = response_message.content
        # print(f"Bot: {chat_message}")
        messages.append({"role": "assistant", "content": chat_message})
        # print(messages)
        pretty_print_conversation(messages=messages, message=None)
        return messages

# if __name__ == "__main__":
    messages.get("response")
#   pretty_print_conversation(messages=None, message="Start chatting with Baani. You can ask Baani to create content and image for Linkedin. \nBaani has the ability to post on your behalf as well( after you approval)  (type 'quit' to stop)!")
#   chatbot()