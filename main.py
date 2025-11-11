# main.py
from getpass import getpass
from give_items import Give_Items
from insert_logic import encrypt_and_store
from get_pass import Give_Pass

import os
import sys
import time

def show_menu():
    print("\n=== Password Vault Menu ===")
    print("1) Insert a new record")
    print("2) Update an existing record")
    print("3) List all items")
    print("4) Get password by ID")
    print("0) Exit")
    print("===========================\n")

def safe_copy_to_stdout(data: str):
    # به‌جای clipboard سرور، خروجی base64 رو برمی‌گردونه
    import base64, sys
    encoded = base64.b64encode(data.encode()).decode()
    print(f"__CLIPBOARD__{encoded}__END__")  # برچسب مشخص برای شناسایی سمت کلاینت
    sys.stdout.flush()


def prompt_required(label: str, secret: bool = False, to_int: bool = False):
    while True:
        raw = getpass(f"{label}: ") if secret else input(f"{label}: ")
        raw = raw.strip()
        if not raw:
            print(f"{label} is required. Please enter a value.")
            continue
        if to_int:
            try:
                return int(raw)
            except ValueError:
                print(f"{label} must be an integer.")
                continue
        return raw

def prompt_optional(label: str, secret: bool = False, to_int: bool = False):
    raw = getpass(f"{label} (optional): ") if secret else input(f"{label} (optional): ")
    raw = raw.strip()
    if not raw:
        return None
    if to_int:
        try:
            return int(raw)
        except ValueError:
            print(f"{label} must be an integer (optional left empty if unsure).")
            return None
    return raw

def handle_insert():
    print("\n-- Insert Selected --")
    item = prompt_required("item")
    use = prompt_optional("use")

    while True:
        pw_1 = prompt_required("pass", secret=True)
        pw_2 = prompt_required("Confirm pass", secret=True)
        if pw_1 == pw_2:
            break
        print("❌ Keys do not match. Please try again.\n")

    while True:
        short_key_1 = prompt_required("short_key", secret=True)
        short_key_2 = prompt_required("Confirm short_key", secret=True)
        if short_key_1 == short_key_2:
            break
        print("❌ Keys do not match. Please try again.\n")

    # دریافت MainKey با تأیید کامل در حلقه
    while True:
        main_key_1 = prompt_required("MainKey", secret=True)
        main_key_2 = prompt_required("Confirm MainKey", secret=True)
        if main_key_1 == main_key_2:
            break
        print("❌ Keys do not match. Please try again.\n")

    #main_key = prompt_required("MainKey", secret=True)
    note = prompt_optional("Note")

    encrypt_and_store(item=item, use=use, Pass=pw_1, shortKey=short_key_1, MainKey= main_key_1, note= note)
    print("\nCollected inputs for INSERT:")
    print(f"- item: {item}")
    print(f"- use: {use}")
    print(f"- Pass: {'*' * len(pw_1)} (hidden)")       # don’t echo real password
    print(f"- shortKey: {'*' * len(short_key_1)}(hidden)")
    print(f"- MainKey: {'*' * len(main_key_1)} (hidden)")
    print(f"- Note: {note}")

def handle_update():
    print("\n-- Update Selected --")
    row_id = prompt_required("id", to_int=True)
    old_pass = prompt_required("OldPass", secret=True)
    new_pass = prompt_required("NewPass", secret=True)
    main_key = prompt_required("MainKey", secret=True)

    print("\nCollected inputs for UPDATE:")
    print(f"- id: {row_id}")
    print(f"- OldPass: {'*' * len(old_pass)} (hidden)")
    print(f"- NewPass: {'*' * len(new_pass)} (hidden)")
    print(f"- MainKey: {'*' * len(main_key)} (hidden)")

def handle_list_items():
    print("\n-- List Items Selected --")
    short_key = prompt_required("shortKey", secret=True)
    try:
        df = Give_Items(short_key)
        print(f"Rows in df: {getattr(df, 'shape', [0])[0]}")
        print("\nDecrypted Items:")
        print(df)  # برای تست
        
        # df_string = df.to_string(index=False, max_rows=None, max_cols=None)


    except Exception as e:
        print("Error listing items:", e)


def _clear_screen_and_scrollback():
    """
    سعی می‌کنیم هم صفحه و هم scrollback را پاک کنیم.
    روش اصلی با ANSI escapes است (بسیاری از ترمینال‌های مدرن پشتیبانی می‌کنند).
    در غیر این صورت fallback به cls/clear.
    """
    try:
        # ESC[3J -> clear scrollback, ESC[H -> cursor home, ESC[2J -> clear screen
        sys.stdout.write("\x1b[3J\x1b[H\x1b[2J")
        sys.stdout.flush()
        # بعضی ترمینال‌ها ممکن است به دستور سیستم نیاز داشته باشند
        if os.name == "nt":
            # Windows fallback
            os.system("cls")
        else:
            os.system("clear")
    except Exception:
        try:
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
        except Exception:
            pass  # هیچ چیز بهتر از هیچ چیز نیست


def handle_get_password():
    print("\n-- Get Password Selected --")
    row_id = prompt_required("id", to_int=True)
    main_key = prompt_required("MainKey", secret=True)
    try:
        pw = Give_Pass(row_id, main_key)  # typo? should be Give_Pass
        print("\n🔒 Password (visible for 5 seconds):")

        sys.stdout.write(pw + "\n")
        sys.stdout.flush()

        # صبر برای خواندن یا کپی دستی
        time.sleep(10)   # ← اگر خواستی این مقدار را کم/زیاد کن

        # پاک‌کردن صفحه و اسکرول‌بک
        _clear_screen_and_scrollback()

        # تأیید پاک شدن
        print("✅ Screen cleared for security.")

    except Exception as e:
        print("Error:", e)

def main():
    while True:
        show_menu()
        choice = input("Your choice: ").strip()

        if choice == "1":
            handle_insert()
        elif choice == "2":
            handle_update()
        elif choice == "3":
            handle_list_items()
        elif choice == "4":
            handle_get_password()
        elif choice == "0" or choice.lower() in ("q", "quit", "exit"):
            print("Exiting program. Bye!")
            break
        else:
            print("Invalid choice. Please enter 0–4.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
