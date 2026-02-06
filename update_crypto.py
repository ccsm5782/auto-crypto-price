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
    trade_date = ticker['trade_date_kst']
    trade_time = ticker['trade_time_kst']
    
    # 날짜와 시간 포맷팅 (YYYY-MM-DD HH:MM:SS)
    formatted_date = f"{trade_date[:4]}-{trade_date[4:6]}-{trade_date[6:]}"
    formatted_time = f"{trade_time[:2]}:{trade_time[2:4]}:{trade_time[4:]}"
    
    # 등락 화살표 표시
    if change_rate > 0:
        icon = "🔺"
    elif change_rate < 0:
        icon = "🟦"
    else:
        icon = "➖"

    # README.md에 저장할 내용 작성
    readme_content = f"""
# 💰 비트코인(BTC) 실시간 시세 자동화

GitHub Actions와 Cron을 이용해 5분마다 빗썸 가격 정보를 업데이트합니다.

## 📊 현재 시세 (Bithumb 기준)

| 항목 | 값 |
| --- | --- |
| **현재가** | **{price:,.0f} KRW** |
| **변동률(전일대비)** | {icon} {change_rate:.2f}% |
| **업데이트 시간** | {formatted_date} {formatted_time} (KST) |

---
*Last updated by GitHub Actions bot*
"""

    # README.md 파일 쓰기
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    print("README.md 업데이트 성공")

except Exception as e:
    print(f"에러 발생: {e}")