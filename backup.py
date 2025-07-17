import boto3
import os
from datetime import datetime

# --- CONFIG ---
s3 = boto3.client('s3')
bucket_name = 'preeti-24030142012'
backup_source_dir = '/Users/preetilakade/Library/Mobile Documents/com~apple~TextEdit/Documents/backup_source.txt'  # Change this
allowed_extensions = ['.pdf', '.jpeg', '.jpg', '.mpeg', '.doc', '.docx', '.txt']

# --- HELPER: check extension ---
def is_allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions

# --- BACKUP FUNCTION ---
def backup_files():
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print(f"🔄 Starting backup at {now}")

    for root, dirs, files in os.walk(backup_source_dir):
        for file in files:
            if is_allowed_file(file):
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, backup_source_dir)
                s3_key = f"backups/{now}/{relative_path.replace(os.sep, '/')}"  

                try:
                    s3.upload_file(local_path, bucket_name, s3_key)
                    print(f"✅ Uploaded {local_path} -> s3://{bucket_name}/{s3_key}")
                except Exception as e:
                    print(f"⚠️ Failed to upload {local_path}: {e}")

    print(f"🏁 Backup completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# --- RUN BACKUP ---
if __name__ == "__main__":
    if os.path.exists(backup_source_dir):
        backup_files()
    else:
        print(f"❌ Source directory not found: {backup_source_dir}")
