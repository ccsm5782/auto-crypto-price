import requests
import datetime

# 빗썸 API URL (비트코인 KRW 마켓)
url = "https://api.bithumb.com/v1/ticker?markets=KRW-BTC"

try:
    response = requests.get(url)
    response.raise_for_status() # 에러 발생 시 예외 처리
    data = response.json()
    
    # API 응답이 리스트 형태이므로 첫 번째 요소를 가져옴
    ticker = data[0]
    
    # 필요한 데이터 추출
    price = ticker['trade_price']
    change_rate = ticker['signed_change_rate'] * 100 # 백분율 변환
    
    # [수정된 부분 시작] -----------------------------------------
    # 기존: 빗썸에서 준 거래 체결 시간 사용 (거래 없으면 시간 안 바뀜)
    # 수정: 파이썬이 실행되는 현재 시간을 구해 강제로 시간 갱신 (무조건 바뀜)
    
    # GitHub 서버는 UTC(협정 세계시) 기준이므로 한국 시간(KST, UTC+9)으로 변환
    kst_timezone = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(kst_timezone)
    
    formatted_date = now.strftime("%Y-%m-%d")
    formatted_time = now.strftime("%H:%M:%S")
    # [수정된 부분 끝] -------------------------------------------
    
    # 등락 화살표 표시
    if change_rate > 0:
        icon = "🔺"
    elif change_rate < 0:
        icon = "🟦"
    else:
        icon = "➖"

    # README.md에 저장할 내용 작성
    readme_content = f"""
# 💰 비트코인(BTC) 실시간 시세 자동화: 나는 BIUT야 엄마 나 어떡해 ㅜㅜ

GitHub Actions와 Cron을 이용해 5분마다 빗썸 가격 정보를 업데이트합니다.

## 📊 현재 시세 (Bithumb 기준)

| 항목 | 값 |
| --- | --- |
| **현재가** | **{price:,.0f} KRW** |
| **변동률(전일대비)** | {icon} {change_rate:.2f}% |
| **마지막 확인** | {formatted_date} {formatted_time} (KST) |

---
*Last updated by GitHub Actions bot*
"""

    # README.md 파일 쓰기
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    print("README.md 업데이트 성공")

except Exception as e:
    print(f"에러 발생: {e}")