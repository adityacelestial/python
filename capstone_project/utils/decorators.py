import functools
import time
from fastapi import Depends, HTTPException
from security import get_current_user


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed = end - start
        print(f"[timer] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            last_exc = None
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    attempts += 1
                    print(f"[retry] Attempt {attempts}/{max_attempts} failed: {exc}")
                    last_exc = exc
                    time.sleep(1)
            raise last_exc
        return wrapper
    return decorator


def require_role(role: str):
    def dependency(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        if user_role != role:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient role")
        return current_user
    return dependency
