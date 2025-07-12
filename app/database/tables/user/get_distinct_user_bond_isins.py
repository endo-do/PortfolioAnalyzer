from app.database.helpers.call_procedure import call_procedure

def get_distinct_user_bond_isins(userid):
    rows = call_procedure("get_user_distinct_bond_isins", (userid,))
    return {row[0]: row[1] for row in rows}
