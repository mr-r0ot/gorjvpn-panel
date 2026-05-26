# admincontrol.py
import json
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# ---------- Configuration ----------
ENCRYPTION_KEY = b'\x9f!\x8c\x7e\xd4\x1a\xb3\xc5\xe6\xf0\x2a\x3d\x5e\x7a\x8b\x9c\x0d\x1e\x2f\x3a\x4b\x5c\x6d\x7e\x8f\x9a\xab\xbc\xcd\xde\xef\xf0'
LOCAL_ENCRYPTED_FILE = "data.enc"       # This file will be created/read locally.
                                        # Admin will manually upload its content to GitHub (acc.txt)

# ---------- Crypto Functions ----------
def encrypt_data(plaintext: str, key: bytes) -> str:
    """Encrypt plaintext with AES-CBC and return base64 string."""
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def decrypt_data(encrypted_b64: str, key: bytes) -> str:
    """Decrypt base64 AES-CBC data and return plaintext."""
    raw = base64.b64decode(encrypted_b64)
    iv = raw[:16]
    ciphertext = raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    # Remove PKCS#7 padding
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode('utf-8')

# ---------- Data Management ----------
def load_data():
    """Load existing encrypted data from local file. If file doesn't exist, return default structure."""
    if not os.path.exists(LOCAL_ENCRYPTED_FILE):
        print(f"File '{LOCAL_ENCRYPTED_FILE}' not found. Creating default data structure.")
        return {
            "version": 1,
            "accounts": []
        }
    try:
        with open(LOCAL_ENCRYPTED_FILE, 'r') as f:
            enc_content = f.read().strip()
        plain = decrypt_data(enc_content, ENCRYPTION_KEY)
        return json.loads(plain)
    except Exception as e:
        print(f"Error loading/decrypting data: {e}")
        print("Starting with a fresh default structure.")
        return {
            "version": 1,
            "accounts": []
        }

def save_data(data):
    """Encrypt data and save to local file."""
    plain = json.dumps(data, indent=2, ensure_ascii=False)
    enc = encrypt_data(plain, ENCRYPTION_KEY)
    with open(LOCAL_ENCRYPTED_FILE, 'w') as f:
        f.write(enc)
    print(f"\n[✓] Data successfully saved to '{LOCAL_ENCRYPTED_FILE}'")
    print(f"[i] Copy the entire content of this file and paste it into your GitHub file (acc.txt).")

# ---------- UI Functions (English) ----------
def show_accounts(accounts):
    if not accounts:
        print("No accounts found.")
        return
    print("\n--- Account List ---")
    for i, acc in enumerate(accounts):
        print(f"{i+1}. script_id: {acc['script_id'][:40]}... | auth_key: {acc['auth_key']} | expiry: {acc['expiry']} | devices: {len(acc.get('devices', []))}")

def add_account(accounts):
    print("\n--- Add New Account ---")
    script_id = input("script_id: ").strip()
    auth_key = input("auth_key: ").strip()
    expiry = input("Expiry date (format dd/mm/yyyy): ").strip()
    devices = []
    print("Enter device fingerprints (one per line). Empty line to finish:")
    while True:
        dev = input("Device ID (or press Enter to stop): ").strip()
        if not dev:
            break
        devices.append(dev)
    accounts.append({
        "script_id": script_id,
        "auth_key": auth_key,
        "expiry": expiry,
        "devices": devices
    })
    print("Account added successfully.")

def edit_account(accounts):
    show_accounts(accounts)
    try:
        idx = int(input("Enter account number to edit: ")) - 1
        if idx < 0 or idx >= len(accounts):
            print("Invalid number.")
            return
    except:
        print("Invalid input.")
        return

    acc = accounts[idx]
    print(f"\nEditing account #{idx+1}:")
    print(f"1. script_id (current: {acc['script_id']})")
    print(f"2. auth_key (current: {acc['auth_key']})")
    print(f"3. expiry (current: {acc['expiry']})")
    print(f"4. Add device to allowed list")
    print(f"5. Remove device from allowed list")
    print(f"6. Show current devices")
    choice = input("Choose option (1-6): ").strip()
    if choice == '1':
        acc['script_id'] = input("New script_id: ").strip()
    elif choice == '2':
        acc['auth_key'] = input("New auth_key: ").strip()
    elif choice == '3':
        acc['expiry'] = input("New expiry date (dd/mm/yyyy): ").strip()
    elif choice == '4':
        dev = input("Device ID to add: ").strip()
        if dev not in acc['devices']:
            acc['devices'].append(dev)
            print("Device added.")
        else:
            print("Device already exists.")
    elif choice == '5':
        dev = input("Device ID to remove: ").strip()
        if dev in acc['devices']:
            acc['devices'].remove(dev)
            print("Device removed.")
        else:
            print("Device not found.")
    elif choice == '6':
        print("Allowed devices:")
        for d in acc['devices']:
            print(f"  {d}")
    else:
        print("Invalid option.")
    print("Account updated.")

def delete_account(accounts):
    show_accounts(accounts)
    try:
        idx = int(input("Enter account number to delete: ")) - 1
        if 0 <= idx < len(accounts):
            deleted = accounts.pop(idx)
            print(f"Account with script_id '{deleted['script_id']}' deleted.")
        else:
            print("Invalid number.")
    except:
        print("Invalid input.")

def change_version(data):
    current = data.get("version", 1)
    print(f"Current version: {current}")
    try:
        new_ver = int(input("New version number: "))
        data["version"] = new_ver
        print("Version updated.")
    except:
        print("Invalid number.")

# ---------- Main Menu ----------
def main():
    print("=== Admin Control Panel ===")
    data = load_data()
    
    while True:
        print("\n--- Main Menu ---")
        print("1. Show all accounts")
        print("2. Add new account")
        print("3. Edit an account")
        print("4. Delete an account")
        print("5. Change app version")
        print("6. Save and exit (generate encrypted file)")
        print("7. Exit without saving")
        choice = input("Select option: ").strip()
        
        if choice == '1':
            show_accounts(data["accounts"])
        elif choice == '2':
            add_account(data["accounts"])
        elif choice == '3':
            edit_account(data["accounts"])
        elif choice == '4':
            delete_account(data["accounts"])
        elif choice == '5':
            change_version(data)
        elif choice == '6':
            save_data(data)
            break
        elif choice == '7':
            print("Exiting without saving.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()