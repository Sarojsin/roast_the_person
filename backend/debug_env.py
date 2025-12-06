from dotenv import load_dotenv
import os

print(f"Current CWD: {os.getcwd()}")
# Try loading from default (should look in parents)
loaded = load_dotenv()
print(f"load_dotenv result: {loaded}")

# Try explicit path if default fails
if not loaded:
    print("Trying explicit path ../.env")
    loaded = load_dotenv("../.env")
    print(f"load_dotenv explicit result: {loaded}")

key = os.getenv("GEMINI_API_KEY")
if key:
    print(f"Key found: {key[:4]}...{key[-4:]} (Length: {len(key)})")
else:
    print("Key NOT found")
