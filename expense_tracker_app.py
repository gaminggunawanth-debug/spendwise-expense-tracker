import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# Custom Styling
st.set_page_config(page_title="SpendWise", page_icon="💸", layout="centered")

# Custom CSS for better look
st.markdown("""
    <style>
    .main {background-color: #0f0f1a;}
    .stApp {background-color: #0f0f1a; color: #ffffff;}
    h1 {color: #00ff9d; font-size: 3rem;}
    .metric-label {color: #00ff9d !important;}
    </style>
""", unsafe_allow_html=True)

st.title("💸 SpendWise")
st.markdown("**Your Personal Expense Tracker** | Track • Visualize • Control")

# Initialize
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Sidebar
with st.sidebar:
    st.header("Add New Expense")
    with st.form("expense_form"):
        item = st.text_input("What did you buy/spend on?")
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Amount ₹", min_value=0.0, step=50.0)
            date = st.date_input("Date", datetime.now())
        with col2:
            category = st.selectbox("Category", 
                ["Food & Drinks", "Transport", "Shopping", "Entertainment", 
                 "Bills & Recharge", "Study Materials", "Travel", "Other"])
        
        submitted = st.form_submit_button("➕ Add Expense", type="primary")
        if submitted and item and amount > 0:
            st.session_state.expenses.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Item": item.title(),
                "Amount": amount,
                "Category": category
            })
            st.success("Expense Added Successfully! 🎉")

# Main Content
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Spent", f"₹{df['Amount'].sum():,.0f}")
    with col2:
        st.metric("Transactions", len(df))
    with col3:
        st.metric("Avg per day", f"₹{df['Amount'].mean():.0f}")
    
    st.subheader("📊 Spending by Category")
    fig = px.pie(df, names='Category', values='Amount', hole=0.4, 
                 color_discrete_sequence=px.colors.sequential.Mint)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📋 All Expenses")
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)
    
    # Monthly trend (simple)
    df['Date'] = pd.to_datetime(df['Date'])
    daily = df.groupby('Date')['Amount'].sum().reset_index()
    st.subheader("📈 Daily Spending Trend")
    st.line_chart(daily.set_index('Date'))
    
else:
    st.info("No expenses added yet. Use the sidebar to add your first expense 💰")

# Footer
if st.button("🗑️ Clear All Data"):
    st.session_state.expenses = []
    st.success("All data cleared!")

st.caption("Built by you • For your freedom to roam the world 🌍")