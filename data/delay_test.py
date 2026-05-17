"""
딜레이 효과 측정 스크립트

동일한 질문 세트를 딜레이 없음 / 딜레이 있음으로 각각 실행해
TPM 한도 오류 해소 여부와 실제 속도 차이를 비교합니다.

실행:
  .venv/bin/python delay_test.py             # 딜레이 없음 vs 15초 비교
  .venv/bin/python delay_test.py --delay 10  # 비교할 딜레이 직접 지정 (초)
"""

import argparse
import time
import requests

SERVER_URL = "http://localhost:8080/api/chat"

QUESTIONS = [
    "반품은 배송 완료 후 며칠 안에 신청해야 하나요?",
    "주문 취소는 어떻게 하나요?",
    "VIP 회원은 무료 배송 혜택이 어떻게 되나요?",
    "플러스 등급 포인트 적립률이 몇 퍼센트예요?",
    "걍 환불해주세요 ㅠㅠ",
    "구독 서비스 이용 중이면 무료 배송 기준이 달라지나요?",
    "마켓플레이스 상품도 14일 안에 반품할 수 있나요?",
]


def ask_server(question: str) -> tuple[dict | None, float]:
    """(응답, 소요시간) 반환"""
    start = time.time()
    try:
        resp = requests.post(SERVER_URL, json={"question": question}, timeout=60)
        elapsed = time.time() - start
        if resp.status_code == 200:
            return resp.json(), elapsed
        return None, elapsed
    except Exception:
        return None, time.time() - start


def run_batch(delay: float) -> dict:
    label = f"딜레이 {delay}초" if delay > 0 else "딜레이 없음"
    print(f"\n{'─' * 60}")
    print(f"▶ {label} 실행 중...")

    success, errors = 0, 0
    latencies = []
    total_start = time.time()

    for i, question in enumerate(QUESTIONS):
        if delay > 0 and i > 0:
            print(f"  [{i}/{len(QUESTIONS)}] {delay}초 대기...", end="\r")
            time.sleep(delay)

        result, elapsed = ask_server(question)
        status = "✓" if result else "✗ 오류"
        tokens = result.get("tokenUsage", {}).get("promptTokens", "?") if result else "?"
        print(f"  [{i+1}/{len(QUESTIONS)}] {status}  응답: {elapsed:.1f}초  prompt tokens: {tokens}  | {question[:30]}")

        if result:
            success += 1
            latencies.append(elapsed)
        else:
            errors += 1

    total_elapsed = time.time() - total_start
    delay_total = delay * (len(QUESTIONS) - 1)

    print(f"\n  결과: {success}성공 / {errors}실패")
    print(f"  총 소요시간  : {total_elapsed:.1f}초")
    print(f"  딜레이 합계  : {delay_total:.0f}초")
    print(f"  실제 처리시간: {total_elapsed - delay_total:.1f}초")
    if latencies:
        print(f"  평균 응답시간: {sum(latencies)/len(latencies):.1f}초")

    return {
        "label": label,
        "success": success,
        "errors": errors,
        "total_elapsed": total_elapsed,
        "delay_total": delay_total,
        "avg_latency": sum(latencies) / len(latencies) if latencies else 0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", type=float, default=15, metavar="초", help="비교할 딜레이 (기본 15초)")
    args = parser.parse_args()

    print(f"서버: {SERVER_URL}")
    print(f"질문 수: {len(QUESTIONS)}개")
    print(f"비교: 딜레이 없음  vs  딜레이 {args.delay}초")

    no_delay = run_batch(delay=0)

    print(f"\n  ⏸  다음 배치 전 30초 대기 (TPM 윈도우 리셋)...", end="", flush=True)
    time.sleep(30)
    print()

    with_delay = run_batch(delay=args.delay)

    print(f"\n{'=' * 60}")
    print(f"{'':20s}  {'딜레이 없음':>12s}  {'딜레이 ' + str(args.delay) + '초':>12s}")
    print(f"{'─' * 60}")
    print(f"{'성공/실패':20s}  {no_delay['success']}✓ {no_delay['errors']}✗{'':>8s}  {with_delay['success']}✓ {with_delay['errors']}✗")
    print(f"{'총 소요시간':20s}  {no_delay['total_elapsed']:>11.1f}초  {with_delay['total_elapsed']:>11.1f}초")
    print(f"{'실제 처리시간':20s}  {no_delay['total_elapsed']:>11.1f}초  {with_delay['total_elapsed'] - with_delay['delay_total']:>11.1f}초")
    print(f"{'평균 응답시간':20s}  {no_delay['avg_latency']:>11.1f}초  {with_delay['avg_latency']:>11.1f}초")
    overhead = with_delay['total_elapsed'] - no_delay['total_elapsed']
    print(f"\n딜레이로 인한 추가 대기: +{overhead:.0f}초")


if __name__ == "__main__":
    main()
