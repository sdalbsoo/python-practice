def create_table(con_db):
    cursor = con_db.cursor()
    with open("./schema.sql", "r") as f:
        stripped_lines = [s.rstrip() for s in f.readlines()]
        for command_line in stripped_lines:
            cursor.execute(command_line)


def insert_words_table(con_db, word, meanings):
    cursor = con_db.cursor()
    cursor.execute("USE cheese_project")
    meaning = ", ".join(meanings)
    sql = """INSERT INTO words(word, meaning) SELECT %s, %s FROM dual\
    WHERE NOT EXISTS (SELECT * FROM words where word=%s);"""
    val = (word, meaning, word)
    cursor.execute(sql, val)
    con_db.commit()


def insert_ratio_table(con_db, percent, words):
    cursor = con_db.cursor()
    cursor.execute("USE cheese_project")
    sql = """INSERT INTO subtitle(percent, count_words)\
    VALUES(%s, %s)"""
    val = (percent, words)
    cursor.execute(sql, val)
    con_db.commit()


def search_exiting_dict(con_db, word):
    cursor = con_db.cursor()
    cursor.execute("USE cheese_project")
    sql = "SELECT word, meaning FROM words WHERE word=%s"
    val = (word)
    cursor.execute(sql, val)
    result_word = cursor.fetchone()
    return result_word
