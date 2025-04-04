import argparse
import random
import requests
import sys
import time


def wait_for_openai_server(url: str, timeout: int = 300, check_interval: float = 1.0, 
                          verbose: bool = True) -> bool:
    """
    Wait for an OpenAI-compatible server to be ready.
    
    Args:
        url (str): URL of the OpenAI-compatible server
        timeout (int): Maximum waiting time in seconds (default: 300)
        check_interval (float): Initial check interval in seconds (default: 1.0)
        verbose (bool): Print status messages if True (default: True)
        
    Returns:
        bool: True if the server is ready, False otherwise
    """
    start_time = time.time()
    health_url = url.rstrip('/') + '/health/ready'
    models_url = url.rstrip('/') + '/models'
    
    if verbose:
        print(f"Wating for the server to be ready: {url}")
    
    max_backoff = 30  # 최대 백오프 시간(초)
    
    while time.time() - start_time < timeout:
        try:
            # 먼저 health 엔드포인트 시도 (NVIDIA NIM 스타일)
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    if verbose:
                        print(f"Server is ready! Health endpoint is accessible.")
                    return True
            except requests.RequestException:
                # Health 엔드포인트를 사용할 수 없는 경우, models 엔드포인트 시도
                pass
                
            # models 엔드포인트 시도 (OpenAI 스타일)
            response = requests.get(models_url, timeout=5)
            if response.status_code == 200:
                if verbose:
                    print(f"Server is ready! Models endpoint is accessible.")
                return True
                
        except requests.RequestException as e:
            if verbose:
                print(f"Server is not ready yet: {str(e)}")
            
        # 지터를 사용한 지수 백오프
        jitter = random.uniform(0, 0.5)
        sleep_time = min(check_interval + jitter, max_backoff)
        
        if verbose:
            elapsed = time.time() - start_time
            print(f"Wating... (Elapsed: {elapsed:.1f} sec, Next check in {sleep_time:.1f} sec)")
            
        time.sleep(sleep_time)
        
        # 지수 백오프를 위한 확인 간격 증가
        check_interval = min(check_interval * 1.5, max_backoff)
    
    if verbose:
        print(f"Timeout reached after {timeout} seconds. The server may not be ready.")
    
    return False


def main():
    parser = argparse.ArgumentParser(description="Wait for an OpenAI-compatible server to be ready")
    parser.add_argument("url", type=str, help="URL of the OpenAI-compatible server")
    parser.add_argument("--timeout", type=int, default=300, 
                        help="Maximum waiting time in seconds (default: 300)")
    parser.add_argument("--check-interval", type=float, default=1.0,
                        help="Initial check interval in seconds (default: 1.0)")
    parser.add_argument("--quiet", action="store_true", 
                        help="Do not print status messages")
    
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
