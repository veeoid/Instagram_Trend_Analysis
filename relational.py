import psycopg2

conn = psycopg2.connect("dbname=big_data_project user=postgres password=RITPostGreSQL")
cur = conn.cursor()
cur.execute(
    "drop table if exists l1_test; CREATE TABLE L1_test AS SELECT DISTINCT(p.location_id), COUNT(p.profile_id) AS freq FROM final.tempposts p GROUP BY p.location_id HAVING COUNT(p.profile_id)>=50;")

prev_level_table = "L1_test"
level = 2
num_frequent_itemsets = 1
last_frequency = float('inf')
iter = 2
while num_frequent_itemsets > 0:
    current_level_table = f"L{level}"
    sql = f"CREATE TABLE {current_level_table} AS SELECT "
    for i in range(1, level + 1):
        sql += f"p{i}.location_id AS location{i}, "
    sql += f"COUNT(DISTINCT p1.profile_id) AS count FROM final.tempposts p1 "
    for i in range(2, level + 1):
        join_cond = ""
        for j in range(1, i):
            s = f"JOIN final.tempposts p{i}"
            if s not in sql:
                join_cond += f"JOIN final.tempposts p{i} ON p{j}.profile_id = p{i}.profile_id AND p{i-1}.location_id < p{i}.location_id "
                sql += join_cond
    if prev_level_table == 'L1_test':
        sql += f"JOIN {prev_level_table} ON {prev_level_table}.location_id = p1.location_id "
    else:
        sql += f"JOIN {prev_level_table} ON {prev_level_table}.location1 = p1.location_id "
    for i in range(2, level):
        if prev_level_table == 'L1_test':
            sql += f"OR {prev_level_table}.location_id = p1.location_id "
        else:
            sql += f"OR {prev_level_table}.location{i} = p{i}.location_id "
    sql += f"GROUP BY "
    for i in range(1, level + 1):
        sql += f"p{i}.location_id, "
    sql = sql[:-2] + f" HAVING COUNT(DISTINCT p1.profile_id) >= 50;"
    print(sql)
    cur.execute("drop table if exists "+current_level_table)
    cur.execute(sql)
    num_frequent_itemsets = cur.rowcount

    print(f"Number of frequent itemsets in {current_level_table}: {num_frequent_itemsets}")

    level += 1

conn.commit()
cur.close()

conn.close()

