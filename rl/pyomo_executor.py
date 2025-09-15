#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import tempfile
import os
import threading
import logging
from typing import Dict, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor

class PyomoExecutor:
    """Pyomo code executor class that supports parallel execution"""
    
    def __init__(self, max_workers: int = 4, default_timeout: int = 120):
        self.max_workers = max_workers
        self.default_timeout = default_timeout
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self._lock = threading.Lock()
    
    def execute_pyomo_code(self, code_content: str, timeout: Optional[int] = None) -> Dict:
        if timeout is None:
            timeout = self.default_timeout
            
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            if not code_content.startswith('# -*- coding: utf-8 -*-'):
                code_content = '# -*- coding: utf-8 -*-\n\n' + code_content
            f.write(code_content)
            temp_file_path = f.name
        
        try:
            cmd = f"python {temp_file_path}"
            
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True,
                cwd=os.path.dirname(temp_file_path),
                timeout=timeout
            )
            
            os.unlink(temp_file_path)
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "error": ""
                }
            else:
                return {
                    "status": "error",
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "error": result.stderr
                }
                
        except subprocess.TimeoutExpired:
            try:
                os.unlink(temp_file_path)
            except:
                pass
            
            return {
                "status": "timeout",
                "stdout": "",
                "stderr": f"Code execution timeout ({timeout} seconds)",
                "error": f"Code execution timeout ({timeout} seconds)"
            }
            
        except Exception as e:
            try:
                os.unlink(temp_file_path)
            except:
                pass
            
            return {
                "status": "exception",
                "stdout": "",
                "stderr": f"Execution exception: {str(e)}",
                "error": f"Execution exception: {str(e)}"
            }
    
    def execute_batch(self, code_contents: list, timeout: Optional[int] = None) -> List[Dict]:
        futures = []
        for code in code_contents:
            future = self.executor.submit(self.execute_pyomo_code, code, timeout)
            futures.append(future)
        
        results = []
        for future in futures:
            try:
                results.append(future.result())
            except Exception as e:
                results.append({
                    "status": "exception",
                    "stdout": "",
                    "stderr": f"Asynchronous execution exception: {str(e)}",
                    "error": f"Asynchronous execution exception: {str(e)}"
                })
        
        return results
    
    def shutdown(self):
        self.executor.shutdown(wait=True)


_default_executor = None

def get_executor(max_workers: int = 4, default_timeout: int = 120) -> PyomoExecutor:
    global _default_executor
    if _default_executor is None:
        _default_executor = PyomoExecutor(max_workers, default_timeout)
    return _default_executor

def execute_code(code_content: str, timeout: Optional[int] = None) -> Dict:
    executor = get_executor()
    return executor.execute_pyomo_code(code_content, timeout)

def execute_batch(code_contents: list, timeout: Optional[int] = None) -> List[Dict]:
    executor = get_executor()
    return executor.execute_batch(code_contents, timeout)

def shutdown_executor():
    global _default_executor
    if _default_executor is not None:
        _default_executor.shutdown()
        _default_executor = None


def run_pyomo_code_local(
    pyomo_codes: List[str],
    max_retries: int = 3,
    retry_delay: float = 0.5,
    timeout: int = 120,
    max_workers: int = 4
) -> List[Tuple[str, str]]:
    """
    Execute multiple Pyomo codes locally
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            executor = PyomoExecutor(max_workers=max_workers, default_timeout=timeout)
            results = executor.execute_batch(pyomo_codes, timeout)
            
            output_list = []
            for result in results:
                if result["status"] == "success":
                    output_list.append((result["stdout"], result["stderr"]))
                else:
                    error_msg = result.get("error", "Unknown error")
                    output_list.append(("", f"Execution failed: {error_msg}"))
            
            executor.shutdown()
            return output_list
            
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                logging.warning(f"Attempt {attempt + 1} failed, retrying in {retry_delay * (attempt + 1)}s: {str(e)}")
            continue
    
    logging.error(f"Failed after {max_retries} retries. Error: {str(last_exception)}")
    return [("", f"All retries failed: {str(last_exception)}")] * len(pyomo_codes)

