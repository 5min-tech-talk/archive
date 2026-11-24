import hashlib
import subprocess
import sys
import time


def demo_1_blacklist_filtering():
    """
    [실무 문제 1] 유저 로그 5만 건에서 블랙리스트 1만 명 필터링하기
    - list 사용 시: O(N * M) -> 체감될 정도로 멈춤
    - set  사용 시: O(N + M) -> 해시 테이블 조회 O(1)로 즉시 완료
    """
    print("=" * 55)
    print("🔥 [문제 1] 로그 5만 건 중 블랙리스트 1만 명 필터링")
    print("=" * 55)

    logs = [f"user_{i}" for i in range(50_000)]
    blacklist_list = [f"user_{i}" for i in range(40_000, 50_000)]

    # 1) list로 in 연산 (O(N * M))
    t0 = time.perf_counter()
    blocked_list = [u for u in logs if u in blacklist_list]
    t1 = time.perf_counter()

    # 2) set(해시 테이블)으로 변환 후 in 연산 (O(N + M))
    t2 = time.perf_counter()
    blacklist_set = set(blacklist_list)
    blocked_set = [u for u in logs if u in blacklist_set]
    t3 = time.perf_counter()

    list_ms = (t1 - t0) * 1000
    set_ms = (t3 - t2) * 1000

    print(f"• list 탐색 결과: {len(blocked_list):,}건 | 소요 시간: {list_ms:,.2f} ms")
    print(f"• set  탐색 결과: {len(blocked_set):,}건 | 소요 시간: {set_ms:,.2f} ms")
    print(f"👉 속도 차이: 약 {list_ms / set_ms:,.0f}배 빨라짐!\n")


def demo_2_cache_key_bug():
    """
    [실무 문제 2] 다국어 JSON 캐시 키로 Python hash()를 썼을 때의 버그
    - Python은 Hash DoS 공격 방어를 위해 프로세스 시작마다 PYTHONHASHSEED를 랜덤화함
    - 서버가 재시작되면 같은 데이터도 hash() 값이 달라져 캐시가 100% 깨짐
    - 해결: ETag/캐시 키 등 영구 식별자는 반드시 암호화 해시(SHA-256) 사용
    """
    print("=" * 55)
    print("🔥 [문제 2] 서버 재시작 시 Python hash() vs SHA-256")
    print("=" * 55)

    payload = '{"greeting": "오늘 기분은 어때?"}'
    payload_modified = '{"greeting": "오늘 기분은 어때요?"}'  # 1글자('요') 추가

    # 새 파이썬 프로세스를 2번 띄워 '서버 재시작' 상황 재현
    cmd = [sys.executable, "-c", f"print(hash({payload!r}))"]
    h1 = subprocess.check_output(cmd, text=True).strip()
    h2 = subprocess.check_output(cmd, text=True).strip()

    print(f"[Python hash() - 서버 1회차 실행] {h1}")
    print(f"[Python hash() - 서버 재시작 후 ] {h2}")
    print(f"👉 같은 데이터인데 일치 여부: {h1 == h2} (캐시 100% 깨짐!)\n")

    # SHA-256 (ETag용 콘텐츠 해시)
    sha1 = hashlib.sha256(payload.encode()).hexdigest()
    sha2 = hashlib.sha256(payload.encode()).hexdigest()
    sha_mod = hashlib.sha256(payload_modified.encode()).hexdigest()

    print(f"[SHA-256 원본 1회차] {sha1}")
    print(f"[SHA-256 원본 2회차] {sha2}  (항상 동일: {sha1 == sha2})")
    print(f"[SHA-256 1글자 수정] {sha_mod}  (쇄도 효과로 완전히 달라짐)")


if __name__ == "__main__":
    demo_1_blacklist_filtering()
    demo_2_cache_key_bug()