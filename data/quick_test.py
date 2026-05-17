"""
빠른 수동 검증 스크립트 — LLM 판정 없음, 비용 $0

서버 응답을 눈으로 확인합니다. 각 wall_type별 대표 질문을 포함합니다.

실행:
  .venv/bin/python quick_test.py           # 전체 출력
  .venv/bin/python quick_test.py --compact  # 답변 요약만
"""

import json
import argparse
import requests
from pathlib import Path

SERVER_URL = "http://localhost:8080/api/chat"

# wall_type별 대표 질문 — easy/conditional/cross_language/versioning 커버
QUESTIONS = [
    {
        "id": "Q001",
        "label": "[easy] 단순 FAQ",
        "question": "주문 취소는 어떻게 하나요?",
        "expected": "My Orders에서 '준비중' 상태일 때 취소 가능. 즉시 처리, 전액 환불. '배송중' 이후는 반품으로 진행.",
    },
    {
        "id": "Q003",
        "label": "[easy] 단순 FAQ",
        "question": "반품은 배송 완료 후 며칠 안에 신청해야 하나요?",
        "expected": "배송 완료 후 14일 이내.",
    },
    {
        "id": "Q016",
        "label": "[medium / contradiction] 마켓플레이스 반품",
        "question": "마켓플레이스 상품도 14일 안에 반품할 수 있나요?",
        "expected": "마켓플레이스 상품은 판매자별 정책(3~30일) 적용. 초록 코퍼레이션 14일 정책 미적용.",
    },
    {
        "id": "Q034",
        "label": "[hard / cross_language] 구어체",
        "question": "걍 환불해주세요 ㅠㅠ",
        "expected": "My Orders > 반품 신청, 사진 첨부, 수거일 선택. 변심은 3,000원 수수료. 카카오페이는 즉시 환불.",
    },
    {
        "id": "CUSTOM-1",
        "label": "[conditional] 등급 조건 분기",
        "question": "VIP 회원은 무료 배송 혜택이 어떻게 되나요?",
        "expected": "VIP는 모든 주문에 Priority 배송 무료.",
    },
    {
        "id": "CUSTOM-2",
        "label": "[versioning] 구버전 함정",
        "question": "플러스 등급 포인트 적립률이 몇 퍼센트예요?",
        "expected": "Plus 3%, VIP 5%. (구버전 5%/7%가 아님)",
    },
    {
        "id": "CUSTOM-3",
        "label": "[conditional] 구독자 조건",
        "question": "구독 서비스 이용 중이면 무료 배송 기준이 달라지나요?",
        "expected": "구독자는 금액 무관 모든 주문 무료 배송. 일반 Standard 회원 2만원 기준 미적용.",
    },
]


def ask_server(question: str) -> dict | None:
    try:
        resp = requests.post(SERVER_URL, json={"question": question}, timeout=60)
        if resp.status_code == 200:
            return resp.json()
        print(f"  [ERROR] HTTP {resp.status_code}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"  [ERROR] 서버 연결 실패: {SERVER_URL}")
        return None
    except requests.exceptions.Timeout:
        print("  [ERROR] 타임아웃 (60초)")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compact", action="store_true", help="답변 첫 줄만 출력")
    args = parser.parse_args()

    print(f"서버: {SERVER_URL}")
    print(f"질문 수: {len(QUESTIONS)}개  |  비용: $0 (LLM 판정 없음)\n")
    print("=" * 70)

    success = 0
    for q in QUESTIONS:
        print(f"\n{q['label']}")
        print(f"질문  : {q['question']}")

        result = ask_server(q["question"])
        if result is None:
            print("응답  : [서버 오류]")
            continue

        answer = result.get("answer", "")
        tokens = result.get("tokenUsage", {})

        if args.compact:
            print(f"응답  : {answer.splitlines()[0][:80]}")
        else:
            print(f"응답  : {answer}")

        print(f"기대  : {q['expected']}")
        print(f"토큰  : prompt={tokens.get('promptTokens')}  completion={tokens.get('completionTokens')}")
        print("-" * 70)
        success += 1

    print(f"\n완료: {success}/{len(QUESTIONS)}건 응답 수신")
    print("응답이 '기대'와 일치하는지 직접 확인하세요.")


if __name__ == "__main__":
    main()
