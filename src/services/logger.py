import logging
import time
import functools
import os
import inspect
import utils.helpers as helpers
def get_log_path():
    return os.path.join(helpers.get_project_root(), "app.log")

log_path = get_log_path()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d - %(filename)s:%(lineno)d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler()
    ])

logger = logging.getLogger(__name__)

def _get_caller_info(level):
    frame = inspect.currentframe()
    for _ in range(level):
        frame = frame.f_back
        if frame is None:
            break
    return frame.f_code.co_filename, frame.f_lineno

def get_logs():
    with open(log_path, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def log(mode="debug", call_level=3):  # debug, info, error
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if mode == "debug":
                # DEBUG: time_measurement
                start = time.time()
                result = func(*args, **kwargs)
                duration = (time.time() - start) * 1000
                debug(f"PERF: {func.__name__} took {duration:.2f}ms", level=call_level)
                return result
                
            elif mode == "info":
                # INFO: call_arguments
                info(f"CALL: {func.__name__} with args={args}, kwargs={kwargs}", level=call_level)
                return func(*args, **kwargs)
                
            elif mode == "error":
                # ERROR: log_exceptions
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error(f"ERROR in {func.__name__}: {e}", level=call_level)
                    raise
            elif mode == "critical":
                # CRITICAL: log_exceptions
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    critical(f"CRITICAL in {func.__name__}: {e}", level=call_level)
                    raise
            else: 
                error(f"ШАКАЛ: неизвестный mode='{mode}' в декораторе @log", level=call_level)
                return func(*args, **kwargs) 
                    
        return wrapper
    return decorator

def debug(msg, level=2):
    filename, lineno = _get_caller_info(level)
    logger.debug(f"{os.path.basename(filename)}:{lineno} - {msg}")

def info(msg, level=2):
    filename, lineno = _get_caller_info(level)  
    logger.info(f"{os.path.basename(filename)}:{lineno} - {msg}")

def warning(msg, level=2):
    filename, lineno = _get_caller_info(level)  
    logger.warning(f"{os.path.basename(filename)}:{lineno} - {msg}")

def error(msg, level=2):
    filename, lineno = _get_caller_info(level)  
    logger.error(f"{os.path.basename(filename)}:{lineno} - {msg}")

def critical(msg, level=2):
    filename, lineno = _get_caller_info(level)  
    logger.critical(f"{os.path.basename(filename)}:{lineno} - {msg}")

def clear_logs():
    open('app.log', 'w').close()
    info("Логи очищены пользователем")