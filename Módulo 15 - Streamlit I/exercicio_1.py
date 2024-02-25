import streamlit as st
import pandas as pd
import numpy as np

st.markdown('## Tell us your name:')
st.text_input("**Write down below** :arrow_down:", key="name")
if st.session_state.name != "":
    st.title(f"Welcome to this interactive page, {st.session_state.name}")
    st.markdown(f"- ### {st.session_state.name} ,if you're an astronomy enthusiast like me, I'd like to share three interesting images with you!")
else:
    st.write("")


col1, col2, col3 = st.columns(3)

with col1:
   st.header("Western Veil Nebula:")
   st.image("https://apod.nasa.gov/apod/image/2310/WesternVeil_Wu_960.jpg")
   button_neb = st.button('Nebula Details')
   if button_neb:
      st.markdown("**Explanation**")       

with col2:
   st.header("Creature Aurora Over Norway:")
   st.image("https://apod.nasa.gov/apod/image/2311/CreatureAurora_Salomonsen_960.jpg")
   button_auro = st.button('Aurora Details')
   if button_auro:
      st.markdown("**Explanation**")

with col3:
   st.header("Hummingbird Galaxy:")
   st.image("https://apod.nasa.gov/apod/image/2309/Arp142_HubbleChakrabarti_960.jpg")
   button_galax = st.button('Galaxy Details')
   if button_galax:
      st.markdown("**Explanation**")


if button_neb:
      st.markdown("### Dust and the Western Veil Nebula")
      st.markdown("""It's so big it is easy to miss. The entire Veil Nebula spans six times the diameter of the full moon, 
                  but is so dim you need binoculars to see it. The nebula was created about 15,000 years ago when a star 
                  in the constellation of the Swan (Cygnus) exploded. The spectacular explosion would have appeared brighter 
                  than even Venus for a week - but there is no known record of it. Pictured is the western edge of the 
                  still-expanding gas cloud. Notable gas filaments include the Witch's Broom Nebula on the upper left near 
                  the bright foreground star 52 Cygni, and Fleming's Triangular Wisp (formerly known as Pickering's Triangle) 
                  running diagonally up the image middle. What is rarely imaged -- but seen in the featured long exposure across 
                  many color bands -- is the reflecting brown dust that runs vertically up the image left, dust likely created in 
                  the cool atmospheres of massive stars.""") 
      st.markdown("[Text Origin](https://apod.nasa.gov/apod/ap231018.html)")

if button_auro:
      st.markdown("### Creature Aurora Over Norway")
      st.markdown("""It was Halloween and the sky looked like a creature. Exactly which creature, the astrophotographer was unsure 
                  (but possibly you can suggest one). Exactly what caused this eerie apparition in 2013 was sure: one of the best 
                  auroral displays that year. This spectacular aurora had an unusually high degree of detail. Pictured here, the vivid 
                  green and purple auroral colors are caused by high atmospheric oxygen and nitrogen reacting to a burst of incoming 
                  electrons. Birch trees in Tromsø, Norway formed an also eerie foreground. Frequently, new photogenic auroras accompany 
                  new geomagnetic storms.""")
      st.markdown("[Text Origin](https://apod.nasa.gov/apod/ap231105.html)")

if button_galax:
      st.markdown("### Arp 142: The Hummingbird Galaxy")
      st.markdown("""What's happening to this spiral galaxy? Just a few hundred million years ago, NGC 2936, the upper of the two large
                   galaxies shown at the bottom, was likely a normal spiral galaxy -- spinning, creating stars -- and minding its own 
                  business. But then it got too close to the massive elliptical galaxy NGC 2937, just below, and took a turn. Sometimes 
                  dubbed the Hummingbird Galaxy for its iconic shape, NGC 2936 is not only being deflected but also being distorted by the 
                  close gravitational interaction. Behind filaments of dark interstellar dust, bright blue stars form the nose of the 
                  hummingbird, while the center of the spiral appears as an eye. Alternatively, the galaxy pair, together known as Arp 142, 
                  look to some like Porpoise or a penguin protecting an egg. The featured re-processed image showing Arp 142 in great 
                  detail was taken recently by the Hubble Space Telescope. Arp 142 lies about 300 million light years away toward the 
                  constellation of the Water Snake (Hydra). In a billion years or so the two galaxies will likely merge into one larger 
                  galaxy.""")
      st.markdown("[Text Origin](https://apod.nasa.gov/apod/ap230925.html)")

st.title("Measurement Converter")
st.markdown("### LBS to KG:")

def lbs_to_kg():
   st.session_state.kg = st.session_state.lbs/2.2046
  
def kg_to_lbs():
   st.session_state.lbs = st.session_state.kg*2.2046 

col1, buff, col2 = st.columns(3)

with col1:
   pounds = st.number_input("Pounds:", key="lbs", 
                            on_change= lbs_to_kg)
with col2:
   kilogram = st.number_input("kilograms:", key="kg", 
                            on_change= kg_to_lbs)
   

st.title("Pizza Dough")

col1, buff, col2 = st.columns(3)

with col1:
    st.slider("Flour(Kg)", 0, 10,1, key='flour')

with col2:
    st.slider("Moisture Percentage(%)", 0, 100,60, key='percent')

value = (st.session_state.flour*1000)*(st.session_state.percent/100)
st.title("Water Measure:")
st.markdown(f"## {value}")

st.title('Uber pickups in NYC:')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)