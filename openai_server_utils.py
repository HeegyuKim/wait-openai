import argparse
import random
import requests
import sys
import time


def wait_for_openai_server(url: str, timeout: int = 300, check_interval: float = 1.0, 
                          verbose: bool = True) -> bool:
    """
    OpenAI 호환 서버가 준비될 때까지 대기합니다.
    
    Args:
        url: OpenAI 호환 서버의 기본 URL (예: 'http://localhost:9090/v1')
        timeout: 최대 대기 시간(초)
        check_interval: 초기 확인 간격(초)
        verbose: 상태 메시지 출력 여부
        
    Returns:
        bool: 서버가 준비되면 True, 타임아웃에 도달하면 False
    """
    start_time = time.time()
    health_url = url.rstrip('/') + '/health/ready'
    models_url = url.rstrip('/') + '/models'
    
    if verbose:
        print(f"OpenAI 호환 서버({url})가 준비될 때까지 대기 중...")
    
    max_backoff = 30  # 최대 백오프 시간(초)
    
    while time.time() - start_time < timeout:
        try:
            # 먼저 health 엔드포인트 시도 (NVIDIA NIM 스타일)
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    if verbose:
                        print(f"서버가 준비되었습니다! 상태 확인 성공.")
                    return True
            except requests.RequestException:
                # Health 엔드포인트를 사용할 수 없는 경우, models 엔드포인트 시도
                pass
                
            # models 엔드포인트 시도 (OpenAI 스타일)
            response = requests.get(models_url, timeout=5)
            if response.status_code == 200:
                if verbose:
                    print(f"서버가 준비되었습니다! Models 엔드포인트 접근 가능.")
                return True
                
        except requests.RequestException as e:
            if verbose:
                print(f"서버가 아직 준비되지 않았습니다: {str(e)}")
            
        # 지터를 사용한 지수 백오프
        jitter = random.uniform(0, 0.5)
        sleep_time = min(check_interval + jitter, max_backoff)
        
        if verbose:
            elapsed = time.time() - start_time
            print(f"대기 중... (경과: {elapsed:.1f}초, 다음 확인까지 {sleep_time:.1f}초)")
            
        time.sleep(sleep_time)
        
        # 지수 백오프를 위한 확인 간격 증가
        check_interval = min(check_interval * 1.5, max_backoff)
    
    if verbose:
        print(f"{timeout}초 후 타임아웃에 도달했습니다. 서버가 준비되지 않았을 수 있습니다.")
    
    return False


def main():
    parser = argparse.ArgumentParser(description="OpenAI 호환 서버가 준비될 때까지 대기")
    parser.add_argument("url", type=str, help="OpenAI 호환 서버의 URL")
    parser.add_argument("--timeout", type=int, default=300, 
                        help="최대 대기 시간(초) (기본값: 300)")
    parser.add_argument("--check-interval", type=float, default=1.0,
                        help="초기 확인 간격(초) (기본값: 1.0)")
    parser.add_argument("--quiet", action="store_true", 
                        help="상태 메시지 출력 안 함")
    
    args = parser.parse_args()
    
    success = wait_for_openai_server(
        url=args.url,
        timeout=args.timeout,
        check_interval=args.check_interval,
        verbose=not args.quiet
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
