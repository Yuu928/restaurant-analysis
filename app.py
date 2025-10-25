import streamlit as st
import pandas as pd
import plotly.express as px

def create_sample_data():
    """Create a sample data file"""
    try:
        df = pd.read_csv('data/restaurants.csv')
        
        sample_df = df.sample(3000, random_state=42)
        
        sample_df.to_csv('data/restaurant_sample.csv', index=False)
        
        st.success(f"The sample data has been successfully created! with {len(sample_df)} records")
        return sample_df
        
    except Exception as e:
        st.error(f"Sample creation failed: {e}")
        return None

#create_sample_data()

# Configure page
st.set_page_config(page_title="Restaurant Analysis", layout="wide")

# App title
st.title("🍽️ Restaurant Insights")
st.subheader("TripAdvisor European Restaurants Analysis")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/restaurant_sample.csv') 
        st.success("Data loaded successfully!")
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please place CSV file in data folder.")
        return pd.DataFrame()

df = load_data()

# Display app content if data loaded successfully
if not df.empty:
    # Display basic information
    st.write(f"Dataset contains **{len(df)}** restaurants")
    
    # Display data column information
    st.write("Data columns:", list(df.columns))
    
    # Sidebar filters
    st.sidebar.header("🔍 Data Filters")
    
    # City selector
    if 'City' in df.columns:
        cities = st.sidebar.multiselect(
            "Select Cities:",
            options=df['City'].unique(),
            default=df['City'].unique()[:2] if len(df) > 0 else []
        )
    else:
        cities = []
        st.sidebar.write("No 'City' column in data")
    
    # Apply filters
    filtered_df = df.copy()
    if cities:
        filtered_df = filtered_df[filtered_df['City'].isin(cities)]
    
    # Create tab layout
    tab1, tab2, tab3 = st.tabs(["📊 City Analysis", "📈 Price Relationship", "🥧 Cuisine Distribution"])
    
    with tab1:
        # Bar chart - Average ratings by city
        if 'Rating' in df.columns and 'City' in df.columns:
            st.subheader("Average Ratings by City")
            city_ratings = filtered_df.groupby('City')['Rating'].mean().sort_values(ascending=False)
            fig1 = px.bar(
                x=city_ratings.index,
                y=city_ratings.values,
                title="City Ratings Comparison",
                labels={'x': 'City', 'y': 'Average Rating'}
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.write("Missing rating or city data")
    
    with tab2:
        # Scatter plot - Price vs Rating relationship
        st.subheader("Price vs Rating Relationship")
        if 'Rating' in df.columns and 'Price Range' in df.columns:
            fig2 = px.scatter(
                filtered_df,
                x='Price Range',
                y='Rating',
                color='City' if 'City' in df.columns else None,
                title="Price vs Rating"
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.write("Missing price or rating data")
    
    with tab3:
        # Pie chart - Cuisine distribution
        st.subheader("Cuisine Distribution")
        if 'Cuisine Style' in df.columns:
            cuisine_counts = filtered_df['Cuisine Style'].value_counts().head(10)
            fig3 = px.pie(
                values=cuisine_counts.values,
                names=cuisine_counts.index,
                title="Top 10 Cuisine Distribution"
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.write("Missing cuisine data")
    
    # Data display
    st.subheader("Restaurant Data")
    st.dataframe(filtered_df.head(20))

else:
    st.info("Please place TripAdvisor restaurant data CSV file in the data folder")