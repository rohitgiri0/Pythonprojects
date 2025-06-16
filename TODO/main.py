import streamlit as st
import json

def load_file():
    try:
        with open ("tasks.txt", "r")as f:
            return json.load(f)
    except (FileNotFoundError,ValueError,json.JSONDecodeError):
        return []
    
def save_data(tasks):
    with open("tasks.txt","w") as f:
        return json.dump(tasks,f)
    
def show_task(tasks):
    if not tasks:
        st.write("there are no tasks")
        return
    for index,task in enumerate(tasks,start=1):
        st.checkbox(f"{index}. {task.get('task','unknown')}")

def add_task(tasks):
    task=st.text_input("Enter task here",placeholder="ex. study for 2 hours",key="new_task")
    if st.button("Save task",key="save_task_button"):
        if task.strip():
            tasks.append({"task": task})
            save_data(tasks)
            st.success("task added ✅")
        else:
            st.warning("please enter a task and then press the save button!")
        
def delete_task(indecies):
    tasks=load_file()
    for index in sorted(indecies,reverse=True):
        del tasks[index-1]
    save_data(tasks)

    
def main():
    tasks=load_file()
    st.title("TODO")
    st.subheader("app made by Rohit")
    col1,col2,col3=st.columns(3)
    with col1:
        if "show_input" not in st.session_state:
            st.session_state.show_input=False
        
        if st.button("Add Task",type="primary"):
            st.session_state.show_input=True
        
        if st.session_state.show_input:
            add_task(tasks)
            
            
        
    with col2: 
        if st.toggle("show task"):
            show_task(tasks)
            
    with col3: 
        selected_index=st.multiselect("select the indeces you like to delete",[i for i in range(1,len(tasks)+1)])
        if st.button("Delete selected tasks"):
            delete_task(selected_index)
    
if __name__ == "__main__":
    main()
