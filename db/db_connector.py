import pandas as pd
import requests
from sqlalchemy import text


def insert_idea(db, title, name_owner, email, r_d, tl, project_description, keywords, needs, type_of_collaboration, notes, poc):
    """
    Inserts data into the ideas_register table securely using parameterized queries.
    
    :param db: Database connection engine
    :param title: Title of the idea
    :param name_owner: Name of the owner
    :param email: Email of the owner
    :param r_d: Research & Development category
    :param tl: Technology Level
    :param project_description: Description of the project
    :param keywords: Keywords related to the project
    :param needs: Project needs
    :param type_of_collaboration: Type of collaboration required
    :param notes: Additional notes
    :param poc: Point of contact
    """
    query = text("""
        INSERT INTO ideas_register 
        (title, name_owner, email, r_d, tl, project_description, keywords, needs, type_of_collaboration, notes, poc) 
        VALUES 
        (:title, :name_owner, :email, :r_d, :tl, :project_description, :keywords, :needs, :type_of_collaboration, :notes, :poc);
    """)

    with db.connect() as conn:
        conn.execute(query, {
            'title': title,
            'name_owner': name_owner,
            'email': email,
            'r_d': r_d,
            'tl': tl,
            'project_description': project_description,
            'keywords': keywords,
            'needs': needs,
            'type_of_collaboration': type_of_collaboration,
            'notes': notes,
            'poc': poc
        })
        conn.commit()

def insert_expression_of_interest(db, name_interest, email, r_d, collaborations, title):
    """
    Inserts data into the expression_interest table securely using parameterized queries.
    
    :param db: Database connection engine
    :param name_interest: Name of the person expressing interest
    :param email: Email of the person
    :param r_d: Research & Development category
    :param collaborations: Desired collaborations
    """
    query = text("""
        INSERT INTO expression_interest 
        (name_interest, email, r_d, collaborations, title) 
        VALUES 
        (:name_interest, :email, :r_d, :collaborations, :title);
    """)

    with db.connect() as conn:
        conn.execute(query, {
            'name_interest': name_interest,
            'email': email,
            'r_d': r_d,
            'collaborations': collaborations,
            'title': title
        })
        conn.commit()

def fetch_ideas(db):
    query = text("SELECT * FROM ideas_register ORDER BY date_created DESC;")

    with db.connect() as conn:
        result = conn.execute(query)
        columns = result.keys()
        data = result.fetchall()
    return pd.DataFrame(data, columns=columns)

def fetch_interest(db, title):
    query = text(f"SELECT name_interest, email, r_d, collaborations FROM expression_interest WHERE title LIKE \'{title}\';")

    with db.connect() as conn:
        result = conn.execute(query)
        columns = result.keys()
        data = result.fetchall()
    return pd.DataFrame(data, columns=columns)

def get_ideas_title(db):
    with db.connect() as conn:
        result = conn.execute(text('SELECT DISTINCT title FROM ideas_register'))
        return [row[0] for row in result]