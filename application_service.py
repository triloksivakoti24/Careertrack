from database.db import get_connection

STATUSES = [
    "Applied",
    "Interview",
    "Selected",
    "Rejected",
]


def add_application(
    company,
    role,
    location,
    application_date,
    job_link,
    status,
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO applications
            (
                company,
                role,
                location,
                application_date,
                job_link,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                company,
                role,
                location,
                application_date,
                job_link,
                status,
            ),
        )
        connection.commit()


def get_applications():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM applications
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def update_application_status(application_id, status):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE applications
            SET status = ?
            WHERE id = ?
            """,
            (status, application_id),
        )
        connection.commit()


def delete_application(application_id):
    with get_connection() as connection:
        connection.execute(
            """
            DELETE FROM applications
            WHERE id = ?
            """,
            (application_id,),
        )
        connection.commit()


def get_statistics():
    applications = get_applications()

    statistics = {
        "Total": len(applications),
        "Applied": 0,
        "Interview": 0,
        "Selected": 0,
        "Rejected": 0,
    }

    for application in applications:
        status = application.get("status")

        if status in statistics:
            statistics[status] += 1

    return statistics