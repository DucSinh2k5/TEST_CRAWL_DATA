import argparse
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:5000/api"

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Đã lưu dữ liệu vào file: {filename}")

def lookup_by_name(name):
    res = requests.get(f"{BASE_URL}/player", params={"name": name})
    if res.status_code == 200:
        data = res.json()
        print(f"\nKết quả tra cứu cầu thủ '{name}':")
        df = pd.DataFrame(data)
        print(df.head())
        save_to_csv(data, f"{name.replace(' ', '_')}.csv")
    else:
        print(res.json())

def lookup_by_club(club):
    res = requests.get(f"{BASE_URL}/club", params={"squad": club})
    if res.status_code == 200:
        data = res.json()
        print(f"\nKết quả tra cứu CLB '{club}':")
        df = pd.DataFrame(data)
        print(df.head())
        save_to_csv(data, f"{club.replace(' ', '_')}.csv")
    else:
        print(res.json())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tra cứu dữ liệu cầu thủ Premier League.")
    parser.add_argument("--name", help="Tên cầu thủ cần tra cứu", default=None)
    parser.add_argument("--club", help="Tên câu lạc bộ cần tra cứu", default=None)
    args = parser.parse_args()

    # Xử lý linh hoạt:
    if args.name and args.club:
        print(f"\nTra cứu cầu thủ: {args.name}")
        lookup_by_name(args.name)
        print(f"\nTra cứu câu lạc bộ: {args.club}")
        lookup_by_club(args.club)

    elif args.name:
        print(f"\nTra cứu cầu thủ: {args.name}")
        lookup_by_name(args.name)

    elif args.club:
        print(f"\nTra cứu câu lạc bộ: {args.club}")
        lookup_by_club(args.club)

    else:
        print("Cần nhập ít nhất 1 trong 2 tham số: --name hoặc --club")

