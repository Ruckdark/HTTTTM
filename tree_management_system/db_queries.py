import pandas as pd

def get_trees(engine):
    query = """
    SELECT Tree.TreeId, Species.SpeciesId , Species.SpeciesName AS Species, Tree.Age, 
           Tree.Height / 100.0 AS Height, Tree.Diameter / 100.0 AS Diameter,
           Tree.HealthStatus, Tree.Note, Tree.Location, Tree.ReminderDate 
    FROM Tree
    JOIN Species ON Tree.Species = Species.SpeciesId
    """
    df = pd.read_sql_query(query, engine)
    return df

def add_tree(engine, species, age, height_cm, diameter_cm, health_status, note, location, reminder_date):
    query = "INSERT INTO Tree (Species, Age, Height, Diameter, HealthStatus, Note, Location, ReminderDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    with engine.connect() as conn:
        conn.execute(query, (species, age, height_cm, diameter_cm, health_status, note, location, reminder_date))

def update_tree(engine, tree_id, species, age, height_cm, diameter_cm, health_status, note, location, reminder_date):
    query = "UPDATE Tree SET Species = ?, Age = ?, Height = ?, Diameter = ?, HealthStatus = ?, Note = ?, Location = ?, ReminderDate = ? WHERE TreeId = ?"
    with engine.connect() as conn:
        conn.execute(query, (species, age, height_cm, diameter_cm, health_status, note, location, reminder_date, tree_id))

def delete_tree(engine, tree_id):
    query = "DELETE FROM Tree WHERE TreeId = ?"
    with engine.connect() as conn:
        conn.execute(query, (tree_id))

def get_species(engine):
    query = "SELECT SpeciesId, SpeciesName FROM Species"
    df = pd.read_sql_query(query, engine)
    return df

