from datetime import datetime
import random
import os
from reportlab.pdfgen import canvas

folder = "Seating_Plans"
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

    institution_name = "BHAVAN'S GANGABUX KANORIA VIDYAMANDIR"
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

def send_to_pdf(c):
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

            rolls1 = parse_rollpairs(lines[3].strip())
            rolls2 = parse_rollpairs(lines[4].strip())

            add_room_page(c, classes[0], classes[1] if len(classes) == 2 else "None", room1[0], starts1, rolls1)
            add_room_page(c, classes[0], classes[1] if len(classes) == 2 else "None", room2[0], starts2, rolls2)

def gen_pdf(pdfname):
    c = canvas.Canvas("PDFs\\" + pdfname + ".pdf", pagesize=(600, 400))
    send_to_pdf(c)
    c.save()

gen_pdf("all_rooms")
