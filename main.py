import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to create the daily tracker
def daily_tracker():
    st.title("Daily Task Tracker")

    # Create empty list to store tasks
    tasks_list = []

    time_slots = pd.date_range(start="2024-03-30 00:00", end="2024-03-30 23:59", freq="3h")
    time_slots = [(time.strftime("%I:%M %p"), (time + pd.Timedelta(hours=3)).strftime("%I:%M %p")) for time in time_slots]

    for start_time, end_time in time_slots:
        task_assigned = st.text_input(f"{start_time} to {end_time}:", key=start_time)
        if task_assigned:
            tasks_list.append({"Time Slot": f"{start_time} to {end_time}", "Task Assigned": task_assigned, "Completed": False})

    # Create DataFrame from tasks list
    tasks_df = pd.DataFrame(tasks_list)

    # Display tasks dataframe with checkboxes if it's not empty
    if not tasks_df.empty:
        st.write("## Tasks for the Day")
        for index, row in tasks_df.iterrows():
            task_completed = st.checkbox(f"{row['Time Slot']} - {row['Task Assigned']}", key=index, value=row.get('Completed', False))
            tasks_df.at[index, 'Completed'] = task_completed

        # Calculate task completion percentage
        total_tasks = len(tasks_df)
        completed_tasks = tasks_df["Completed"].sum()
        tasks_remaining = total_tasks - completed_tasks
        completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        # Display task completion information
        st.write(f"## Task Completion Information")
        st.write(f"Total Tasks: {total_tasks}")
        st.write(f"Tasks Completed: {completed_tasks}")
        st.write(f"Tasks Remaining: {tasks_remaining}")
        st.write(f"Completion Percentage: {completion_percentage:.2f}%")

        # Plot task completion chart with custom colors
        fig, ax = plt.subplots(figsize=(6, 1))
        colors = ['#25e014', '#e0142c']
        ax.barh(['Completed', 'Remaining'], [completed_tasks, tasks_remaining], color=colors)
        ax.set_xlabel('Number of Tasks')
        ax.set_title('Task Completion Chart')
        fig.set_facecolor('black')
        ax.set_facecolor('black')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['top'].set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(10)  
        st.pyplot(fig)
    else:
        st.write("No tasks added for the day.")


# Main function
def main():
    daily_tracker()


if __name__ == "__main__":
    main()
