# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()


# Write directly to the app
st.title(f":cup_with_straw: CUSTOMIZE YOUR SMOOTHIE :cup_with_straw:")
st.write(
  """ CHOOSE THE FRUITS IN YOUR CUSTOM SMOOTHIE
  """
)

User_input = st.text_input('YOUR NAME PLEASE: ')










from snowflake.snowpark.functions import col, when_matched



my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))



ingredients_list = st.multiselect(
    'CHOOSE UPTO 5 INGREDIENTS:',
    my_dataframe
)



if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen
        
        
        my_insert_stmt = """insert into smoothies.public.orders(ingredients,name_on_order)
        values('"""+ ingredients_string+"""','"""+User_input+"""')"""
    
    
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon ="✅")


