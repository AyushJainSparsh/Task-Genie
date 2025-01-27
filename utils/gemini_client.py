import os # to use operating system resources
import google.generativeai as genai # to generate ai
from dotenv import load_dotenv # to create a local environment

load_dotenv()

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Utility function to get a Gemini model with dynamic configuration
def get_gemini_model(config=generation_config):
    """
    Returns a Gemini model instance with the specified configuration.
    
    Args:
        config (dict): The generation configuration for the Gemini model.

    Returns:
        GenerativeModel: An initialized Gemini GenerativeModel.
    """
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Initialize the model with dynamic configuration
    return genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=config
    )
