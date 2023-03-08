import streamlit as st
import easyocr as ocr
import sqlite3

uploaded_file = st.file_uploader("Upload a business card image", type=["jpg", "jpeg", "png"])
if st.button("Extract Information"):
    if uploaded_file is not None:
        image = uploaded_file.read()
        reader = ocr.Reader(['en'])
        results = reader.readtext(image)      
        st.write("Extracted Information:")
        table_data = [[result[0], result[1]] for result in results]
        st.table(table_data) 
        conn = sqlite3.connect('business_cards.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS business_cards (id INTEGER PRIMARY KEY, image BLOB, name TEXT, email TEXT, phone TEXT)')
        name = ""
        email = ""
        phone = ""
        for result in results:
            if "name" in result[1].lower():
                name = result[1].split("name")[-1].strip()
            elif "email" in result[1].lower():
                email = result[1].split("email")[-1].strip()
            elif "phone" in result[1].lower():
                phone = result[1].split("phone")[-1].strip()
        c.execute("INSERT INTO business_cards (image, name, email, phone) VALUES (?, ?, ?, ?)", (sqlite3.Binary(image), name, email, phone))
        conn.commit()
        conn.close()
    else:
        st.write("Please upload an image before extracting information.")