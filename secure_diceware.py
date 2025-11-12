# secure_diceware.py
import urllib.request
import secrets

URL = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"

def pick_words(n=6):
    with urllib.request.urlopen(URL, timeout=10) as r:
        # هر خط: "11111\tword"
        lines = [line.decode().strip().split()[-1] for line in r.readlines()]
    # انتخاب امن بدون بازنویسی فایل دیسک
    chosen = [secrets.choice(lines) for _ in range(n)]
    # فوراً رفرنس‌ها از بین می‌روند وقتی تابع تموم بشه (garbage collect)
    return " ".join(chosen)

if __name__ == "__main__":
    print(pick_words(6))


# Set-PSReadLineOption -HistorySaveStyle SaveNothing
# python secure_diceware.py
# Clear-History
# Clear-Host

