import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Role Map",
    page_icon="🗺️",
    layout="wide"
)

# -----------------------------
# ROLE MAP: PAGE DESIGN
# -----------------------------

st.title("🗺️ Role Map")
st.subheader("Human-AI Responsibility Mapping Tool")

st.write(
    "Role Map helps organizations evaluate job tasks and determine "
    "whether work should be completed by AI, a human employee, "
    "or through shared responsibility."
)

st.info(
    "Prototype notice: This application uses fictional sample data "
    "and rule-based recommendations. Recommendations are not "
    "scientifically validated and require human review."
)

# -----------------------------
# SAMPLE JOB INFORMATION
# -----------------------------

if "job_title" not in st.session_state:
    st.session_state.job_title = "Customer Service Representative"

if "job_description" not in st.session_state:
    st.session_state.job_description = (
        "Supports customers by answering questions, resolving "
        "complaints, processing requests, and maintaining records."
    )

if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "Task": "Answer order-status questions",
            "Repetitiveness": 5,
            "Human Judgment": 2,
            "Human Interaction": 2,
            "Risk and Accountability": 2,
            "Human Oversight": 2
        },
        {
            "Task": "Tag and route incoming support tickets",
            "Repetitiveness": 5,
            "Human Judgment": 2,
            "Human Interaction": 1,
            "Risk and Accountability": 2,
            "Human Oversight": 2
        },
        {
            "Task": "Issue small refunds following written policy",
            "Repetitiveness": 4,
            "Human Judgment": 2,
            "Human Interaction": 1,
            "Risk and Accountability": 3,
            "Human Oversight": 3
        },
        {
            "Task": "Draft replies to common product questions",
            "Repetitiveness": 4,
            "Human Judgment": 3,
            "Human Interaction": 3,
            "Risk and Accountability": 2,
            "Human Oversight": 3
        },
        {
            "Task": "Summarize calls and chats into case records",
            "Repetitiveness": 4,
            "Human Judgment": 3,
            "Human Interaction": 2,
            "Risk and Accountability": 3,
            "Human Oversight": 3
        },
        {
            "Task": "Review suspicious account activity",
            "Repetitiveness": 2,
            "Human Judgment": 5,
            "Human Interaction": 2,
            "Risk and Accountability": 5,
            "Human Oversight": 5
        },
        {
            "Task": "Resolve upset customer complaints",
            "Repetitiveness": 2,
            "Human Judgment": 5,
            "Human Interaction": 5,
            "Risk and Accountability": 4,
            "Human Oversight": 4
        },
        {
            "Task": "Approve refunds over $500 and policy exceptions",
            "Repetitiveness": 2,
            "Human Judgment": 5,
            "Human Interaction": 2,
            "Risk and Accountability": 5,
            "Human Oversight": 5
        }
    ]

if "overrides" not in st.session_state:
    st.session_state.overrides = {}

if "reasons" not in st.session_state:
    st.session_state.reasons = {}

# -----------------------------
# RECOMMENDATION RULES
# -----------------------------

CATEGORIES = [
    "AI",
    "Human Employee",
    "Shared Responsibility"
]

def recommend(task):
    repetition = task["Repetitiveness"]
    judgment = task["Human Judgment"]
    interaction = task["Human Interaction"]
    risk = task["Risk and Accountability"]
    oversight = task["Human Oversight"]

    if risk >= 5 or judgment >= 5:
        return "Human Employee"

    if interaction >= 4:
        return "Human Employee"

    if (
        repetition >= 4
        and judgment <= 2
        and interaction <= 2
        and risk <= 2
    ):
        return "AI"

    return "Shared Responsibility"


def explanation(category):
    if category == "AI":
        return (
            "This task is repetitive and follows a predictable process. "
            "AI may help complete it efficiently, with monitoring "
            "and exception handling."
        )
    elif category == "Human Employee":
        return (
            "This task requires human judgment, interaction, "
            "or accountability. An employee should remain responsible."
        )
    else:
        return (
            "AI may assist with parts of this task, but an employee "
            "should review the work and remain accountable for the outcome."
        )

# -----------------------------
# JOB INFORMATION
# -----------------------------

st.header("1. Job Information")

st.session_state.job_title = st.text_input(
    "Job Title",
    value=st.session_state.job_title
)

st.session_state.job_description = st.text_area(
    "Job Description",
    value=st.session_state.job_description
)

# -----------------------------
# TASK MANAGEMENT
# -----------------------------

st.header("2. Task Analysis")

st.write(
    "Rate each task from 1 to 5. "
    "A rating of 1 means low and 5 means high."
)

st.caption(
    "Ratings represent prototype inputs, not validated assessment scales."
)

with st.expander("➕ Add a New Task"):
    with st.form("add_task_form"):
        new_task_name = st.text_input("Task Name")

        new_repetition = st.slider("Repetitiveness", 1, 5, 3)
        new_judgment = st.slider("Human Judgment", 1, 5, 3)
        new_interaction = st.slider("Human Interaction", 1, 5, 3)
        new_risk = st.slider("Risk and Accountability", 1, 5, 3)
        new_oversight = st.slider("Need for Human Oversight", 1, 5, 3)

        add_clicked = st.form_submit_button("Add Task")

        if add_clicked:
            if new_task_name.strip():
                st.session_state.tasks.append({
                    "Task": new_task_name.strip(),
                    "Repetitiveness": new_repetition,
                    "Human Judgment": new_judgment,
                    "Human Interaction": new_interaction,
                    "Risk and Accountability": new_risk,
                    "Human Oversight": new_oversight
                })
                st.success("Task added successfully!")
                st.rerun()
            else:
                st.warning("Please enter a task name.")

