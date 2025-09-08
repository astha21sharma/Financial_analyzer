from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Function to add code block style
def add_code_block(doc, code_text):
    p = doc.add_paragraph()
    run = p.add_run(code_text)
    run.font.name = 'Courier New'
    run.font.size = Pt(10)
    # Make it look like a code box
    shading_elm = OxmlElement("w:shd")
    shading_elm.set(qn("w:fill"), "D9EAF7")  # light blue background
    p._element.get_or_add_pPr().append(shading_elm)

# Create a new Document
doc = Document()

# Title
doc.add_heading('House Price Dataset Analysis', level=1)

# ---------------- Sample Data ----------------
doc.add_heading('1. Sample Data (First 5 Rows)', level=2)
add_code_block(doc, "print(df.head())")

sample_data = [
    ["price", "area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom", "basement",
     "hotwaterheating", "airconditioning", "parking", "prefarea", "furnishingstatus"],
    [13300000, 7420, 4, 2, 3, "yes", "no", "no", "no", "yes", 2, "yes", "furnished"],
    [12250000, 8960, 4, 4, 4, "yes", "no", "no", "no", "yes", 3, "no", "furnished"],
    [12250000, 9960, 3, 2, 2, "yes", "no", "yes", "no", "no", 2, "yes", "semi-furnished"],
    [12215000, 7500, 4, 2, 2, "yes", "no", "yes", "no", "yes", 3, "yes", "furnished"],
    [11410000, 7420, 4, 1, 2, "yes", "yes", "yes", "no", "yes", 2, "no", "furnished"],
]

table = doc.add_table(rows=len(sample_data), cols=len(sample_data[0]))
table.style = 'Light List Accent 1'
for i, row in enumerate(sample_data):
    for j, val in enumerate(row):
        table.cell(i, j).text = str(val)

# ---------------- Range ----------------
doc.add_heading('2. Range (Max – Min)', level=2)
add_code_block(doc, "range_values = df.max(numeric_only=True) - df.min(numeric_only=True)\nprint('Range:\\n', range_values, '\\n')")

range_data = [
    ["Feature", "Range"],
    ["price", 11550000],
    ["area", 14550],
    ["bedrooms", 5],
    ["bathrooms", 3],
    ["stories", 3],
    ["parking", 3]
]
table = doc.add_table(rows=len(range_data), cols=len(range_data[0]))
table.style = 'Light Grid Accent 2'
for i, row in enumerate(range_data):
    for j, val in enumerate(row):
        table.cell(i, j).text = str(val)

# ---------------- Q1 ----------------
doc.add_heading('3. Q1 (25th Percentile)', level=2)
add_code_block(doc, "q1 = df.quantile(0.25, numeric_only=True)\nprint('Q1 (25th percentile):\\n', q1, '\\n')")

q1_data = [
    ["Feature", "Q1 Value"],
    ["price", 3430000],
    ["area", 3600],
    ["bedrooms", 2],
    ["bathrooms", 1],
    ["stories", 1],
    ["parking", 0]
]
table = doc.add_table(rows=len(q1_data), cols=len(q1_data[0]))
table.style = 'Light Grid Accent 2'
for i, row in enumerate(q1_data):
    for j, val in enumerate(row):
        table.cell(i, j).text = str(val)

# ---------------- Q3 ----------------
doc.add_heading('4. Q3 (75th Percentile)', level=2)
add_code_block(doc, "q3 = df.quantile(0.75, numeric_only=True)\nprint('Q3 (75th percentile):\\n', q3, '\\n')")

q3_data = [
    ["Feature", "Q3 Value"],
    ["price", 5740000],
    ["area", 6360],
    ["bedrooms", 3],
    ["bathrooms", 2],
    ["stories", 2],
    ["parking", 1]
]
table = doc.add_table(rows=len(q3_data), cols=len(q3_data[0]))
table.style = 'Light Grid Accent 2'
for i, row in enumerate(q3_data):
    for j, val in enumerate(row):
        table.cell(i, j).text = str(val)

# ---------------- IQR ----------------
doc.add_heading('5. Interquartile Range (IQR)', level=2)
add_code_block(doc, "iqr = q3 - q1\nprint('Interquartile Range (IQR):\\n', iqr, '\\n')")

iqr_data = [
    ["Feature", "IQR"],
    ["price", 2310000],
    ["area", 2760],
    ["bedrooms", 1],
    ["bathrooms", 1],
    ["stories", 1],
    ["parking", 1]
]
table = doc.add_table(rows=len(iqr_data), cols=len(iqr_data[0]))
table.style = 'Light Grid Accent 2'
for i, row in enumerate(iqr_data):
    for j, val in enumerate(row):
        table.cell(i, j).text = str(val)

# Save document
doc.save("house_summary_with_code.docx")
print("✅ Word document created: house_summary_with_code.docx")
