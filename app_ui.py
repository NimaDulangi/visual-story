import streamlit as st
import json
import os
import base64
from PIL import Image
from io import BytesIO
from streamlit_drawable_canvas import st_canvas
from app import main

# Initialize session state for custom stories if it doesn't exist
if 'custom_stories' not in st.session_state:
    st.session_state.custom_stories = {}

# Set page configuration
st.set_page_config(
    page_title="Visual Story Drawing Tool",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a more kid-friendly interface
st.markdown("""
<style>
    .main {
        background-color: #f0f8ff;
    }
    .stApp {
        background-image: linear-gradient(to bottom right, #f0f8ff, #e6f7ff);
    }
    h1, h2, h3 {
        color: #2e86c1;
    }
    .story-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #85c1e9;
        margin-bottom: 20px;
    }
    .canvas-container {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #85c1e9;
    }
    .stButton button {
        background-color: #2ecc71;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
    }
    .stButton button:hover {
        background-color: #27ae60;
    }
    .result-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #85c1e9;
        margin-top: 20px;
    }
    .custom-story-form {
        background-color: #e8f8f5;
        padding: 15px;
        border-radius: 10px;
        border: 2px dashed #16a085;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# App title with emoji
st.title("🎨 Visual Story Drawing Adventure! 🖌️")

# Sidebar for story selection and creation
with st.sidebar:
    st.image("https://img.freepik.com/free-vector/children-drawing-with-crayons_1308-93156.jpg", width=300)
    
    # Story creation section
    st.markdown("<div class='custom-story-form'>", unsafe_allow_html=True)
    st.header("✏️ Create a New Story")
    
    new_story_title = st.text_input("Story Title", placeholder="Enter a title for your story")
    new_story_text = st.text_area("Story Description", 
                                  placeholder="Write a short, descriptive story for the child to draw...",
                                  height=150)
    
    if st.button("✨ Save New Story ✨"):
        if new_story_title and new_story_text:
            st.session_state.custom_stories[new_story_title] = new_story_text
            st.success(f"Story '{new_story_title}' saved successfully!")
        else:
            st.warning("Please enter both a title and description for your story.")
    
    # Delete a custom story
    if st.session_state.custom_stories:
        story_to_delete = st.selectbox("Delete a custom story", 
                                      ["None"] + list(st.session_state.custom_stories.keys()),
                                      index=0)
        if story_to_delete != "None" and st.button("🗑️ Delete Story"):
            del st.session_state.custom_stories[story_to_delete]
            st.success(f"Story '{story_to_delete}' deleted successfully!")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Story selection section
    st.header("🌟 Choose a Story 📚")
    
    # Sample standard stories for kids
    standard_stories = {
        "Mountains and Trees": "One day, there were two tall mountains standing side by side. The sun was shining brightly in the sky, spreading its warm light over everything. Three birds were flying high near the sun, enjoying the fresh air. At the bottom of the mountains, there were two big trees with lots of leaves. The trees stood tall, giving shade and making the place look peaceful.",
        
        "Ocean Adventure": "Imagine a blue ocean with gentle waves. On the surface, a small red boat is floating. There's a happy dolphin jumping out of the water next to the boat. Above, three seagulls are flying in the sky. The bright sun is shining down on everything, making the water sparkle.",
        
        "Playground Fun": "Draw a playground with a tall slide in the center. On the left side, there's a swing set with two swings. On the right side, there's a sandbox. Two children are playing - one on the slide and one on a swing. A big tree provides shade over part of the playground."
    }
    
    # Combine standard and custom stories
    all_stories = {}
    
    # Add standard stories with a label
    for title, text in standard_stories.items():
        all_stories[f"📚 {title}"] = text
    
    # Add custom stories with a label if any exist
    if st.session_state.custom_stories:
        for title, text in st.session_state.custom_stories.items():
            all_stories[f"✏️ {title}"] = text
    
    story_choice = st.radio("Select a story to draw", list(all_stories.keys()))
    selected_story = all_stories[story_choice]
    
    st.subheader("✨ Drawing Tools ✨")
    
    # Drawing tools
    stroke_width = st.slider("Brush Size:", 1, 25, 5)
    stroke_color = st.color_picker("Stroke Color:", "#FF5733")
    bg_color = "#FFFFFF"  # White background

# Main content area split into two columns
col1, col2 = st.columns([1, 1])

with col1:
    # Story description in a colorful card
    st.markdown(f"""
    <div class="story-card">
        <h2>📖 Your Story to Draw:</h2>
        <p style="font-size: 18px; color: #333333;">{selected_story}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #ffeaa7; padding: 15px; border-radius: 10px; border: 2px dashed #fdcb6e;">
        <h3 style="color: #e17055;">🎯 Your Mission:</h3>
        <p style="font-size: 16px;">Draw what you see in the story! Try to include all the details mentioned.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Canvas for drawing
    st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=400,
        width=600,
        drawing_mode="freedraw",
        key="canvas",
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Button to evaluate drawing
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    evaluate_button = st.button("✨ Evaluate My Drawing! ✨")

# Results section
if evaluate_button and canvas_result.image_data is not None:
    st.markdown("<h2 style='text-align: center; color: #3498db;'>🌈 Your Drawing Results 🌈</h2>", unsafe_allow_html=True)
    
    # Save the image to a temporary file
    img_data = canvas_result.image_data
    img = Image.fromarray(img_data.astype('uint8'), 'RGBA')
    img_path = "temp_drawing.png"
    img.save(img_path)
    
    with st.spinner("Our art experts are reviewing your masterpiece..."):
        try:
            # Call the main function from app.py to evaluate the drawing
            evaluation = main(img_path, selected_story)
            
            # Display the evaluation results in a colorful format
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            
            # Display each evaluation point with colorful formatting
            st.markdown(f"<h3 style='color: #3498db;'>🧠 Understanding the Story</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 16px;'>{evaluation['Can the child understand the scenario?']}</p>", unsafe_allow_html=True)
            
            st.markdown(f"<h3 style='color: #e74c3c;'>🔢 Object Count</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 16px;'>{evaluation['Is the object count accurate and relevant?']}</p>", unsafe_allow_html=True)
            
            st.markdown(f"<h3 style='color: #2ecc71;'>🧩 Object Positioning</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 16px;'>{evaluation['Can the object be positioned correctly?']}</p>", unsafe_allow_html=True)
            
            st.markdown(f"<h3 style='color: #f39c12;'>🎯 Overall Accuracy</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 16px;'>{evaluation['How far is it accurate?']}</p>", unsafe_allow_html=True)
            
            st.markdown(f"<h3 style='color: #9b59b6;'>💫 Special Feedback</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 16px;'>{evaluation['ASD-related feedback']}</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Celebrate with confetti if the accuracy is high
            if "90%" in evaluation['How far is it accurate?'] or "80%" in evaluation['How far is it accurate?']:
                st.balloons()
            
        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)}")
            st.info("Make sure your drawing is clear and you've included elements from the story.")
            
    # Remove the temporary file
    if os.path.exists(img_path):
        os.remove(img_path)

# Footer section
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 10px; background-color: #d1f2eb; border-radius: 10px;">
    <p style="font-size: 14px; color: #16a085;">Made with ❤️ for kids with ASD</p>
</div>
""", unsafe_allow_html=True) 