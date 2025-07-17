import boto3
import os
from datetime import datetime

# --- SETUP ---
boto3.set_stream_logger('')  # Enables Boto3's internal debug logs (optional, very detailed)
s3 = boto3.client('s3')
bucket_name = 'preeti-24030142012'

# --- CONFIG ---
ALLOWED_EXTENSIONS = ['.pdf', '.jpeg', '.jpg', '.mpeg', '.doc', '.docx', '.txt']

# --- FUNCTION: Check extension ---
def is_allowed_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    print(f"🔍 Checking extension for {file_path}: {ext}")
    return ext in ALLOWED_EXTENSIONS

# --- FUNCTION: Upload file sorted by date ---
def upload_file(file_path):
    if not is_allowed_file(file_path):
        print(f"❌ Skipping unsupported file: {file_path}")
        return

    today = datetime.today().strftime('%Y-%m-%d')
    filename = os.path.basename(file_path)
    s3_key = f"{today}/{filename}"

    print(f"🚀 Preparing to upload: {file_path}")
    print(f"➡ S3 bucket: {bucket_name}")
    print(f"➡ S3 key: {s3_key}")

    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"✅ Successfully uploaded '{file_path}' to S3 as '{s3_key}'")
    except Exception as e:
        print(f"⚠️ Upload failed for '{file_path}'. Error: {e}")

# --- EXAMPLE USAGE ---
files_to_upload = [
    '/Users/preetilakade/Library/Mobile Documents/com~apple~TextEdit/Documents/hello.txt',
]

for file_path in files_to_upload:
    print(f"📄 Processing file: {file_path}")
    if os.path.exists(file_path):
        upload_file(file_path)
    else:
        print(f"⚠️ File not found: {file_path}")
