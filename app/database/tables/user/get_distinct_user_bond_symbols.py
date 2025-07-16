from app.database.helpers.call_procedure import call_procedure

def get_distinct_user_bond_symbols(userid):
    rows = call_procedure("get_user_distinct_bond_symbols", (userid,))
    return {row[0]: row[1] for row in rows}
