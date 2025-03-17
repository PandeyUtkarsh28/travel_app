import streamlit as st 
import pandas as pd
import folium
from streamlit_folium import st_folium
import requests
import paypalrestsdk
import logging
import streamlit.components.v1 as components

# Configuration
st.set_page_config(page_title="Explore India", page_icon="🌐", layout="wide")
st.title("🇮🇳 Explore India Tourism Dashboard")
st.markdown("Discover popular destinations, interactive maps, curated travel packages, and book your dream hotels.")

# Background CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://th.bing.com/th/id/R.1a57565e1a8f2b2bdeb899723310ae81?rik=UQmcqSAXD%2fP1LQ&riu=http%3a%2f%2ftravelfore.com%2fwp-content%2fuploads%2f2016%2f04%2fbali.jpg&ehk=v9y0vodV%2bGS1smYLfGV3NX%2fWPGkODQaRrgUDcthpyZ0%3d&risl=&pid=ImgRaw&r=0p');
        background-size: cover;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sample Data
destinations_data = {
    "Destination": ["Taj Mahal", "Goa Beaches", "Jaipur", "Kashmir Valley", "Kerala Backwaters", 
                    "Hampi", "Rishikesh", "Andaman Islands", "Darjeeling", "Ladakh"],
    "State": ["Uttar Pradesh", "Goa", "Rajasthan", "Jammu & Kashmir", "Kerala",
              "Karnataka", "Uttarakhand", "Andaman & Nicobar", "West Bengal", "Ladakh"],
    "Category": ["Heritage", "Beach", "Cultural", "Nature", "Adventure",
                 "Heritage", "Adventure", "Beach", "Nature", "Adventure"],
    "Average Cost (₹)": [41000, 57000, 49000, 65500, 61400, 52000, 45000, 62000, 58000, 70000],
    "Image": [
        "https://4.bp.blogspot.com/-TrWYtD3zcaY/Wq0ZjzgDGJI/AAAAAAAAAmY/OBwAVhu7FJM-K9DT7MDZ43BFDRdZd0u8gCEwYBhgL/s1600/taj-mahal-1400824_1920.jpg",
        "https://q-xx.bstatic.com/xdata/images/hotel/max1200/207321005.jpg?k=1edb37487105bfdb2e86e1cc39788982b80d3a523a5eace91e62f3f2c32ae469&o=",
        "https://th.bing.com/th/id/OIP.osd9uY4SJIRwNZPtMX16cQHaDt?rs=1&pid=ImgDetMain",
        "https://th.bing.com/th/id/OIP.ffBB1VVWj8PyORP5tksoEAHaE7?rs=1&pid=ImgDetMain",
        "https://th.bing.com/th/id/OIP.HyjU2tItxGqeu1piwJogEQHaE8?rs=1&pid=ImgDetMain",
        "https://karnatakatourism.org/wp-content/uploads/2020/05/Hampi.jpg",
        "https://www.holidify.com/images/bgImages/RISHIKESH.jpg",
        "https://th.bing.com/th/id/OIP.gC271gC_vAEdwZXsGVaufQHaE8?rs=1&pid=ImgDetMain",
        "https://sikkimtourism.org/wp-content/uploads/2022/06/Darheeling-Toy-Train.jpg",
        "https://th.bing.com/th/id/OIP.cU66fTkWKwf-knmNo_LY7gHaE8?rs=1&pid=ImgDetMain",
    ],
    "Latitude": [27.1751, 15.2993, 26.9124, 34.0837, 9.9312, 15.3350, 30.0869, 12.0016, 27.0410, 34.1526],
    "Longitude": [78.0421, 73.9091, 75.7873, 74.7973, 76.2673, 76.4600, 78.2678, 93.8552, 88.2627, 77.5772],
    "Availability": ["Available", "Few Slots", "Available", "Sold Out", "Few Slots", "Available", "Available", "Sold Out", "Few Slots", "Available"]
}

destinations_df = pd.DataFrame(destinations_data)

