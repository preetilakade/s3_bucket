import boto3





# Step 1: Initialize the S3 client
s3 = boto3.client('s3')

# Step 2: Specify bucket name (must already exist)
bucket_name = 'preeti-24030142012'  # change to your bucket name

# Step 3: File to upload
file_path = '/Users/preetilakade/Library/Mobile Documents/com~apple~TextEdit/Documents/hello.txt'  # full path to file
object_name = 'hello.txt'  # what it will be called in S3

# Step 4: Upload file
s3.upload_file(file_path, bucket_name, object_name)
print(f"✅ Uploaded '{file_path}' to S3 bucket '{bucket_name}' as '{object_name}'.")


print("📦 Your Buckets:")
buckets = s3.list_buckets()
for b in buckets['Buckets']:
    print(f" - {b['Name']}")

print(f"\n📂 Objects in '{bucket_name}':")
objects = s3.list_objects_v2(Bucket=bucket_name)
if 'Contents' in objects:
    for obj in objects['Contents']:
        print(f" - {obj['Key']}")
else:
    print(" (Empty)")








