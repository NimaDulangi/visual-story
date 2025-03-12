import json
import base64
from typing import Dict, Any, Optional
import requests
from jsonschema import validate, ValidationError
import streamlit as st


# Get API key from environment variables
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# Define the JSON schema for the evaluation output
EVALUATION_SCHEMA = {
    "type": "object",
    "properties": {
        "Can the child understand the scenario?": {"type": "string"},
        "Is the object count accurate and relevant?": {"type": "string"},
        "Can the object be positioned correctly?": {"type": "string"},
        "How far is it accurate?": {"type": "string"},
        "ASD-related feedback": {"type": "string"}
    },
    "required": [
        "Can the child understand the scenario?",
        "Is the object count accurate and relevant?",
        "Can the object be positioned correctly?",
        "How far is it accurate?",
        "ASD-related feedback"
    ],
    "additionalProperties": False
}

def encode_image_to_base64(image_path: str) -> str:
    """
    Encode an image file to base64 string
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string of the image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_drawing(image_path: str, story_description: str) -> Dict[str, Any]:
    """
    Analyze a child's drawing using OpenAI's Vision model
    
    Args:
        image_path: Path to the drawing image
        story_description: Original story description given to the child
        
    Returns:
        JSON response from the OpenAI API
    """
    # Encode the image
    base64_image = encode_image_to_base64(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Analyze this child's drawing. The child was given the following story description:
                        
                        '{story_description}'
                        
                        Please analyze how well the drawing matches the description. Focus on:
                        1. Whether the child understood the scenario
                        2. If the object count is accurate and relevant
                        3. If objects are positioned correctly
                        4. Overall accuracy percentage
                        
                        Provide a detailed analysis of the drawing in relation to the story."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

def evaluate_drawing(analysis_response: Dict[str, Any], story_description: str) -> Dict[str, str]:
    """
    Generate an evaluation report based on the analysis
    
    Args:
        analysis_response: Response from the OpenAI Vision API
        story_description: Original story description
        
    Returns:
        Evaluation report in the required JSON format
    """
    # Check if 'choices' is in the response
    if "choices" not in analysis_response:
        raise ValueError("The API response does not contain 'choices'. Response: " + json.dumps(analysis_response, indent=2))

    # Extract the analysis text from the response
    analysis_text = analysis_response["choices"][0]["message"]["content"]
    
    # Use GPT to generate the evaluation in the required format
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert in evaluating children's drawings, especially for kids with ASD (Autism Spectrum Disorder)."
            },
            {
                "role": "user",
                "content": f"""Based on the following analysis of a child's drawing and the original story description, 
                generate an evaluation report in JSON format with these exact keys:
                
                1. "Can the child understand the scenario?"
                2. "Is the object count accurate and relevant?"
                3. "Can the object be positioned correctly?"
                4. "How far is it accurate?"
                5. "ASD-related feedback"
                
                Original story description: '{story_description}'
                
                Analysis of the drawing: '{analysis_text}'
                
                Provide detailed but concise answers for each question. For the accuracy, include a percentage estimate.
                For ASD-related feedback, provide insights or observations related to ASD.
                Return ONLY the JSON object with no additional text."""
            }
        ],
        "response_format": {"type": "json_object"}
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    evaluation_text = response.json()["choices"][0]["message"]["content"]
    
    # Parse the JSON response
    evaluation = json.loads(evaluation_text)
    
    # Validate the evaluation against the schema
    try:
        validate(instance=evaluation, schema=EVALUATION_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"Invalid evaluation format: {e.message}")
    
    return evaluation

def main(image_path: str, story_description: str) -> Dict[str, str]:
    """
    Main function to evaluate a child's drawing
    
    Args:
        image_path: Path to the drawing image
        story_description: Original story description given to the child
        
    Returns:
        Evaluation report in JSON format
    """
    # Analyze the drawing
    analysis = analyze_drawing(image_path, story_description)
    
    # Generate evaluation report
    evaluation = evaluate_drawing(analysis, story_description)
    
    # Print and return the evaluation
    print(json.dumps(evaluation, indent=2))
    return evaluation

if __name__ == "__main__":
    # Example usage
    image_path = "images/visual story.jpeg"
    story_description = "small description goes here"
    main(image_path, story_description)