hotels_data = {
    "Hotel Name": ["Taj Hotel", "Leela Beach Resort", "Raj Mahal", "Houseboat Stay", "Backwater Retreat",
                   "Hampi Palace", "Rishikesh Retreat", "Andaman Seaside", "Darjeeling Heights", "Ladakh Serenity"],
    "Destination": ["Taj Mahal", "Goa Beaches", "Jaipur", "Kerala Backwaters", "Kashmir Valley",
                    "Hampi", "Rishikesh", "Andaman Islands", "Darjeeling", "Ladakh"],
    "Cost per Night (₹)": [9840, 12300, 8200, 6560, 7380, 7000, 6000, 8500, 9200, 11000],
    "Rating": [4.8, 4.7, 4.6, 4.9, 4.5, 4.6, 4.4, 4.7, 4.5, 4.8],
    "Image": [
        "https://imgcld.yatra.com/ytimages/image/upload/t_hotel_yatra_details_desktop/v1449645827/Domestic%20Hotels/Hotels_Agra/Hotel%20Taj%20Resorts/ENTRANCE-1.jpg",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/20/64/f2/b3/sibaya-beach-resort.jpg?w=1400&h=-1&s=1",
        "https://i.pinimg.com/originals/f4/02/da/f402da68c36ad9634d9be2ef741c0a43.jpg",
        "https://s4.scoopwhoop.com/anj/houseboat/731473165.jpg",
        "https://th.bing.com/th/id/R.e448f6d151211f96baa5a66bd2845a4b?rik=RBXZvx8YpJeg0A&riu=http%3a%2f%2fwww.inditales.com%2fwp-content%2fuploads%2f2016%2f03%2fthe-khyber-himalayan-resort-spa-gulmarg-640x330.jpg&ehk=JLM07qX0dhjx6Wv%2fKB9qLBtdm5gBCMnZTp53FP1Pk9w%3d&risl=&pid=ImgRaw&r=0",
        "https://www.shivavilaspalacehotel.com/assets/img/banner4.jpg",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/22/e2/48/67/justa-rasa-retreat-spa.jpg?w=1400&h=-1&s=1",
        "https://th.bing.com/th/id/OIP.JQ8OMezwlzC0fk01UdUVLQHaEK?rs=1&pid=ImgDetMain",
        "https://th.bing.com/th/id/OIP.Q0zLjosBGeAIFCR2vP9J9gHaE8?rs=1&pid=ImgDetMain",
        "https://th.bing.com/th/id/OIP.E9W78KQnXWm_Fl55Pfdy7QHaEo?rs=1&pid=ImgDetMain",
    ],
}

# Load Data into DataFrames
destinations_df = pd.DataFrame(destinations_data)
hotels_df = pd.DataFrame(hotels_data)

# Utility Functions
def display_destinations(df, category="All"):
    filtered_df = df if category == "All" else df[df["Category"] == category]
    for _, row in filtered_df.iterrows():
        st.image(row["Image"], use_column_width=True)
        st.write(f"**{row['Destination']}** ({row['Category']}) - {row['State']}")
        st.write(f"*Cost:* ₹{row['Average Cost (₹)']} | *Availability:* {row['Availability']}")
        st.markdown("---")

def generate_map(df):
    map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(
                f"<b>{row['Destination']}</b><br>Category: {row['Category']}<br>Cost: ₹{row['Average Cost (₹)']}<br>Availability: {row['Availability']}",
                max_width=200,
            ),
            tooltip=row["Destination"]
        ).add_to(map)
    return map

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

# Personalized Chatbot
def personalized_chatbot():
    st.subheader("Ask Our Travel Assistant")
    user_input = st.text_input("Type your question here")
    if user_input:
        if "destination" in user_input.lower():
            st.write("Looking for destination information? Here's a list of popular spots:")
            display_destinations(destinations_df)
        elif "ticket" in user_input.lower():
            st.write("You can raise a ticket for assistance. Please fill in the following details:")
            name = st.text_input("Your Name")
            issue = st.text_area("Describe your issue")
            if st.button("Submit Ticket"):
                st.success("Your ticket has been submitted. Our team will get back to you shortly!")
        elif "call back" in user_input.lower():
            st.write("Request a call back. Please provide your details:")
            name = st.text_input("Your Name")
            phone = st.text_input("Your Phone Number")
            if st.button("Request Call Back"):
                st.success("Our team will call you back shortly!")
        else:
            st.write("Our assistant is working on your query. Please wait a moment.")

# Navigation
page = st.sidebar.radio("Navigate", ["Home", "Destinations", "Interactive Map", "Travel Planner","Hotel Booking", "Weather Forecast", "Advanced Tools", "Contact Us", "Payment"])
# Home Page
if page == "Home":
    # Home Page Content (Destinations and Booking)
    st.subheader("🌟 Popular Destinations")
    cols = st.columns(5)
    for i, row in destinations_df.iterrows():
        with cols[i % 5]:
            st.image(row["Image"], caption=row["Destination"], use_column_width=True)
            st.write(f"**{row['Category']}** - ₹{row['Average Cost (₹)']}")
    st.subheader("Chat with Our Travel Assistant")
    personalized_chatbot()


    # User Reviews
    st.subheader("User Reviews")
    reviews = st.text_area("Write a review about your experience")
    if st.button("Submit Review"):
        st.success("Thank you for your review!")
        st.write(reviews)
        # Note: In a real app, you would save the review to a database or file

