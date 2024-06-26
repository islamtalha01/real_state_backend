

import json
import os
import time
from flask import Flask, request, jsonify,send_file
from flask_cors import CORS
import openai
from openai import OpenAI
import functions
from dotenv import load_dotenv
import base64
from packaging import version

# Check OpenAI version compatibility
load_dotenv()
app = Flask(__name__)
CORS(app) 
required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)
OPENAI_API_KEY = os.environ['OPENAI_API_KEY'].rstrip()


if current_version < required_version:
    raise ValueError(
        f"Error: OpenAI version {openai.__version__} is less than the required version 1.1.1"
    )
else:
    print("OpenAI version is compatible.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Create or load assistant
assistant_id = functions.create_assistant(client)

# Start conversation thread
@app.route('/start', methods=['GET'])
def start_conversation():
    # print("Starting a new conversation...")
    thread = client.beta.threads.create()
    # print(f"New thread created with ID: {thread.id}")

    # # Create the response object
    response = jsonify({"thread_id": thread.id})

    # Add CORS headers to the response
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')

    return response

    
@app.route('/')
def index():
    return 'Server running'






@app.route('/download_audio', methods=['GET'])
def download_audio():
    # Endpoint to download the generated audio file
    return send_file("output.mp3", mimetype='audio/mpeg', as_attachment=True, download_name='response.mp3')




@app.route('/chat', methods=['POST','GET'])
def chat():
    data = request.json
    thread_id = data.get('thread_id')
    voice_flag = data.get('voiceResponse')
    user_input = data.get('message', '')
    print("voice flag value is ", voice_flag)
    if not thread_id:
        print("Error: Missing thread_id")
        return jsonify({"error": "Missing thread_id"}), 400

    print(f"Received message: {user_input} for thread ID: {thread_id}")

    # Add the user's message to the thread
    client.beta.threads.messages.create(thread_id=thread_id,
                                        role="user",
                                        content=user_input)

    # Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread_id,
                                          assistant_id=assistant_id)

    # Check if the Run requires action (function call)
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id,
                                                       run_id=run.id)
        if run_status.status == 'completed':
            break
        elif run_status.status == 'requires_action':
            # Handle the function call
            for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                if tool_call.function.name == "get_property_value_estimate":
                    # Process property value estimation
                    arguments = json.loads(tool_call.function.arguments)
                    output = functions.get_property_value_estimate(arguments["address"], arguments["features"])
                    client.beta.threads.runs.submit_tool_outputs(thread_id=thread_id,
                                                                 run_id=run.id,
                                                                 tool_outputs=[{
                                                                     "tool_call_id": tool_call.id,
                                                                     "output": json.dumps(output)
                                                                 }])
            time.sleep(1)  # Wait for a second before checking again

    # Retrieve and return the latest message from the assistant
    messages = client.beta.threads.messages.list(thread_id=thread_id)
   
    response_text = messages.data[0].content[0].text.value
    print("result",response_text)

    # Add CORS headers to the response
   


    response = jsonify({'text': response_text})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    
    if voice_flag:
        return response
    else:
        print("in else")
        audio_response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=response_text
        )
    # Save the audio file
        audio_file_path = "test.mp3"
        audio_response.stream_to_file(audio_file_path)
        with open(audio_file_path, "rb") as audio_file:
         audio_base64 = base64.b64encode(audio_file.read()).decode('utf-8')
    
        response = {
            'text': response_text,
            'audio': audio_base64
        }
        print("data",response)
        return jsonify(response)





if __name__ == '__main__':
     app.run(host='0.0.0.0', port=int(os.getenv("PORT", 3001)))
