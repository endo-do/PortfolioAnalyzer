from app.database.helpers.execute_change_query import execute_change_query

def insert_default_bondcategories():
    categories = ['ETF', 'Share', 'Mutual Fund', 'Government Fund', 'Other']
    
    for category in categories:
        execute_change_query(
            "INSERT INTO bondcategory (bondcategoryname) VALUES (%s)",
            (category,)
        )
    
    print(f"    ✅ Bond categories inserted successfully")