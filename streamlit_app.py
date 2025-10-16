# Import python packages
import streamlit as st

# Try to connect to Snowflake, handle any connection errors
try:
    cnx = st.connection("snowflake")
    session = cnx.session()
    # Test the session with a simple query to verify connectivity
    session.sql("SELECT 1").collect()
    connection_ok = True
except Exception as e:
    connection_ok = False
    error_message = str(e)

if not connection_ok:
    st.error(f"Could not connect to Snowflake: {error_message}")
    st.stop()

# Write directly to the app
st.title(f":cup_with_straw: CUSTOMIZE YOUR SMOOTHIE :cup_with_straw:")
st.write(
    """ CHOOSE THE FRUITS IN YOUR CUSTOM SMOOTHIE
    """
)

User_input = st.text_input('YOUR NAME PLEASE: ')

from snowflake.snowpark.functions import col, when_matched

# Fetch fruit options from Snowflake
try:
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
    fruit_options = [row['FRUIT_NAME'] for row in my_dataframe.collect()]
except Exception as e:
    st.error(f"Error fetching fruit options from Snowflake: {e}")
    st.stop()

ingredients_list = st.multiselect(
    'CHOOSE UPTO 5 INGREDIENTS:',
    fruit_options
)

if ingredients_list:
    ingredients_string = ','.join(ingredients_list)
    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values('{ingredients_string}', '{User_input}')
    """

    try:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    except Exception as e:
        st.error(f"Error placing your order: {e}")
