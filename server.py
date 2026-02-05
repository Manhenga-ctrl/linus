import time
from paynow import Paynow

# ---- CONFIG ----
INTEGRATION_ID = "23355"
INTEGRATION_KEY = "6d375f6a-0058-43a3-9869-1fb46100da78"
RETURN_URL = "https://linus.co.zw"
RESULT_URL = "https://linus.co.zw/"

# ---- INIT ----
paynow = Paynow(
    INTEGRATION_ID,
    INTEGRATION_KEY,
    RETURN_URL,
    RESULT_URL
)

print("\n=== PAYNOW CLI TEST ===\n")

# ---- USER INPUT ----
phone = input("Enter EcoCash number (e.g. 0777xxxxxx): ").strip()
amount = float(input("Enter amount (USD): "))

# ---- CREATE PAYMENT ----
payment = paynow.create_payment("CLI Test Payment", "cli@test.com")
payment.add("Test Item", amount)

print("\nSending payment request to EcoCash...")

# ---- SEND PAYMENT ----
response = paynow.send_mobile(payment, phone, "ecocash")

if not response.success:
    print("❌ Failed to initiate payment")
    print("Error:", response.error)
    exit(1)

poll_url = response.poll_url
print("✅ Payment request sent")
print("Poll URL:", poll_url)

# ---- POLLING ----
print("\nWaiting for customer confirmation...")
print("Press Ctrl+C to stop\n")

try:
    while True:
        status = paynow.check_transaction_status(poll_url)

        print(
            f"Status: {status.status} | "
            f"Paid: {status.paid} | "
            f"Amount: {status.amount}"
        )

        if status.status.lower() in ["paid", "cancelled", "failed"]:
            print("\n=== FINAL STATUS ===")
            print("Status:", status.status)
            break

        time.sleep(5)

except KeyboardInterrupt:
    print("\nPolling stopped by user")
