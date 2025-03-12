# Visual Story Evaluation Tool

This tool evaluates how well a child's drawing matches a given story description. It's designed specifically for applications working with children with Autism Spectrum Disorder (ASD).

## How It Works

1. The system takes a child's drawing (image) and the original story description
2. It uses OpenAI's Vision model to analyze the drawing
3. It compares the drawing with the original description
4. It generates an evaluation report in JSON format with specific criteria

## Requirements

- Python 3.7+
- OpenAI API key

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Command Line Interface

Run the script from the command line:

```bash
python app.py
```

### Interactive UI for Kids

For a kid-friendly interface with an interactive drawing canvas:

```bash
streamlit run app_ui.py
```

The Streamlit interface provides:
- A selection of pre-defined stories to draw
- Ability to create and save custom stories for children to draw
- An interactive canvas with drawing tools
- Instant evaluation with colorful, kid-friendly feedback
- ASD-specific insights

#### Creating Custom Stories

The application allows educators, therapists, or parents to:
1. Create new stories by providing a title and description
2. Save them for future use
3. Delete stories that are no longer needed
4. Select from both standard and custom stories for drawing exercises

## Output

The evaluation includes:
- Whether the child understood the scenario
- If the object count is accurate and relevant
- If objects are positioned correctly
- Overall accuracy percentage
- ASD-related feedback

## Integration

You can also import the main function in your own Python code:

```python
from app import main

evaluation = main("path/to/drawing.jpg", "A short story description")
print(evaluation)
``` 