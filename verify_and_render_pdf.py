import os
import fitz  # PyMuPDF

pdf_path = "paper/SemanticShield_AI_Research_Paper.pdf"
out_dir = "paper/pages_preview"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
page_count = len(doc)
print(f"Total pages in rendered PDF: {page_count}")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    png_path = os.path.join(out_dir, f"page_{i+1:02d}.png")
    pix.save(png_path)
    print(f"Rendered Page {i+1} -> {png_path} (Width: {pix.width}px, Height: {pix.height}px)")

# Perform text checks across all pages
all_text = ""
for i, page in enumerate(doc):
    all_text += f"\n--- PAGE {i+1} ---\n" + page.get_text("text")

print("\n--- TEXT VERIFICATION CHECK ---")
print(f"Title present: {'SemanticShield AI' in all_text}")
print(f"Authors present: {'Ch. Avinash' in all_text and 'K. Mani Tej Kumar' in all_text and 'K. Kowshik' in all_text}")
print(f"SentinelAI absent: {'SentinelAI' not in all_text}")
print(f"Running header present: {'SemanticShield AI — An Intelligent Agent' in all_text}")
print(f"Table 1 present: {'Technology Stack used in SemanticShield AI' in all_text}")
print(f"Table 4 present: {'Behavioral Profile Summary Performance Metrics' in all_text}")
print(f"Figures 1-16 cited: {all([f'Figure {k}' in all_text for k in range(1, 17)])}")
print(f"References [1] to [14] present: {all([f'[{k}]' in all_text for k in range(1, 15)])}")
