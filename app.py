from flask import Flask, request, jsonify
from main import chatbot
from flask import Flask, jsonify, request, session, redirect
from flask_cors import CORS

import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
CORS(app)
app = Flask(__name__)

# Replace with your GPT-4 API function
# def get_response_openai(prompt):
#     # Implement your function to call GPT-4 API and return the response
#     # Example implementation:
#     # response = some_function_to_call_gpt4_api(prompt)
#     response = "This is a placeholder response"
#     return response
import os
import openai
from dotenv import load_dotenv
import json
from tools import tools
from function.dalle_executor import generate_image
from function.linkedin_executor import make_post_linkedin
from function.twitter_executor import make_post_twitter
from interface.terminal import pretty_print_conversation
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

def chatbot(message:str):
  # Create a list to store all the messages for context
    messages = [
    {"role": "system", "content": os.getenv("LLM_INSTRUCTIONS")},
  ]

#   # Keep repeating the following
#   while True:
#     # Prompt user for input
#     message = input("User: ")
#     print("\n")

#     # Exit program if user inputs "quit"
#     if message.lower() == "quit":
#       break

    # Add each new message to the list
    messages.append({"role": "user", "content": message})
    # pretty_print_conversation(messages=messages, message=None)

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
        # only one function in this example, but you can have multiple
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            pretty_print_conversation(messages=None, message=f"Calling {function_name}")
            function_response = execute_function(function_name, tool_call)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )  # extend conversation with function response
            second_response = client.chat.completions.create(
                model="gpt-4-0613",
                messages=messages,
            )
            final_response = second_response.choices[0].message.content
            # get a new response from the model where it can see the function response
        chat_message = final_response
        # print(f"Bot: {chat_message}")
        messages.append({"role": "assistant", "content": chat_message})
        pretty_print_conversation(messages=messages, message=None)
        return messages
    else:
        chat_message = response_message.content
        # print(f"Bot: {chat_message}")
        messages.append({"role": "assistant", "content": chat_message})
        pretty_print_conversation(messages=messages, message=None)
        return messages
# if __name__ == "__main__":
#   pretty_print_conversation(messages=None, message="Start chatting with Baani. You can ask Baani to create content and image for Linkedin. \nBaani has the ability to post on your behalf as well( after you approval)  (type 'quit' to stop)!")
#   chatbot()
@app.route('/generate', methods=['POST'])
def generate_response():
    if request.method=='POST':
        try:
            # Get the prompt from the POST request
            data = request.json
            print(data)

            # app.logger.info(f"{data}")
            # print(data)
            prompt = data.get('prompt')
            print(type(prompt))
            if not prompt:
                return jsonify({'error': 'Missing prompt parameter'}), 400

            # Call your GPT-4 API function to get the response
            response = chatbot(prompt)

            if response:
                return jsonify({'response': response}), 200
            else:
                return jsonify({'error': 'Failed to generate response'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
