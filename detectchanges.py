import boto3
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIG ---
bucket_name = 'preeti-24030142012'
backup_source_dir = '/Users/preetilakade/Library/Mobile Documents/com~apple~TextEdit/Documents/backup_source.txt'
allowed_extensions = ['.pdf', '.jpeg', '.jpg', '.mpeg', '.doc', '.docx', '.txt']

s3 = boto3.client('s3')

# --- HELPER: check allowed file ---
def is_allowed_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return ext in allowed_extensions

# --- S3 UPLOAD FUNCTION ---
def upload_file(file_path):
    if not is_allowed_file(file_path):
        print(f"❌ Skipping unsupported file: {file_path}")
        return
    if not os.path.exists(file_path):
        print(f"⚠️ File no longer exists: {file_path}")
        return
    now = datetime.now().strftime('%Y-%m-%d')
    rel_path = os.path.relpath(file_path, backup_source_dir).replace(os.sep, '/')
    s3_key = f"auto_backup/{now}/{rel_path}"
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"✅ Uploaded: {file_path} -> s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"⚠️ Failed to upload {file_path}: {e}")

# --- EVENT HANDLER ---
class S3BackupHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"🟢 Detected new file: {event.src_path}")
            upload_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"🟠 Detected modified file: {event.src_path}")
            upload_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"🗑️ Detected deleted file: {event.src_path}")
            # Optional: delete from S3 if desired

# --- MONITOR ---
if __name__ == "__main__":
    if not os.path.exists(backup_source_dir):
        print(f"❌ Source folder not found: {backup_source_dir}")
        exit(1)

    event_handler = S3BackupHandler()
    observer = Observer()
    observer.schedule(event_handler, path=backup_source_dir, recursive=True)
    observer.start()
    print(f"👀 Monitoring {backup_source_dir} for changes...")

    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
