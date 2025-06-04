import streamlit as st
import os
import zipfile
import tempfile
from opencc import OpenCC

st.title("🈷️ Batch Convert Simplified Chinese to Traditional Chinese")

uploaded_zip = st.file_uploader("📁 Upload a ZIP file of .txt files (Simplified Chinese)", type="zip")

if uploaded_zip:
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "uploaded.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        extract_dir = os.path.join(tmpdir, "extracted")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        converted_dir = os.path.join(tmpdir, "converted")
        os.makedirs(converted_dir, exist_ok=True)
        converter = OpenCC('s2t')

        for root, _, files in os.walk(extract_dir):
            for file in files:
                if file.endswith(".txt"):
                    src = os.path.join(root, file)
                    with open(src, "r", encoding="utf-8") as f:
                        content = f.read()
                    converted = converter.convert(content)

                    relative_path = os.path.relpath(src, extract_dir)
                    dest_path = os.path.join(converted_dir, relative_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    with open(dest_path, "w", encoding="utf-8") as f:
                        f.write(converted)

        result_zip_path = os.path.join(tmpdir, "converted.zip")
        with zipfile.ZipFile(result_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(converted_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, converted_dir)
                    zipf.write(full_path, arcname)

        with open(result_zip_path, "rb") as f:
            st.download_button("⬇️ Download Converted ZIP", f, "converted_traditional_chinese.zip", "application/zip")
