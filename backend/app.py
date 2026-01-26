from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import base64
import cv2
import numpy as np
from datetime import datetime
import random
import json

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Zodiac database
ZODIAC_DATA = {
    "aries": {
        "icon": "♈",
        "name": "Aries",
        "dates": "March 21 - April 19",
        "element": "Fire",
        "planet": "Mars",
        "traits": ["Energetic", "Courageous", "Confident", "Enthusiastic", "Optimistic", "Honest"],
        "description": "Based on the analysis of your hand shape and lines, you exhibit strong Aries qualities. Your hand shows dynamic energy patterns with strong heart lines indicating passion and leadership potential.",
        "recommendations": [
            {"icon": "fas fa-dumbbell", "title": "Physical Activity", "desc": "Channel your energy into sports or fitness routines"},
            {"icon": "fas fa-flag", "title": "New Challenges", "desc": "Take on leadership roles in projects"},
            {"icon": "fas fa-heart", "title": "Relationships", "desc": "Practice patience in personal relationships"},
            {"icon": "fas fa-bolt", "title": "Energy Management", "desc": "Find outlets for your abundant energy"}
        ],
        "colors": ["Red", "White"],
        "lucky_numbers": [1, 9],
        "compatibility": ["Leo", "Sagittarius", "Gemini"]
    },
    "taurus": {
        "icon": "♉",
        "name": "Taurus",
        "dates": "April 20 - May 20",
        "element": "Earth",
        "planet": "Venus",
        "traits": ["Reliable", "Patient", "Practical", "Devoted", "Responsible", "Stable"],
        "description": "Your hand analysis reveals Taurus characteristics. The strong, straight lines indicate determination and practicality, while the palm shape suggests a love for comfort and beauty.",
        "recommendations": [
            {"icon": "fas fa-tree", "title": "Nature Time", "desc": "Spend time in natural environments to recharge"},
            {"icon": "fas fa-utensils", "title": "Culinary Arts", "desc": "Explore cooking or gourmet tasting experiences"},
            {"icon": "fas fa-music", "title": "Music Therapy", "desc": "Listen to calming or classical music"},
            {"icon": "fas fa-hands", "title": "Tactile Activities", "desc": "Engage in gardening or pottery"}
        ],
        "colors": ["Green", "Pink"],
        "lucky_numbers": [2, 6],
        "compatibility": ["Virgo", "Capricorn", "Cancer"]
    },
    "gemini": {
        "icon": "♊",
        "name": "Gemini",
        "dates": "May 21 - June 20",
        "element": "Air",
        "planet": "Mercury",
        "traits": ["Versatile", "Expressive", "Curious", "Kind", "Adaptable", "Quick-witted"],
        "description": "Your hand shows Gemini traits with multiple branching lines indicating versatility and intellectual curiosity. The finger length suggests excellent communication skills.",
        "recommendations": [
            {"icon": "fas fa-book", "title": "Learning", "desc": "Take up a new course or language"},
            {"icon": "fas fa-comments", "title": "Social Connection", "desc": "Join discussion groups or podcasts"},
            {"icon": "fas fa-pen", "title": "Writing", "desc": "Start a blog or journal"},
            {"icon": "fas fa-plane", "title": "Short Trips", "desc": "Plan weekend getaways to new places"}
        ],
        "colors": ["Yellow", "Light Blue"],
        "lucky_numbers": [5, 7],
        "compatibility": ["Libra", "Aquarius", "Leo"]
    },
    "cancer": {
        "icon": "♋",
        "name": "Cancer",
        "dates": "June 21 - July 22",
        "element": "Water",
        "planet": "Moon",
        "traits": ["Intuitive", "Emotional", "Protective", "Loyal", "Sympathetic", "Nurturing"],
        "description": "The analysis reveals Cancer's emotional depth. Your hand shows sensitive patterns with a prominent heart line indicating strong emotional intelligence and nurturing qualities.",
        "recommendations": [
            {"icon": "fas fa-home", "title": "Home Projects", "desc": "Create a comfortable living space"},
            {"icon": "fas fa-heart", "title": "Family Time", "desc": "Plan regular family gatherings"},
            {"icon": "fas fa-water", "title": "Water Activities", "desc": "Try swimming or beach walks"},
            {"icon": "fas fa-moon", "title": "Self-Care", "desc": "Practice meditation and self-reflection"}
        ],
        "colors": ["Silver", "White"],
        "lucky_numbers": [2, 7],
        "compatibility": ["Scorpio", "Pisces", "Taurus"]
    },
    "leo": {
        "icon": "♌",
        "name": "Leo",
        "dates": "July 23 - August 22",
        "element": "Fire",
        "planet": "Sun",
        "traits": ["Creative", "Passionate", "Generous", "Cheerful", "Warm-hearted", "Charismatic"],
        "description": "Your hand exhibits Leo's radiant energy. The prominent life line and strong fingers indicate vitality, leadership, and a natural flair for creativity and performance.",
        "recommendations": [
            {"icon": "fas fa-crown", "title": "Leadership", "desc": "Take charge of creative projects"},
            {"icon": "fas fa-theater-masks", "title": "Performing Arts", "desc": "Try acting, singing, or dancing"},
            {"icon": "fas fa-sun", "title": "Sun Exposure", "desc": "Spend time in sunlight responsibly"},
            {"icon": "fas fa-gift", "title": "Generosity", "desc": "Volunteer or mentor others"}
        ],
        "colors": ["Gold", "Orange"],
        "lucky_numbers": [1, 4],
        "compatibility": ["Aries", "Sagittarius", "Gemini"]
    },
    "virgo": {
        "icon": "♍",
        "name": "Virgo",
        "dates": "August 23 - September 22",
        "element": "Earth",
        "planet": "Mercury",
        "traits": ["Analytical", "Practical", "Precise", "Kind", "Hardworking", "Modest"],
        "description": "The analysis shows Virgo's attention to detail. Your hand reveals precise line patterns and well-defined mounts indicating analytical thinking and practical problem-solving skills.",
        "recommendations": [
            {"icon": "fas fa-clipboard-check", "title": "Organization", "desc": "Create detailed plans and systems"},
            {"icon": "fas fa-seedling", "title": "Gardening", "desc": "Start an herb or vegetable garden"},
            {"icon": "fas fa-book-medical", "title": "Health Focus", "desc": "Develop a wellness routine"},
            {"icon": "fas fa-puzzle-piece", "title": "Problem Solving", "desc": "Engage in puzzles or strategy games"}
        ],
        "colors": ["Green", "Brown"],
        "lucky_numbers": [5, 14],
        "compatibility": ["Taurus", "Capricorn", "Cancer"]
    },
    "libra": {
        "icon": "♎",
        "name": "Libra",
        "dates": "September 23 - October 22",
        "element": "Air",
        "planet": "Venus",
        "traits": ["Diplomatic", "Graceful", "Social", "Idealistic", "Cooperative", "Romantic"],
        "description": "Your hand shows balanced Libra characteristics. The symmetrical lines and elegant finger shapes indicate a natural sense of harmony, justice, and aesthetic appreciation.",
        "recommendations": [
            {"icon": "fas fa-balance-scale", "title": "Balance Activities", "desc": "Try yoga or meditation"},
            {"icon": "fas fa-users", "title": "Social Engagement", "desc": "Host gatherings or join social clubs"},
            {"icon": "fas fa-palette", "title": "Art Appreciation", "desc": "Visit galleries or engage in artistic pursuits"},
            {"icon": "fas fa-heart", "title": "Relationship Focus", "desc": "Nurture partnerships and seek harmony"}
        ],
        "colors": ["Pink", "Blue"],
        "lucky_numbers": [6, 15],
        "compatibility": ["Gemini", "Aquarius", "Sagittarius"]
    },
    "scorpio": {
        "icon": "♏",
        "name": "Scorpio",
        "dates": "October 23 - November 21",
        "element": "Water",
        "planet": "Pluto",
        "traits": ["Passionate", "Resourceful", "Brave", "Determined", "Intense", "Loyal"],
        "description": "Your hand reveals Scorpio's depth and intensity. The deep, pronounced lines indicate strong willpower, emotional depth, and transformative potential.",
        "recommendations": [
            {"icon": "fas fa-search", "title": "Research Projects", "desc": "Channel intensity into investigative work"},
            {"icon": "fas fa-water", "title": "Water Activities", "desc": "Swimming or beach walks for emotional balance"},
            {"icon": "fas fa-moon", "title": "Introspection", "desc": "Journaling or meditation for self-discovery"},
            {"icon": "fas fa-lock", "title": "Privacy Boundaries", "desc": "Create personal spaces for rejuvenation"}
        ],
        "colors": ["Black", "Red"],
        "lucky_numbers": [8, 11],
        "compatibility": ["Cancer", "Pisces", "Virgo"]
    },
    "sagittarius": {
        "icon": "♐",
        "name": "Sagittarius",
        "dates": "November 22 - December 21",
        "element": "Fire",
        "planet": "Jupiter",
        "traits": ["Adventurous", "Optimistic", "Honest", "Philosophical", "Independent", "Fun-loving"],
        "description": "Your hand shows Sagittarius' adventurous spirit. The long lines and expansive palm indicate a love for freedom, exploration, and philosophical thinking.",
        "recommendations": [
            {"icon": "fas fa-hiking", "title": "Adventure", "desc": "Plan outdoor adventures or travel"},
            {"icon": "fas fa-graduation-cap", "title": "Higher Learning", "desc": "Take advanced courses or workshops"},
            {"icon": "fas fa-globe", "title": "Cultural Exploration", "desc": "Learn about different cultures"},
            {"icon": "fas fa-horse", "title": "Animal Connection", "desc": "Spend time with animals or horseback riding"}
        ],
        "colors": ["Purple", "Blue"],
        "lucky_numbers": [3, 12],
        "compatibility": ["Aries", "Leo", "Aquarius"]
    },
    "capricorn": {
        "icon": "♑",
        "name": "Capricorn",
        "dates": "December 22 - January 19",
        "element": "Earth",
        "planet": "Saturn",
        "traits": ["Ambitious", "Disciplined", "Patient", "Responsible", "Practical", "Wise"],
        "description": "Your hand reveals Capricorn's disciplined nature. The strong bone structure and defined lines indicate ambition, perseverance, and practical wisdom.",
        "recommendations": [
            {"icon": "fas fa-mountain", "title": "Goal Setting", "desc": "Climb literal or metaphorical mountains"},
            {"icon": "fas fa-chart-line", "title": "Career Development", "desc": "Focus on long-term career goals"},
            {"icon": "fas fa-history", "title": "Tradition", "desc": "Connect with family traditions"},
            {"icon": "fas fa-gem", "title": "Quality Focus", "desc": "Invest in quality over quantity"}
        ],
        "colors": ["Brown", "Gray"],
        "lucky_numbers": [4, 8],
        "compatibility": ["Taurus", "Virgo", "Pisces"]
    },
    "aquarius": {
        "icon": "♒",
        "name": "Aquarius",
        "dates": "January 20 - February 18",
        "element": "Air",
        "planet": "Uranus",
        "traits": ["Innovative", "Humanitarian", "Independent", "Intellectual", "Friendly", "Original"],
        "description": "Your hand shows Aquarius' innovative thinking. The unique line patterns and finger shapes indicate originality, humanitarian values, and futuristic vision.",
        "recommendations": [
            {"icon": "fas fa-lightbulb", "title": "Innovation", "desc": "Work on inventive projects"},
            {"icon": "fas fa-hands-helping", "title": "Community Service", "desc": "Volunteer for social causes"},
            {"icon": "fas fa-network-wired", "title": "Networking", "desc": "Connect with diverse groups"},
            {"icon": "fas fa-robot", "title": "Technology", "desc": "Explore new tech trends"}
        ],
        "colors": ["Blue", "Silver"],
        "lucky_numbers": [7, 22],
        "compatibility": ["Gemini", "Libra", "Sagittarius"]
    },
    "pisces": {
        "icon": "♓",
        "name": "Pisces",
        "dates": "February 19 - March 20",
        "element": "Water",
        "planet": "Neptune",
        "traits": ["Compassionate", "Artistic", "Intuitive", "Gentle", "Dreamy", "Empathetic"],
        "description": "Your hand reveals Pisces' sensitive and creative nature. The soft lines and flexible palm indicate strong intuition, artistic talent, and emotional depth.",
        "recommendations": [
            {"icon": "fas fa-paint-brush", "title": "Creative Expression", "desc": "Engage in painting, music, or writing"},
            {"icon": "fas fa-water", "title": "Water Therapy", "desc": "Spend time near water bodies"},
            {"icon": "fas fa-heart", "title": "Compassion Work", "desc": "Help those in need"},
            {"icon": "fas fa-cloud", "title": "Dream Work", "desc": "Keep a dream journal"}
        ],
        "colors": ["Sea Green", "Purple"],
        "lucky_numbers": [3, 9],
        "compatibility": ["Cancer", "Scorpio", "Taurus"]
    }
}

