#!/usr/bin/env python3
"""
Secure Password Hash Generator for 40th Birthday Trip Assistant

This script generates a bcrypt password hash that should be stored
in the TRIP_PASSWORD_HASH environment variable.

Usage:
    python generate_password.py
"""

import bcrypt
import getpass

def generate_password_hash():
    """Generate a secure bcrypt password hash"""
    print("\n" + "="*60)
    print("🔐 SECURE PASSWORD HASH GENERATOR")
    print("="*60)
    print("\nThis will create a bcrypt hash for your trip assistant.")
    print("The hash will be stored in the TRIP_PASSWORD_HASH environment variable.")
    print("\n⚠️  IMPORTANT: Keep this password secure and memorable!\n")

    # Get password from user (hidden input)
    while True:
        password = getpass.getpass("Enter your desired password: ")
        password_confirm = getpass.getpass("Confirm password: ")

        if password != password_confirm:
            print("❌ Passwords don't match. Try again.\n")
            continue

        if len(password) < 8:
            print("❌ Password must be at least 8 characters. Try again.\n")
            continue

        break

    # Generate bcrypt hash with salt (rounds=12 is good balance of security/speed)
    print("\n🔄 Generating secure hash...")
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    hashed_str = hashed.decode('utf-8')

    print("✅ Password hash generated successfully!\n")

    # Display results
    print("="*60)
    print("📋 ADD THIS TO YOUR .env FILE:")
    print("="*60)
    print(f"TRIP_PASSWORD_HASH={hashed_str}")
    print("="*60)

    # Verify it works
    print("\n🧪 TESTING THE HASH...")
    if bcrypt.checkpw(password_bytes, hashed):
        print("✅ Hash verification successful!")
    else:
        print("❌ Hash verification failed! (This should never happen)")

    print("\n" + "="*60)
    print("📝 NEXT STEPS:")
    print("="*60)
    print("1. Copy the TRIP_PASSWORD_HASH line above")
    print("2. Add it to your .env file (create if it doesn't exist)")
    print("3. Restart your Streamlit application")
    print("4. Test login with your password")
    print("\n⚠️  Security Tips:")
    print("   - NEVER commit the .env file to Git")
    print("   - Keep a secure backup of your password")
    print("   - Use a unique, strong password")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        generate_password_hash()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
