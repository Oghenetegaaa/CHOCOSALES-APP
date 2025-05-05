import streamlit as st 
import pandas as pd 
import altair as alt


def load_data():
    df = pd.read_csv("chocosales.csv")
    #Convert date column to datetime date type
    df.Date = pd.to_datetime(df.Date,format="%d-%b-%y")
    # Convert the Amount column to float datatype
    df.Amount = df.Amount.str.replace("$","").str.replace(",","").str.strip().astype("float")
    return df 

df = load_data()

# App title
st.title("Chocolate Sales App")

#create filters
filters ={
    "SalesPerson": df["Sales Person"].unique(),
    "Country":df["Country"].unique(),
    "Product":df["Product"].unique()
}

# store user selection
selected_filters ={}


# generate multi-select widgets dynamically
for key, options in filters.items():
    selected_filters[key] = st.sidebar.multiselect(key,options)

# lets have full data
filtered_df = df.copy()


# Supply filter selection to the data
for key, selected_values in selected_filters.items():
    if selected_values:
        filtered_df = filtered_df[filtered_df[key].isin(selected_values)]

#display the data
st.dataframe(filtered_df.head())


# calculations
no_of_transactions = len(filtered_df)
total_revenue = filtered_df["Amount"].sum()
total_boxes = filtered_df["Boxes Shipped"].sum()
no_of_products = filtered_df["Product"].nunique()


#streamlit column component
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Transactions",no_of_transactions)

with col2:
    st.metric("Total Revenue",total_revenue)

with col3:
    st.metric("Total boxes",total_boxes)

with col4:
    st.metric("Products",no_of_products)


st.dataframe(df.head())

#charts
st.subheader("Products with the largest revenue")

top_products=filtered_df.groupby("Product")["Amount"].sum().nlargest(5).reset_index()

st.write(top_products)

 # alrair plotting library
chart1 =alt.Chart(top_products).mark_bar().encode(
    x=alt.X('Amount:Q', title= "Revenue ($)"),
    y=alt.Y("Product:N"),
    color = alt.Color("Product:N", legend= None)
 ).properties(height = 300)

 # display the chart
st.altair_chart(chart1, use_container_width = True)

#piechart
data = filtered_df.groupby("Country")["Amount"].sum().reset_index()
data['percent'] = data['Amount'] / data['Amount'].sum() * 100


st.write(data)

chart2 = alt.Chart(data).mark_arc().encode(
    theta = alt.Theta('Amount', type = "quantitative", title = "Percentage of country"),
    color = alt.Color('Country', type = "nominal"),
    tooltip = ['Country', 'Amount', alt.Tooltip('percent:Q', format='.2f')] 
)


st.altair_chart(chart2, use_container_width = True)


#group by country
country_gain = filtered_df.groupby("Country")["Amount"].sum().reset_index()

st.write(country_gain)

chart3 = alt.Chart(country_gain).mark_bar().encode(
    x = alt.X("Country"),
    y = alt.Y("Amount", title = "Revenue($)"),
    color = alt.Color("Amount")
)

st.altair_chart(chart3, use_container_width = True)


#sales by salesperson (Bar)

sales_person = filtered_df.groupby("Sales Person")["Amount"].sum().reset_index()

st.write(sales_person)

chart3 = alt.Chart(sales_person).mark_bar().encode(
    x = alt.X("Amount", title = "Revenue($)"),
    y = alt.Y("Sales Person"),
color = alt.Color("Amount")
)

st.altair_chart(chart3, use_container_width = True)

#change date to datetime

df["Date"] = pd.to_datetime(df["Date"])

#extract month from date
df['Month'] = df['Date'].dt.month

#Group by revenue and sum the revenue
month_sales = df.groupby("Month")["Amount"].sum().reset_index()
st.write(month_sales)

chart4 = alt.Chart(month_sales).mark_line().encode(
    x = alt.X("Month" , title = "Sales for each month."),
    y = alt.Y("Amount")
)
st.altair_chart(chart4 , use_container_width = True)
