import boto3
import os
import zipfile
from datetime import datetime

# --- CONFIG ---
bucket_name = 'preeti-24030142012'  # Your bucket (versioning should be enabled)
source_dir = '/Users/preetilakade/Library/Mobile Documents/com~apple~TextEdit/Documents/backup_source.txt'
zip_filename = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
zip_path = f"/tmp/{zip_filename}"

s3 = boto3.client('s3')

# --- FUNCTION: Create zip file ---
def create_zip(source_dir, zip_path):
    print(f"📦 Creating zip file: {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
                print(f"  ➡ Added {file_path} as {arcname}")
    print(f"✅ Zip created: {zip_path}")

# --- FUNCTION: Upload zip to S3 ---
def upload_to_s3(zip_path, bucket_name, s3_key):
    print(f"🚀 Uploading {zip_path} to s3://{bucket_name}/{s3_key}")
    try:
        s3.upload_file(zip_path, bucket_name, s3_key)
        print(f"✅ Uploaded to S3 as {s3_key}")
    except Exception as e:
        print(f"⚠️ Upload failed: {e}")

# --- MAIN ---
if __name__ == "__main__":
    if not os.path.exists(source_dir):
        print(f"❌ Source folder not found: {source_dir}")
        exit(1)

    create_zip(source_dir, zip_path)

    # Use a consistent S3 key so S3 versioning tracks versions of this object
    s3_key = 'backups/latest_backup.zip'
    upload_to_s3(zip_path, bucket_name, s3_key)

    # Clean up local zip file if desired
    # os.remove(zip_path)
