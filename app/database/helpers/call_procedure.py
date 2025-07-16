from app.database.connection.cursor import db_cursor


def call_procedure(proc_name, args=None, dictionary=False):
    if args is not None and not isinstance(args, (tuple, list)):
        raise ValueError(f"Procedure args must be tuple or list, got {type(args)}")
    
    args = args or ()
    with db_cursor(dictionary=dictionary) as cursor:
        cursor.callproc(proc_name, args)
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        return results if results else None