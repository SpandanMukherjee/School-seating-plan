import mysql.connector
import getpass

try:
    password = getpass.getpass("Enter password: ")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="School_seating_plan"
    )

    cursor = conn.cursor()

    if conn.is_connected():
        print("Successfully connected to the database")

    cursor.execute("""

            CREATE TABLE IF NOT EXISTS extra_classes(
                class VARCHAR(5) NOT NULL,
                section VARCHAR(5) NOT NULL,
                boys INT,
                girls INT,
                total INT NOT NULL,
                PRIMARY KEY (class, section)
            );
                   
    """)

    cursor.execute("TRUNCATE TABLE extra_classes")
    exam_date = input("Enter exam date (YYYY-MM-DD): ")

    def get_classes_on_date(cursor):
        cursor.execute("SELECT * FROM exam_fixture WHERE exam_date = %s", (exam_date,))
        result = cursor.fetchone()

        if not result:
            print("No exam scheduled on this date.")
            return {}
        
        class_columns = ["VI", "VII", "VIII", "IX", "X", "XI", "XII"]
        classes_with_exam = {}

        for i in range(1, len(result)):
            subject = result[i]

            if subject and subject.upper() != "NULL":
                class_name = class_columns[i - 1]
                classes_with_exam[class_name] = subject

        return classes_with_exam

    def get_total(section):
        return section[4]

    def combine_small_sections(sections, min_size=30):
        combined = []
        temp = []
        total = 0
        sorted_sections = sorted(sections, key=get_total)

        for sec in sorted_sections:

            if sec[4] >= min_size:
                combined.append(sec)
            else:
                temp.append(sec)
                total += sec[4]
                
                if total >= min_size:
                    class_ = temp[0][0]
                    sections_str = ""
                    idx = 0

                    while idx < len(temp):

                        if idx == 0:
                            sections_str = temp[idx][1]
                        else:
                            sections_str = sections_str + "+" + temp[idx][1]

                        idx += 1

                    boys = 0
                    girls = 0
                    tot = 0

                    for s in temp:
                        boys += s[2]
                        girls += s[3]
                        tot += s[4]

                    combined.append((class_, sections_str, boys, girls, tot))
                    temp = []
                    total = 0

        for s in temp:
            combined.append(s)

        return combined

    def pair_sections_by_total(sections1, sections2, target=80):
        pairs = []
        leftovers1 = []
        leftovers2 = []
        s1 = sections1[:]
        s2 = sections2[:]
        s1.sort(key=get_total, reverse=True)
        s2.sort(key=get_total, reverse=True)

        while s1 and s2:
            sec1 = s1[0]
            best_idx = 0
            best_diff = abs(sec1[4] + s2[0][4] - target)
            i = 1

            while i < len(s2):
                diff = abs(sec1[4] + s2[i][4] - target)

                if diff < best_diff:
                    best_diff = diff
                    best_idx = i

                i += 1

            sec2 = s2[best_idx]
            pairs.append((sec1, sec2))
            s1.pop(0)
            s2.pop(best_idx)

        for sec in s1:
            leftovers1.append(sec)
        for sec in s2:
            leftovers2.append(sec)

        leftovers = leftovers1 + leftovers2
        return pairs, leftovers

    def pair_classes(cursor):
        classes_with_exam = get_classes_on_date(cursor)

        if not classes_with_exam:
            print("No exams today. Exiting program")
            return [], []

        class_data = {}

        for class_name in classes_with_exam:
            cursor.execute("SELECT * FROM classes WHERE class = %s", (class_name,))
            sections = cursor.fetchall()
            class_data[class_name] = sections

        preferred_pairs = [("VI", "IX"), ("VIII", "XI"), ("X", "XII")]
        paired_sections = []
        leftovers = []
        present = set(class_data.keys())
        singles = []
        used = set()

        for a, b in preferred_pairs:

            if a in present and b in present:
                sec_a = combine_small_sections(class_data[a])
                sec_b = combine_small_sections(class_data[b])
                pairs, leftover_secs = pair_sections_by_total(sec_a, sec_b)
                paired_sections.extend(pairs)
                leftovers.extend(leftover_secs)
                used.add(a)
                used.add(b)
            elif a in present and b not in present:
                singles.append(a)
                used.add(a)
            elif b in present and a not in present:
                singles.append(b)
                used.add(b)

        if "VII" in present and "VII" not in used:
            singles.append("VII")
            used.add("VII")

        lower = []
        upper = []

        for c in singles:

            if c in ("VI", "VII", "VIII"):
                lower.append(c)
            else:
                upper.append(c)

        singles_pairs = []

        while lower and upper:
            a = lower.pop(0)
            b = upper.pop(0)
            singles_pairs.append((a, b))
            used.add(a)
            used.add(b)
        while len(lower) >= 2:
            a = lower.pop(0)
            b = lower.pop(0)
            singles_pairs.append((a, b))
            used.add(a)
            used.add(b)
        while len(upper) >= 2:
            a = upper.pop(0)
            b = upper.pop(0)
            singles_pairs.append((a, b))
            used.add(a)
            used.add(b)

        leftovers_classes = lower + upper

        for a, b in singles_pairs:
            sec_a = combine_small_sections(class_data[a])
            sec_b = combine_small_sections(class_data[b])
            pairs, leftover_secs = pair_sections_by_total(sec_a, sec_b)
            paired_sections.extend(pairs)
            leftovers.extend(leftover_secs)

        for cls in leftovers_classes:

            for section in class_data.get(cls, []):
                leftovers.append(section)

        for section_tuple in leftovers:
            cursor.execute(
                "INSERT INTO extra_classes (class, section, boys, girls, total) VALUES (%s, %s, %s, %s, %s)",
                section_tuple
            )

        conn.commit()
        return paired_sections, leftovers
    
    pairs, leftovers = pair_classes(cursor)
    print("Pairs:", pairs)
    print("Leftovers:", leftovers)

    cursor.close()
    conn.close()
    print("Successful completion of all required tasks")

except Exception as e:
    print("Error while connecting to database:", e)