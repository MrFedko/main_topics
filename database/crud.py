import sqlite3


class Database:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.scheme_tables = {
            "topics": ("restaurant", "topic", "question", "answer", "restrictions", "url", "date_control", "responsible_position", "responsible_name",
                       "approval_is_required", "approval_position", "approval_contact", "approval_period", "next_approve", "answer_status", "notes"),
        }

    def execute(self, query: str, params: tuple = (), fetchone=False, fetchall=False):
        with self.connection:
            cursor = self.connection.execute(query, params)
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()

    def create_table_topics(self):
        self.execute("""CREATE TABLE topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restaurant TEXT,
    topic TEXT,
    question TEXT,
    answer TEXT,
    restrictions TEXT,
    url TEXT,
    date_control TEXT,
    responsible_position TEXT,
    responsible_name TEXT,
    approval_is_required TEXT,
    approval_position TEXT,
    approval_contact TEXT,
    approval_period TEXT,
    next_approve TEXT,
    answer_status TEXT,
    notes TEXT
);""")

    def create_topics_ids_table(self):
        self.execute("""CREATE TABLE topics_ids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT
);""")


    def insert_row(self, table: str, row: list):
        row = [x.strip() if isinstance(x, str) else x for x in row][1:]  # Remove the first element (id) and strip whitespace from strings
        placeholders = ', '.join(['?'] * len(row))
        table_names = self.scheme_tables[table]
        query = f"INSERT INTO {table} {table_names} VALUES ({placeholders})"
        self.execute(query, tuple(row))

    def upload_topics_ids(self, topics):
        for topic in topics:
            self.execute("INSERT INTO topics_ids (topic) VALUES (?)", (topic,))

    def clean_all_values(self):
        for table in self.scheme_tables.keys():
            self.execute(f"DELETE FROM {table}")

    def get_restaurants(self, table: str):
        query = f"SELECT DISTINCT restaurant FROM {table}"
        result = self.execute(query, fetchall=True)
        return [row["restaurant"] for row in result]

    def get_topics_by_restaurant(self, restaurant: str):
        query = f"SELECT DISTINCT topic FROM topics WHERE restaurant = ?"
        result = self.execute(query, params=(restaurant, ), fetchall=True)
        return [row["topic"] for row in result]

    def get_topic_id_by_name(self, topic: str):
        query = f"SELECT id FROM topics_ids WHERE topic = ?"
        result = self.execute(query, params=(topic,), fetchone=True)
        return result["id"] if result else None

    def get_topic_name_by_id(self, topic_id: int):
        query = f"SELECT topic FROM topics_ids WHERE id = ?"
        result = self.execute(query, params=(topic_id,), fetchone=True)
        return result["topic"] if result else None

    def get_all_topics(self, table: str):
        query = f"SELECT DISTINCT topic FROM {table}"
        result = self.execute(query, fetchall=True)
        return [row["topic"] for row in result]

    def get_questions(self, restaurant: str, topic: str):
        query = f"SELECT id, question FROM topics WHERE restaurant = ? AND topic = ?"
        result = self.execute(query, params=(restaurant, topic), fetchall=True)
        return [(row["id"], row["question"]) for row in result]

    def get_answer_by_id(self, question_id: int):
        query = f"""SELECT restaurant, topic, question, answer, restrictions, url, date_control, 
        responsible_position, responsible_name, approval_is_required, approval_position, approval_contact, 
        approval_period, next_approve, answer_status, notes FROM topics WHERE id = ?"""
        result = self.execute(query, params=(question_id,), fetchone=True)
        return result if result else None


# def main():
#     db = Database("../topics.db")
#     all_topics = db.get_all_topics("topics")
#     db.upload_topics_ids(all_topics)
#
#
# if __name__ == "__main__":
#     main()