def simple_hand_analysis(image_data):
    """Simple hand analysis without ML - for demo purposes"""
    # In a real application, this would use OpenCV and ML
    # For now, we'll use a deterministic but pseudo-random approach
    
    # Convert base64 to numpy array
    nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Save the image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"uploads/hand_{timestamp}.jpg"
    cv2.imwrite(filename, img)
    
    # Simple image analysis (demo)
    height, width = img.shape[:2]
    
    # Generate a deterministic "fingerprint" from the image
    # This is a simplified version - real ML would be more complex
    avg_color = np.mean(img)
    brightness = np.mean(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    
    # Use image properties to select zodiac (deterministic but varied)
    zodiac_index = int((avg_color + brightness) % 12)
    zodiac_keys = list(ZODIAC_DATA.keys())
    selected_zodiac = zodiac_keys[zodiac_index]
    
    # Add some "analysis details" for realism
    analysis_details = {
        "hand_detected": True,
        "brightness_level": round(float(brightness), 2),
        "image_size": f"{width}x{height}",
        "analysis_confidence": round(random.uniform(85, 95), 1),
        "lines_detected": random.randint(3, 8),
        "dominant_features": random.sample(["Heart Line", "Life Line", "Head Line", "Fate Line", "Mount of Venus"], 3)
    }
    
    return selected_zodiac, analysis_details

@app.route('/')
def serve_frontend():
    """Serve the frontend HTML file"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory(app.static_folder, path)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint to analyze hand image"""
    try:
        data = request.json
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Extract base64 image data
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        
        # Perform hand analysis
        zodiac_key, analysis_details = simple_hand_analysis(image_data)
        
        # Get zodiac information
        zodiac_info = ZODIAC_DATA[zodiac_key].copy()
        zodiac_info['analysis_details'] = analysis_details
        zodiac_info['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add some randomized but realistic palmistry insights
        palmistry_insights = [
            "Your heart line shows emotional depth and passion.",
            "The life line indicates vitality and resilience.",
            "Head line suggests analytical thinking abilities.",
            "Fate line reveals a strong sense of purpose.",
            "Finger shapes indicate creativity and communication skills."
        ]
        
        zodiac_info['palmistry_insights'] = random.sample(palmistry_insights, 3)
        
        return jsonify(zodiac_info)
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        return jsonify({'error': 'Analysis failed', 'details': str(e)}), 500

@app.route('/api/zodiacs', methods=['GET'])
def get_zodiacs():
    """Get list of all zodiac signs"""
    zodiacs_list = []
    for key, data in ZODIAC_DATA.items():
        zodiacs_list.append({
            'key': key,
            'name': data['name'],
            'icon': data['icon'],
            'dates': data['dates'],
            'element': data['element']
        })
    
    return jsonify(zodiacs_list)

@app.route('/api/zodiac/<sign>', methods=['GET'])
def get_zodiac(sign):
    """Get specific zodiac information"""
    if sign.lower() in ZODIAC_DATA:
        return jsonify(ZODIAC_DATA[sign.lower()])
    else:
        return jsonify({'error': 'Zodiac sign not found'}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PalmAI Backend',
        'version': '1.0.0',
        'zodiacs_available': len(ZODIAC_DATA)
    })

if __name__ == '__main__':
    print("Starting PalmAI Backend Server...")
    print(f"• Frontend served from: {app.static_folder}")
    print(f"• Uploads saved to: {os.path.abspath('uploads')}")
    print(f"• API available at: http://localhost:5000/api/analyze")
    print(f"• Total zodiac signs: {len(ZODIAC_DATA)}")
    app.run(debug=True, port=5000)