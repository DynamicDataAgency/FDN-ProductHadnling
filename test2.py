import os
from dotenv import load_dotenv
load_dotenv()
creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print(creds_path)