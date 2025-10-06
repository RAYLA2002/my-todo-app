import streamlit as st
import functions

# --- تنظیمات اولیه ---
st.set_page_config(layout="centered", page_title="My To-Do App")

todos = functions.get_todos()

# --- توابع Callback اصلاح‌شده ---

def add_todo():
    """فقط برای دکمه تنظیم شده تا از فراخوانی تکراری جلوگیری کند."""
    new_todo_item = st.session_state.get("new_input") # نام کلید ورودی تغییر کرد
    if new_todo_item:
        todos.append(new_todo_item.strip() + "\n")
        functions.write_todos(todos)
        st.session_state["new_input"] = "" # ورودی پس از افزودن پاک می‌شود

def complete_todo(todo_text_to_remove):
    try:
        item_to_remove = todo_text_to_remove.strip() + "\n"
        todos.remove(item_to_remove)
        functions.write_todos(todos)
        st.rerun() 
    except ValueError:
        st.error(f"Error removing: '{todo_text_to_remove.strip()}' not found.")

# --- رابط کاربری برنامه (Application UI) ---

# CSS سفارشی (بدون تغییر)
st.markdown("""
    <style>
    .st-emotion-cache-1jri7xp {
        color: #1E88E5;
        font-family: 'Arial Black', sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stCheckbox > label {
        font-size: 1.1em;
        padding-left: 10px;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 مدیریت وظایف ")
st.markdown("### **:blue[بهره‌وری خود را افزایش دهید!]**")
st.write("وظایف خود را با نظم و ترتیب مدیریت کنید. 
st.divider()

if not todos:
    st.info("لیست وظایف شما خالی است.")

for index, todo in enumerate(todos):
    with st.container(border=True): 
        display_text = todo.strip()
        
        st.checkbox(
            label=display_text, 
            key=f"todo_item_{index}_{display_text}",
            value=False, 
            on_change=complete_todo, 
            args=(display_text,)
        )
        
st.divider()

col1, col2 = st.columns([4, 1])

with col1:
    # --- تغییر کلیدی: on_change حذف شد و key به "new_input" تغییر یافت ---
    # این ورودی حالا فقط مقدار را در session_state ذخیره می‌کند.
    st.text_input(
        label='افزودن وظیفه جدید:', 
        placeholder="کار خود را وارد کنید",
        key="new_input", # کلید تغییر کرد
        label_visibility="collapsed"
    )

with col2:
    # --- تغییر کلیدی: دکمه تنها مرجع اجرای add_todo است ---
    st.button(
        "افزودن", 
        on_click=add_todo,
        key="add_button",
        use_container_width=True
    )
