# Import python packages
import streamlit as st
streamlit.title('My Parents new healthy Dinner')
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize the Smoothie {st.__version__}")
st.write(
    """
    Select fruit and customize your smoothie.
    """
)

cnx = st.connection("Snowflake")
session = cnx.session()

# Input for smoothie name
name_on_order = st.text_input("Name of Smoothie:")
st.write("The name of your smoothie will be:", name_on_order)

# Get active Snowflake session
session = get_active_session()

# Load available fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
st.dataframe(data=my_dataframe, use_container_width=True)

# Multiselect for ingredients with max 5 selections
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    # Build a string of chosen ingredients
    ingredients_string = " ".join(ingredients_list)

    # ✅ Corrected insert statement with both columns
    sql_insert = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # 👀 Show the SQL for debugging
    st.write(sql_insert)

    # Button to run the insert
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(sql_insert).collect()
        st.success(
            f"Your Smoothie is ordered, {name_on_order}! 🥤",
            icon="✅"
        )
