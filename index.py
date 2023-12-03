from http_requests import requestsAPI
from time import sleep
from mysql_db import sqlOperations, sqlPoolOpen

def main():
    try:
        with sqlPoolOpen.get_connection() as connection:
            with connection.cursor() as cursor:
                while True:
                    data = requestsAPI.get_initial_fetch()
                    entries = data['entries']
                    continue_fetch_loop = data['truncated']
                    last_time = entries[-1]['time']
                    last_id = entries[-1]['id']

                    highest_id = sqlOperations.get_highest_id(cursor)
                    continue_fetch_loop = sqlOperations.add_entries(entries, highest_id, cursor)

                    while continue_fetch_loop:
                        data = requestsAPI.get_further_fetch(last_time, last_id)
                        entries = data['entries']
                        last_time = entries[-1]['time']
                        last_id = entries[-1]['id']
                        continue_fetch_loop = sqlOperations.add_entries(entries, highest_id, cursor)
                        if not data['truncated']:
                            break
                        sleep(1)

                    connection.commit()
                    print('Finish fetch & dump, retrying in 60 seconds')
                    sleep(60)

    except KeyboardInterrupt:
        print('Program interrupted by user. Cleaning up...')
    finally:
        connection.commit()
        cursor.close()
        sqlPoolOpen.release_connection(connection)
        print("SQL pool closed and connection released")

if __name__ == "__main__":
    main()