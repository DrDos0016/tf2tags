""" I am not even sure if this is used? The database library is very old here. """

import MySQLdb as mdb

con = mdb.connect('localhost', 'tf2tags', 'TODO: PUT YOUR DATABASE PASSWORD HERE', 'tf2tags');
cur = con.cursor(mdb.cursors.DictCursor)
cur.execute("SELECT s.user_id, SUM(s.score) as total_score, u.maxSubmitted FROM `tf2tags_submissions` s LEFT JOIN `tf2tags_users` u ON s.user_id = u.id WHERE (u.maxSubmitted < 25) GROUP BY s.user_id HAVING total_score >= 99 ORDER BY total_score DESC")
rows = cur.fetchall()

for row in rows:
    if row["total_score"] >= 500:
        new_max = "25"
        new_comments = "50"
    else:
        new_max = "10"
        new_comments = "20"
    query = "UPDATE `tf2tags_users` SET maxSubmitted = "+new_max+", max_posted_comments = "+new_comments+" WHERE id = " + str(row["user_id"]) + ";"
    cur.execute(query)
    print("Set user #", row["user_id"], " to have "+new_max+" max submissions and " + new_comments + " max comments.")
con.commit()
print("Max Submissions updated.")
con.close()
