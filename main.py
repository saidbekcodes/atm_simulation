"""
ATM (Bankomat) Simulyatsiyasi
-------------------------------
Bu dastur konsol orqali ishlaydigan oddiy ATM tizimini simulyatsiya qiladi.
Foydalanuvchi:
  - PIN kod orqali tizimga kiradi
  - Balansni ko'radi
  - Pul yechadi (withdraw)
  - Pul qo'yadi (deposit)
  - Tranzaksiyalar tarixini ko'radi
  - PIN kodni o'zgartiradi
"""

import datetime

# ---------------------------------------------------
# "Baza" o'rnida ishlatiladigan lug'at (dictionary).
# Haqiqiy loyihada bu ma'lumotlar fayl yoki bazada saqlanadi,
# lekin o'rganish uchun xotirada (RAM) saqlaymiz.
# ---------------------------------------------------
accounts = {
    "1111": {
        "name": "Saidbek",
        "balance": 1500000,
        "history": []
    },
    "2222": {
        "name": "Aziza",
        "balance": 500000,
        "history": []
    }
}

MAX_ATTEMPTS = 3  # PIN kodni noto'g'ri kiritish uchun limit


def log_transaction(pin, text):
    """Har bir amalni tarixga (history) yozib boradi, vaqt bilan birga."""
    vaqt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    accounts[pin]["history"].append(f"[{vaqt}] {text}")


def login():
    """Foydalanuvchidan PIN so'raydi va tekshiradi. Muvaffaqiyatli bo'lsa PIN'ni qaytaradi."""
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        pin = input("\nPIN kodni kiriting: ").strip()
        if pin in accounts:
            print(f"\nXush kelibsiz, {accounts[pin]['name']}!")
            return pin
        else:
            attempts += 1
            qolgan = MAX_ATTEMPTS - attempts
            print(f"Noto'g'ri PIN kod. Qolgan urinishlar: {qolgan}")

    print("\nUrinishlar tugadi. Karta bloklandi. Dastur yakunlanmoqda...")
    return None


def show_balance(pin):
    """Joriy balansni ko'rsatadi."""
    balans = accounts[pin]["balance"]
    print(f"\nJoriy balansingiz: {balans:,} so'm".replace(",", " "))


def deposit(pin):
    """Hisobga pul qo'shish."""
    try:
        summa = int(input("Qancha pul qo'ymoqchisiz (so'm): "))
        if summa <= 0:
            print("Summa musbat son bo'lishi kerak!")
            return
        accounts[pin]["balance"] += summa
        log_transaction(pin, f"Hisobga qo'yildi: +{summa} so'm")
        print(f"{summa:,} so'm hisobingizga qo'shildi.".replace(",", " "))
        show_balance(pin)
    except ValueError:
        print("Iltimos, faqat raqam kiriting!")


def withdraw(pin):
    """Hisobdan pul yechish."""
    try:
        summa = int(input("Qancha pul yechmoqchisiz (so'm): "))
        if summa <= 0:
            print("Summa musbat son bo'lishi kerak!")
            return
        if summa > accounts[pin]["balance"]:
            print("Hisobingizda yetarli mablag' yo'q!")
            return
        accounts[pin]["balance"] -= summa
        log_transaction(pin, f"Yechildi: -{summa} so'm")
        print(f"{summa:,} so'm hisobingizdan yechildi.".replace(",", " "))
        show_balance(pin)
    except ValueError:
        print("Iltimos, faqat raqam kiriting!")


def show_history(pin):
    """Barcha amaliyotlar tarixini ko'rsatadi."""
    history = accounts[pin]["history"]
    if not history:
        print("\nHozircha tranzaksiyalar mavjud emas.")
        return
    print("\n--- Tranzaksiyalar tarixi ---")
    for item in history:
        print(item)


def change_pin(pin):
    """PIN kodni o'zgartirish."""
    yangi_pin = input("Yangi PIN kodni kiriting (4 xonali): ").strip()
    if not yangi_pin.isdigit() or len(yangi_pin) != 4:
        print("PIN kod 4 ta raqamdan iborat bo'lishi kerak!")
        return
    if yangi_pin in accounts:
        print("Bu PIN kod band. Boshqasini tanlang.")
        return

    accounts[yangi_pin] = accounts.pop(pin)
    log_transaction(yangi_pin, "PIN kod o'zgartirildi")
    print("PIN kod muvaffaqiyatli o'zgartirildi!")
    return yangi_pin  # yangilangan PIN'ni qaytaramiz


def main_menu(pin):
    """Login bo'lgandan keyingi asosiy menyu."""
    while True:
        print("\n===== ATM MENYU =====")
        print("1. Balansni ko'rish")
        print("2. Pul qo'yish (Deposit)")
        print("3. Pul yechish (Withdraw)")
        print("4. Tranzaksiyalar tarixi")
        print("5. PIN kodni o'zgartirish")
        print("6. Chiqish")

        tanlov = input("Tanlovingizni kiriting (1-6): ").strip()

        if tanlov == "1":
            show_balance(pin)
        elif tanlov == "2":
            deposit(pin)
        elif tanlov == "3":
            withdraw(pin)
        elif tanlov == "4":
            show_history(pin)
        elif tanlov == "5":
            yangi_pin = change_pin(pin)
            if yangi_pin:
                pin = yangi_pin
        elif tanlov == "6":
            print("\nATM tizimidan chiqdingiz. Xayr!")
            break
        else:
            print("Noto'g'ri tanlov! 1 dan 6 gacha raqam kiriting.")


def main():
    """Dastur shu yerdan boshlanadi."""
    print("===========================================")
    print("   PDP BANK - ATM tizimiga xush kelibsiz")
    print("===========================================")

    pin = login()
    if pin:
        main_menu(pin)


if __name__ == "__main__":
    main()