def pdf_gen():
    from datetime import datetime
    import random
    import os
    from reportlab.pdfgen import canvas

    folder = "seating_plans"
    institution_name = "BHAVAN'S GANGABUX KANORIA VIDYAMANDIR"
    os.makedirs("PDFs", exist_ok=True)

    def parse_rollpairs(line):
        pairs = [p.strip() for p in line.replace("(", "").replace(")", "").split(",") if p.strip()]
        result = []

        for pair in pairs:

            try:
                nums = list(map(int, pair.split("+")))

                if len(nums) == 2:
                    result.append(nums)

            except ValueError:
                continue

        return result

    def add_room_page(c, class1 = "Undefined", class2 = "Undefined", room_number = "Undefined", starts = [], rolls = []):

        def gen_spaces(n):
            return random.sample([0, 1, 2, 3, 4], n)

        c.setFont("Helvetica-Bold", 20)
        text_width = c.stringWidth(institution_name, "Helvetica-Bold", 20)
        c.drawString((600 - text_width)/2, 360, institution_name)
        room_text = f"Room Number : {room_number}"
        c.setFont("Helvetica-Bold", 12)
        room_text_width = c.stringWidth(room_text, "Helvetica-Bold", 12)
        c.drawString(580 - room_text_width, 328, room_text)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20, 328, f"Class 1 (Left) : {class1}")
        c.drawString(20, 312, f"Class 2 (Right) : {class2}")
        c.setFont('Helvetica', 12)
        srt1, srt2 = starts[0] + rolls[0][0] - 1, starts[1] + rolls[0][1] - 1

        for i in range(5):
            columnroll = rolls[i]
            leftseats, rightseats = gen_spaces(columnroll[0]), gen_spaces(columnroll[1])

            for j in range(5):
                x0 = 20 + i * 118
                y0 = 60 + j * 48
                c.rect(x0, y0, 85, 48)

                if j in leftseats:
                    c.drawString(x0 + 15, y0 + 20, str(srt1))
                    srt1 -= 1
                if j in rightseats:
                    c.drawString(x0 + 57.5, y0 + 20, str(srt2))
                    srt2 -= 1

                for k in range(1, 2):
                    x_sub = x0 + k * 42.5
                    c.line(x_sub, y0, x_sub, y0 + 48)

            if i < 4:
                srt1 += rolls[i][0] + rolls[i+1][0]
                srt2 += rolls[i][1] + rolls[i+1][1]

        c.setFont("Helvetica", 10)
        date_text = "Generated on Date: " + datetime.now().strftime("%Y-%m-%d")
        signature_text = "Signature:"
        c.drawString(20, 24, signature_text)
        c.drawString(20, 40, date_text)
        c.showPage()

    def gen_cumulative_chart(c, dict):
        c.setFont("Helvetica-Bold", 20)
        text_width = c.stringWidth(institution_name, "Helvetica-Bold", 20)
        c.drawString((600 - text_width)/2, 960, institution_name)
        c.setFont("Helvetica", 12)
        j = 880
        x = 557

        for key in list(dict.keys()):

            if j == -20:
                c.showPage()
                c.setFont("Helvetica-Bold", 20)
                text_width = c.stringWidth(institution_name, "Helvetica-Bold", 20)
                c.drawString((600 - text_width)/2, 960, institution_name)
                c.setFont("Helvetica", 12)
                j = 880

            c.rect(20, j, x, 60)
            j -= 60

            for k in range(2):
                c.line((x/3)*(k+1) + 20, j + 60, (x/3)*(k+1) + 20, j + 120)

            c.line(x/3 + 20, j + 90, x + 20, j + 90)
            c.drawString(x/5.4, j + 85, key)
            c.drawString(x/2, j + 100, f"Roll 1-{dict[key][1] - 1}")
            c.drawString(x/2, j + 70, f"Roll {dict[key][1]}-{dict[key][0]}")
            c.drawString(x/1.23, j + 100, f"Room {dict[key][2]}")
            c.drawString(x/1.23, j + 70, f"Room {dict[key][3]}")

    def send_to_pdf(c1, c2):
        class_data = {}

        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)

            if not os.path.isfile(filepath):
                continue

            with open(filepath, "r") as file:
                lines = file.readlines()

                if len(lines) < 5:
                    continue

                classes = [cls.strip() for cls in lines[0].strip().split(',')]
                room1 = [r.strip() for r in lines[1].strip().split(',')]
                room2 = [r.strip() for r in lines[2].strip().split(',')]

                try:
                    s2 = int(room1[2]) + 1
                except (ValueError, IndexError):
                    s2 = 1

                starts1 = [1, 1]
                starts2 = [int(room1[1]) + 1, s2]
                class_data[classes[0]] = [classes[1], starts2[0], room1[0], room2[0]]

                if len(classes) == 4:
                    class_data[classes[2]] = [classes[3], starts2[1], room1[0], room2[0]]

                rolls1 = parse_rollpairs(lines[3].strip())
                rolls2 = parse_rollpairs(lines[4].strip())
                add_room_page(c1, classes[0], classes[2] if len(classes) == 4 else "None", room1[0], starts1, rolls1)
                add_room_page(c1, classes[0], classes[2] if len(classes) == 4 else "None", room2[0], starts2, rolls2)

        gen_cumulative_chart(c2, class_data)

    def gen_pdf(name1, name2):
        c1 = canvas.Canvas("PDFs\\" + name1 + ".pdf", pagesize=(600, 400))
        c2 = canvas.Canvas("PDFs\\" + name2 + ".pdf", pagesize=(600, 1000))
        send_to_pdf(c1, c2)
        c1.save()
        c2.save()
        
    gen_pdf("all_rooms", "cumulative")