if page == "Travel Planner":
    st.subheader("Plan Your Journey")
    st.markdown("Fill in the details below to get a personalized travel plan:")

    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    destination = st.selectbox("Choose a Destination", options=destinations_df["Destination"].unique())
    travel_date = st.date_input("Select Travel Date")
    num_days = st.number_input("Number of Days", min_value=1, step=1)
    budget = st.number_input("Travel Budget (₹)", min_value=1, step=500)

    if st.button("Generate Plan"):
        st.success("Travel Plan Generated!")
        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Destination:** {destination}")
        st.write(f"**Travel Date:** {travel_date}")
        st.write(f"**Duration:** {num_days} days")
        st.write(f"**Budget:** ₹{budget}")

        # Example of Personalized Recommendation
        st.markdown("### Personalized Recommendations")
        st.write("**Activities:** Visit the local markets, explore historical sites, and enjoy regional cuisines.")
        st.write("**Recommended Hotels:**")
        st.write("1. Hotel A (₹5,000 per night)")
        st.write("2. Hotel B (₹7,500 per night)")

if page == "Interactive Map":
    st.subheader("Explore Destinations on the Map")
    map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    for _, row in destinations_df.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(
                f"<b>{row['Destination']}</b><br>Category: {row['Category']}<br>Average Cost: ₹{row['Average Cost (₹)']}<br>Availability: {row['Availability']}",
                max_width=200,
            ),
            tooltip=row["Destination"],
        ).add_to(map)

    st_folium(map, width=700, height=500)

if page == "Special Packages":
    st.subheader("Exclusive Travel Packages")
    st.markdown("Check out our curated packages for the best travel experience!")
    # Example of adding packages
    st.write("1. Heritage Tour of Rajasthan (₹50,000)")
    st.write("2. Beach Fun in Goa (₹75,000)")
    st.write("3. Nature Escape to Kerala (₹60,000)")

if page == "Hotel Reviews":
    st.subheader("Hotel Reviews")
    st.markdown("Get insights from real travelers.")
    # Example of adding hotel reviews
    reviews_df = pd.DataFrame({
        "Hotel": ["Hotel A", "Hotel B", "Hotel C"],
        "Review": ["Excellent service and location!", "Very comfortable stay.", "Good value for money."],
        "Rating": [5, 4, 4]
    })

    for _, row in reviews_df.iterrows():
        st.write(f"**{row['Hotel']}**")
        st.write(f"Rating: {'⭐'*row['Rating']}")
        st.write(f"Review: {row['Review']}")
        st.markdown("---")

    # Allowing users to submit their own reviews
    st.subheader("Submit Your Review")
    hotel = st.selectbox("Select Hotel", options=reviews_df["Hotel"].unique())
    user_review = st.text_area("Your Review")
    user_rating = st.slider("Your Rating", 1, 5, 3)
    if st.button("Submit Review"):
        st.success("Thank you for your review!")
        # Note: In a real app, you would save the review to a database or file    

    # Hotel Booking Section
    
    st.subheader("🏨 Hotel Booking")
    for i, row in hotels_df.iterrows():
        with st.expander(f"Book {row['Hotel Name']} in {row['Destination']}"):
            st.image(row["Image"], use_column_width=True)
            st.write(f"**Cost per Night:** ₹{row['Cost per Night (₹)']} | **Rating:** {row['Rating']} ⭐")
            
            nights = st.number_input("Enter Number of Nights:", min_value=1, step=1, key=f"nights_{i}")
            total_cost = row["Cost per Night (₹)"] * nights
            
            if nights:
                st.write(f"**Total Cost:** ₹{total_cost}")
                
     # Hotel Booking Page with PayPal Integration
elif page == "Hotel Booking":
    st.subheader("🏨 Book Your Favorite Hotel")
    
    for i, row in hotels_df.iterrows():
        with st.expander(f"Book {row['Hotel Name']} in {row['Destination']}"):
            st.image(row["Image"], use_column_width=True)
            st.write(f"**Cost per Night:** ₹{row['Cost per Night (₹)']} | **Rating:** {row['Rating']} ⭐")
            
            nights = st.number_input("Enter Number of Nights:", min_value=1, step=1, key=f"nights_{i}")
            total_cost = row["Cost per Night (₹)"] * nights
            
            if nights:
                st.write(f"**Total Cost:** ₹{total_cost}")
                
           
# PayPal client ID - Use your own PayPal client ID here.
PAYPAL_CLIENT_ID = "Ae-2B4oTVFzyz1EiWc7yzDY9FL-B1lvKQhV-UN8HVAJ_UN6tfbVV6_BknWz-0eGNfw6wrjoTaBgNAydf"

# Define hotel prices (in INR)
hotel_prices = {
    "Hotel A": 2000,  # Price per night
    "Hotel B": 2500,
    "Hotel C": 3000
}

