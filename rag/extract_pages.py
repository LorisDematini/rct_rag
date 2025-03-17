import fitz  # PyMuPDF
import os
import pickle

def extract_pdf_text_by_page(pdf_path):
    text_by_page = {}
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_by_page[page_num + 1] = page.get_text()  # Page numbers start from 1
    return text_by_page


if __name__ == "__main__":
        
    # Iterate over all PDF files in the /data directory and extract text
    data_dir = '/root/work/rct_rag/get_bdd/data'
    # output_path = '/root/work/rct_rag/rag/data/pages.txt'
    output_path = '/root/work/rct_rag/rag/data/pages.pkl'

    pdf_texts = {}

    for filename in os.listdir(data_dir):
        print(filename)
        # Check if the file is a PDF
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(data_dir, filename)
            # Extract text and store it in the dictionary with filename as key
            pdf_texts[filename] = extract_pdf_text_by_page(pdf_path)


    # # Save the extracted text in a text file
    # with open(output_path, 'w', encoding='utf-8') as f:
    #     for pdf_name, pages in pdf_texts.items():
    #         f.write(f"--- {pdf_name} ---\n")
    #         for page_num, text in pages.items():
    #             f.write(f"\n--- Page {page_num} ---\n")
    #             f.write(text + "\n")
    #         f.write("\n" + "="*50 + "\n")  # Separator for PDFs

    # print(f"Text from all PDFs saved to {output_path}")

    with open(output_path, 'wb') as f:
        pickle.dump(pdf_texts, f)

    print(f"Text from all PDFs saved to {output_path}")