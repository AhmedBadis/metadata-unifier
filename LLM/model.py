import chainlit as cl
from chainlit import user_session
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import List, Dict, Tuple
from huggingface_hub import login

model_loaded: bool = False  # global variable to load model only once
pipe: pipeline = 0  # global Variable for the Model Pipeline

def load_model():
    """
    Load the LLM Model, Qwen/Qwen2.5-1.5B-Instruct, the fine-tuned English speaking model from Qwen. Significant improvements in instruction following,      generating long texts (over 8K tokens), understanding structured data (e.g, tables), and generating structured outputs especially JSON.

    Returns
    -------
    pipe : a TextGenerationPipeline, which can be used on HuggingFace Models for inference
    """
    login("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")
    model_id: str = "Qwen/Qwen2.5-1.5B-Instruct"

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="cuda"  # Use "cuda" to run on GPU / "auto" to allocate resources dynamically
    )

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    pipe = pipeline(
        model=model,
        tokenizer=tokenizer,
        task="text-generation",
        temperature=0.1,
        max_new_tokens=512,
        repetition_penalty=1.1
    )

    return pipe

def format_model_response(model_output: List[Dict], query: str) -> str:
    """
    Extracts the generated response from the model output and removes the prompt.

    Parameters
    ----------
    model_output : List[Dict] : the raw output of the Model
    query : str : the input query to the Model

    Returns
    -------
    response : str : formatted response from the Model
    """
    generated_text = model_output[0]['generated_text']
    response = generated_text[len(query):].strip()  # Remove the prompt from the output

    return response

def create_new_prompt(model_output: List[Dict], new_message: str) -> str:
    """
    Creates a new formatted message for the model including the conversation history.

    Parameters
    ----------
    model_output : List[Dict] : the output of the Model
    new_message : str : the new message for the Model

    Returns
    -------
    new_query_formatted : str : the new correctly formatted message for the Model
    """
    if not model_output or len(model_output) == 0:
        return f"[INST] {new_message} [/INST]"  # Return the new message if there's no previous output

    generated_text = model_output[0]['generated_text']  # Extract from list and dictionary

    new_query_formatted = generated_text + f"</s><s> [INST] {new_message} [/INST]"

    return new_query_formatted

def send_query_to_model(query: str) -> Tuple[List[Dict], str]:
    try:
        model_output: List[Dict] = pipe(
            query,
            min_length=2,     # Minimum length
            temperature=0.7,  # Lower temperature
            top_p=0.85,       # Response diversity
            do_sample=True
        )

        if not model_output or len(model_output) == 0:
            return [], "No response from the model."

        response: str = format_model_response(model_output, query)
        return model_output, response

    except Exception as e:
        return [], f"An error occurred: {str(e)}"

# Chainlit code
@cl.on_chat_start
async def start():
    """
    This method runs when a WebSocket connection event occurs, meaning a user connects to the website.
    It sends an initial message "Starting the bot..." to the user and takes care of all necessary tasks, such as loading the model and
    initializing the user session variables.
    """
    starting_message: str = "Starting the chatbot..."
    welcome_message: str = "Hi there! What can I do for you?"
    SYSTEM_PROMPT: str = """<s>[INST] <<SYS>>
You are a Chatbot on a Website. Your primary objective is to transform and analyze data given by the user to the required format. Do not make any emotes. Keep the conversation friendly and professional. Do not make any gestures. Do not write emojis. Avoid emojis Only reply with words. No roleplaying actions.
<</SYS>>"""

    msg = cl.Message(content=starting_message)
    await msg.send()

    global pipe
    global model_loaded

    # Load the Model, if it is not already loaded
    if not model_loaded:
        pipe = load_model()
        model_loaded = True

    if model_loaded:
        user_session.set("first_message", True)  # first_message: bool, that defines whether it is the first Message to the Model.
        user_session.set("model_output", 0)  # model_output: variable to save the whole interaction with the model
        user_session.set("query", 0)  # query: variable

        msg.content = welcome_message
        await msg.update()

@cl.on_message
async def main(message: cl.Message):
    """
    This method runs when the User sends a Message.
    It gets the User's message and formats it and the previous conversation so that it can be sent to the Model.
    Then it sends the message (query) to the Model.
    The response of the model will be stored as a user_session variable, so that the model can be given the entire conversation for the next message.
    The relevant response for the user is extracted and sent to them.

    Parameters
    ----------
    message: cl.Message, that contains all necessary information about the message (content, author, ...)
    """
    global pipe

    SYSTEM_PROMPT: str = """<s>[INST] <<SYS>>
You are a Chatbot on a Website. Your primary objective is to transform and analyze data given by the user to the required format. Do not make any emotes. Keep the conversation friendly and professional. Do not make any gestures. Do not write emojis. Avoid emojis Only reply with words. No roleplaying actions.
<</SYS>>"""

    query = user_session.get("query")
    model_output = user_session.get("model_output")

    user_message: str = message.content

    # Format the input to be sent to the Model
    if user_session.get("first_message") is True:
        query = SYSTEM_PROMPT + f"\n{user_message} [/INST]"
        user_session.set("first_message", False)
    else:
        query = create_new_prompt(model_output, user_message)

    model_output, response = send_query_to_model(query)
    response = response.replace('[/INST]', '').strip()  # Remove any trailing [/INST]
    response = response.replace('[INST]', '').strip()  # Remove any trailing [INST]
    response = response.replace('<s>', '').strip()  # Remove any trailing [/INST]

    user_session.set("query", query)
    user_session.set("model_output", model_output)

    # Send the Model's response to the User
    await cl.Message(
        content=f"{response}",
    ).send()