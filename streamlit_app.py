# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothi")
st.write(
    "Choose the fruits you want into your smoothie"
)


name_on_order=st.text_input('Name of Smoothie')
st.write('The Name Of Your Smoothie will be:- ',name_on_order)
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingrediants_list=st.multiselect('Choose up to 5 ingrediants:', my_dataframe, max_selections=5)
 
if ingrediants_list:
# st.write(ingrediants_list)
# st.text(ingrediants_list)
 ingredients_string=''
 for fruit_choosen in ingrediants_list:
     ingredients_string +=fruit_choosen +' '

 #st.write(ingredients_string)

 my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string+ """','"""+name_on_order+"""')"""

#st.write(my_insert_stmt)   

time_to_insert=st.button('Submit Order')

if time_to_insert:
   session.sql(my_insert_stmt).collect()
   st.success('Your Smoothie is ordered!', icon="✅")