# Function to handle booking and payment
def handle_booking_payment(hotel, nights, total_cost, user_info):
    # Here you can add functionality to store the booking information in a database
    # For simplicity, let's just show a confirmation message
    st.write(f"Booking confirmed for {hotel}!")
    st.write(f"Total cost: ₹{total_cost}")
    st.write(f"Name: {user_info['name']}")
    st.write(f"Email: {user_info['email']}")
    st.write(f"Phone: {user_info['phone']}")
    st.success("Payment Successful! Your booking is confirmed.")

# Streamlit page setup
st.title("Hotel Booking System")
st.write("Please select a hotel, enter your details, and proceed to payment")

# Create booking form
hotel = st.selectbox("Select Hotel", ["Hotel A", "Hotel B", "Hotel C"])
nights = st.number_input("Number of Nights", min_value=1, value=1)
full_name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone")

# Calculate total cost
total_cost = hotel_prices[hotel] * nights

# Display booking details
st.write(f"Hotel: {hotel}")
st.write(f"Number of Nights: {nights}")
st.write(f"Total Cost: ₹{total_cost}")

# Create a dictionary to store user info
user_info = {
    'name': full_name,
    'email': email,
    'phone': phone
}

# Proceed to payment button
if st.button("Proceed to Payment"):
    # Render PayPal button with Streamlit components
    html_code = f"""
    <script src="https://www.paypal.com/sdk/js?client-id=Ae-2B4oTVFzyz1EiWc7yzDY9FL-B1lvKQhV-UN8HVAJ_UN6tfbVV6_BknWz-0eGNfw6wrjoTaBgNAydf&currency=INR"></script>
    <div id="paypal-button-container"></div>
    <script>
    paypal.Buttons({{
        createOrder: function(data, actions) {{
            return actions.order.create({{
                purchase_units: [{{
                    amount: {{
                        value: '{total_cost:.2f}'
                    }},
                    description: 'Hotel Booking for {hotel}'
                }}]
            }});
        }},
        onApprove: function(data, actions) {{
            return actions.order.capture().then(function(details) {{
                alert('Payment successful! Booking confirmed for ' + details.payer.name.given_name);
                // Store booking info in a database or send confirmation email
                // Optionally, you could send the details to your backend here
                window.location.reload(); // Refresh to show the booking confirmation
            }});
        }},
        onCancel: function(data) {{
            alert('Payment was canceled!');
        }},
        onError: function(err) {{
            console.log(err);
            alert('An error occurred during payment processing.');
        }}
    }}).render('#paypal-button-container');
    </script>
    """
    
    # Inject the PayPal button using Streamlit's components
    components.html(html_code, height=500)

# After Payment Success: Show Confirmation Message
if st.session_state.get('payment_success', False):
    handle_booking_payment(hotel, nights, total_cost, user_info)
elif page == "Destinations":
    st.subheader("Find Your Destination")
    category = st.selectbox("Choose a Category", ["All"] + list(destinations_df["Category"].unique()))
    display_destinations(destinations_df, category)

elif page == "Interactive Map":
    st.subheader("Explore Destinations on the Map")
    map = generate_map(destinations_df)
    st_folium(map, width=700, height=500)

elif page == "Weather Forecast":
    st.subheader("Weather Forecast")
    city = st.text_input("Enter a City", "Delhi")
    api_key = "baa7386be72afe4fbfa2aa29b7091d8b"
    if city:
        data = get_weather(city, api_key)
        if data.get("cod") == 200:
            st.write(f"**City:** {city}")
            st.write(f"**Weather:** {data['weather'][0]['description']}")
            st.write(f"**Temperature:** {data['main']['temp']}°C")
            st.write(f"**Feels Like:** {data['main']['feels_like']}°C")
            st.write(f"**Humidity:** {data['main']['humidity']}%")
        else:
            st.error("Could not fetch weather data. Please try again.")

elif page == "Contact Us":
    st.subheader("Contact Us")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    if st.button("Submit"):
        st.success("Thank you for your message!")

 
# Pricing Calculator
st.sidebar.subheader("Pricing Calculator")
days = st.sidebar.number_input("Number of Days", min_value=1, step=1)
daily_budget = st.sidebar.number_input("Daily Budget (₹)", min_value=0, step=500)
total_budget = days * daily_budget
st.sidebar.write(f"**Total Budget:** ₹{total_budget}")

# User Dashboard
st.sidebar.subheader("User Dashboard")
user_name = st.sidebar.text_input("Enter your name for personalized experience:")
if user_name:
    st.sidebar.write(f"Welcome, {user_name}!")
    st.sidebar.write("Here is your personalized dashboard:")
    st.sidebar.write(f"Total Budget: ₹{total_budget}")
    st.sidebar.write(f"Travel Plan: {days} days with a daily budget of ₹{daily_budget}")