# -----------------------------
# EDIT AND REMOVE TASKS
# -----------------------------

for index, task in enumerate(st.session_state.tasks):
    with st.expander(f"Task {index + 1}: {task['Task']}"):
        with st.form(f"edit_task_{index}"):
            name = st.text_input(
                "Task Name",
                value=task["Task"],
                key=f"name_{index}"
            )

            repetition = st.slider(
                "Repetitiveness", 1, 5,
                task["Repetitiveness"],
                key=f"rep_{index}"
            )

            judgment = st.slider(
                "Human Judgment", 1, 5,
                task["Human Judgment"],
                key=f"jud_{index}"
            )

            interaction = st.slider(
                "Human Interaction", 1, 5,
                task["Human Interaction"],
                key=f"int_{index}"
            )

            risk = st.slider(
                "Risk and Accountability", 1, 5,
                task["Risk and Accountability"],
                key=f"risk_{index}"
            )

            oversight = st.slider(
                "Need for Human Oversight", 1, 5,
                task["Human Oversight"],
                key=f"over_{index}"
            )

            save = st.form_submit_button("Save Changes")

            if save:
                st.session_state.tasks[index] = {
                    "Task": name,
                    "Repetitiveness": repetition,
                    "Human Judgment": judgment,
                    "Human Interaction": interaction,
                    "Risk and Accountability": risk,
                    "Human Oversight": oversight
                }

                st.success("Task updated!")
                st.rerun()

        if st.button("Remove Task", key=f"remove_{index}"):
            st.session_state.tasks.pop(index)
            st.session_state.overrides.clear()
            st.session_state.reasons.clear()
            st.rerun()

# -----------------------------
# RECOMMENDATIONS
# -----------------------------

st.header("3. AI and Human Responsibility Recommendations")

if st.button("Generate Recommendations", type="primary"):
    st.session_state.recommendations_generated = True

if st.session_state.get("recommendations_generated", False):

    results = []

    for index, task in enumerate(st.session_state.tasks):
        original = recommend(task)

        if index not in st.session_state.overrides:
            st.session_state.overrides[index] = original

        results.append({
            "Task": task["Task"],
            "Original Recommendation": original,
            "Final Assignment": st.session_state.overrides[index],
            "Explanation": explanation(original)
        })

    for index, result in enumerate(results):
        st.divider()
        st.subheader(result["Task"])

        st.write(
            "**Original recommendation:** "
            + result["Original Recommendation"]
        )

        st.write(result["Explanation"])

        selected = st.selectbox(
            "Final Assignment — You may override the recommendation",
            CATEGORIES,
            index=CATEGORIES.index(result["Final Assignment"]),
            key=f"assignment_{index}"
        )

        st.session_state.overrides[index] = selected

        if selected != result["Original Recommendation"]:
            reason = st.text_input(
                "Reason for changing the recommendation",
                value=st.session_state.reasons.get(index, ""),
                key=f"reason_{index}"
            )
            st.session_state.reasons[index] = reason

        st.write("**Human oversight:**")
        if selected == "AI":
            st.write(
                "Monitor performance, review exceptions, and allow "
                "employees to escalate problems."
            )
        elif selected == "Shared Responsibility":
            st.write(
                "Require employee review before important actions "
                "and maintain clear accountability."
            )
        else:
            st.write(
                "Keep the employee responsible for decisions and "
                "provide appropriate organizational support."
            )

# -----------------------------
# FINAL SUMMARY
# -----------------------------

st.header("4. Final Role Map Summary")

if st.session_state.get("recommendations_generated", False):

    final_assignments = []

    for index, task in enumerate(st.session_state.tasks):
        original = recommend(task)
        final = st.session_state.overrides.get(index, original)

        final_assignments.append({
            "Task": task["Task"],
            "Original Recommendation": original,
            "Final Assignment": final
        })

    df = pd.DataFrame(final_assignments)

    col1, col2, col3 = st.columns(3)

    counts = df["Final Assignment"].value_counts()

    col1.metric("AI Tasks", counts.get("AI", 0))
    col2.metric(
        "Human Employee Tasks",
        counts.get("Human Employee", 0)
    )
    col3.metric(
        "Shared Responsibility Tasks",
        counts.get("Shared Responsibility", 0)
    )

    st.subheader("Task-by-Task Assignments")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Important Oversight Considerations")

    st.write(
        "- Employees should have opportunities to provide input."
    )
    st.write(
        "- Managers and stakeholders should review proposed assignments."
    )
    st.write(
        "- Human override and escalation options should remain available."
    )
    st.write(
        "- Organizations should monitor errors, workload, and employee feedback."
    )
    st.write(
        "- Responsibility should be clearly assigned before implementation."
    )

    st.warning(
        "These results are draft recommendations, not approved "
        "organizational decisions. All assignments require human review."
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Role Map Summary",
        data=csv,
        file_name="role_map_summary.csv",
        mime="text/csv"
    )

else:
    st.info(
        "Generate recommendations above to view your final Role Map summary."
    )

# -----------------------------
# PRIVACY NOTICE
# -----------------------------

st.divider()

st.caption(
    "Privacy: This prototype uses fictional sample information. "
    "Do not enter confidential employee, customer, or organizational data. "
    "This version does not connect to external AI services or databases."
)
