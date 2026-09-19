import streamlit as st

from services.application_service import (
    add_application,
    get_applications,
    update_application_status,
    delete_application,
    get_statistics,
)


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="CareerTrack",
    page_icon="💼",
    layout="wide",
)


# -----------------------------
# Application Constants
# -----------------------------
STATUSES = [
    "Applied",
    "Interview",
    "Selected",
    "Rejected",
]


# -----------------------------
# Page Header
# -----------------------------
st.title("💼 CareerTrack")
st.caption("Job Application Tracker")


# -----------------------------
# Sidebar Navigation
# -----------------------------
menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Application",
        "Manage Applications",
    ],
)


# =====================================================
# DASHBOARD
# =====================================================
if menu == "Dashboard":

    stats = get_statistics()

    cols = st.columns(5)

    labels = [
        "Total",
        "Applied",
        "Interview",
        "Selected",
        "Rejected",
    ]

    for col, label in zip(cols, labels):
        col.metric(
            label,
            stats.get(label, 0),
        )

    st.divider()

    applications = get_applications()

    if applications:
        st.subheader("Recent Applications")

        st.dataframe(
            applications,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.info("No applications added yet.")


# =====================================================
# ADD APPLICATION
# =====================================================
elif menu == "Add Application":

    st.header("➕ Add Job Application")

    with st.form("application_form"):

        company = st.text_input(
            "Company Name",
            placeholder="Example: Google",
        )

        role = st.text_input(
            "Job Role",
            placeholder="Example: Python Developer",
        )

        location = st.text_input(
            "Location",
            placeholder="Example: Hyderabad / Remote",
        )

        application_date = st.date_input(
            "Application Date",
        )

        job_link = st.text_input(
            "Job Link",
            placeholder="https://example.com/job",
        )

        status = st.selectbox(
            "Status",
            STATUSES,
        )

        submitted = st.form_submit_button(
            "💾 Save Application",
            use_container_width=True,
        )

        if submitted:

            if not company.strip():
                st.error("Company name is required.")

            elif not role.strip():
                st.error("Job role is required.")

            else:

                add_application(
                    company.strip(),
                    role.strip(),
                    location.strip(),
                    str(application_date),
                    job_link.strip(),
                    status,
                )

                st.success(
                    "✅ Application added successfully!"
                )

                st.rerun()


# =====================================================
# MANAGE APPLICATIONS
# =====================================================
elif menu == "Manage Applications":

    st.header("📝 Manage Applications")

    applications = get_applications()

    if not applications:

        st.info("No applications available.")

    else:

        for application in applications:

            app_id = application["id"]

            company = application["company"]
            role = application["role"]

            with st.expander(
                f"💼 {company} — {role}"
            ):

                st.write(
                    f"**Location:** "
                    f"{application.get('location') or 'Not specified'}"
                )

                st.write(
                    f"**Application Date:** "
                    f"{application['application_date']}"
                )

                job_link = application.get("job_link")

                if job_link:
                    st.markdown(
                        f"**Job Link:** [{job_link}]({job_link})"
                    )
                else:
                    st.write("**Job Link:** Not provided")

                current_status = application["status"]

                if current_status in STATUSES:
                    current_index = STATUSES.index(
                        current_status
                    )
                else:
                    current_index = 0

                new_status = st.selectbox(
                    "Update Status",
                    STATUSES,
                    index=current_index,
                    key=f"status_{app_id}",
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "🔄 Update Status",
                        key=f"update_{app_id}",
                        use_container_width=True,
                    ):

                        update_application_status(
                            app_id,
                            new_status,
                        )

                        st.success(
                            "✅ Status updated successfully!"
                        )

                        st.rerun()

                with col2:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{app_id}",
                        use_container_width=True,
                    ):

                        delete_application(app_id)

                        st.success(
                            "🗑️ Application deleted successfully!"
                        )

                        st.rerun()
