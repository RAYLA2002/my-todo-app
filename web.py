import streamlit as st
import functions

st.set_page_config(layout="centered", page_title="My To-Do App")

todos = functions.get_todos()

def add_todo():
    new_todo_item = st.session_state.get("new_todo")
    if new_todo_item:
        todos.append(new_todo_item.strip() + "\n")
        functions.write_todos(todos)
        st.session_state["new_todo"] = ""

def complete_todo(todo_text_to_remove):
    try:
        item_to_remove = todo_text_to_remove.strip() + "\n"
        todos.remove(item_to_remove)
        functions.write_todos(todos)
        st.rerun() 
    except ValueError:
        st.error(f"Error removing: '{todo_text_to_remove.strip()}' not found.")

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

st.title("🎯 اپلیکیشن مدیریت وظایف من")
st.markdown("### **:blue[بهره‌وری خود را افزایش دهید!]**")
st.write("وظایف خود را با نظم و ترتیب مدیریت کنید. برای تکمیل شدن یک وظیفه، تیک آن را بزنید.")

st.divider()

if not todos:
    st.info("🎉 لیست وظایف شما خالی است! یک کار جدید اضافه کنید.")

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
    st.text_input(
        label='افزودن وظیفه جدید:', 
        placeholder="مثلاً: مستندسازی پروژه را تمام کنم...",
        on_change=add_todo,
        key="new_todo",
        label_visibility="collapsed"
    )

with col2:
    st.button(
        "➕ افزودن", 
        on_click=add_todo,
        key="add_button",
        use_container_width=True
    )
