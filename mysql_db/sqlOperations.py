table_name = 'raw_stash_dump'

def get_highest_id(cursor):
    cursor.execute(f"SELECT MAX(id) FROM {table_name}")
    result = cursor.fetchall()
    return result[0][0]

def get_inventory_history(cursor):
    cursor.execute("SELECT * FROM `inventory_history`")
    result = cursor.fetchall()
    return result


def add_entries(entries, highest_id, cursor):
    for entry in entries:
        if highest_id is not None and int(entry['id']) <= highest_id:
            return False
        insert_query = f"""
        INSERT INTO raw_stash_dump (id, time, league, stash, item, action, account_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            int(entry['id']),
            int(entry['time']),
            entry['league'],
            entry['stash'],
            entry['item'],
            entry['action'],
            entry['account']['name'],
        )
        cursor.execute(insert_query, values)
    return True