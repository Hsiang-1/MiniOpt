import re
from typing import List, Tuple
from pyomo_executor import run_pyomo_code_local

RUN_COUNTER = 0

def preprocess(solution_str: str) -> str:
    return f"<think>\n{solution_str}"

def validate_response_structure(processed_str: str) -> bool:
    validation_passed = True

    # Check required tags
    tags = {
        'think_start': ('<think>', 1),
        'think_end': ('</think>', 1),
        'answer_start': ('<answer>', 1),
        'answer_end': ('</answer>', 1)
    }

    positions = {}
    for tag_name, (tag_str, expected_count) in tags.items():
        count = processed_str.count(tag_str)
        positions[tag_name] = pos = processed_str.find(tag_str)
        
        if count != expected_count:
            validation_passed = False

    # Verify tag order
    if (positions['think_start'] > positions['think_end'] or
        positions['think_end'] > positions['answer_start'] or
        positions['answer_start'] > positions['answer_end']):
        validation_passed = False
    else:
        pass

    return validation_passed

def extract_code(completion: str) -> str:
    pattern = re.compile(r"```python\n(.*?)```", re.DOTALL)
    matches = pattern.findall(completion)
    extracted_answer = matches[-1] if len(matches) >= 1 else ""
    return extracted_answer

def run_pyomo_code(
    pyomo_codes: List[str],
    max_retries: int = 1,
    retry_delay: float = 0.5,
    timeout: int = 120,
) -> List[Tuple[str, str]]:
    return run_pyomo_code_local(
        pyomo_codes=pyomo_codes,
        max_retries=max_retries,
        retry_delay=retry_delay,
        timeout=timeout,
        max_workers=16
    )

def extract_obj_value(full_output: str) -> List[str]:
    float_pattern = r'-?\d+\.\d+e[+-]?\d+|-?\d+\.\d+|-?\d+e[+-]?\d+|-?\d+'
    try:
        matches = re.findall(float_pattern, full_output)
        rounded = [str(round(float(num), 1)) for num in matches]
        return rounded
    except Exception as e:
        return []

def compute_score_batched(data_sources, solution_strs, ground_truths, extra_infos, batch_size: int = 8192):
    """
    Computes scores for multiple solutions in batches with parallel execution.
    """
    print(f"Processing {len(solution_strs)} solutions in batches of {batch_size}")

    processed_strs = [preprocess(s) for s in solution_strs]
    format_correct = [validate_response_structure(ps) for ps in processed_strs]
    
    pyomo_codes = [extract_code(ps) if is_correct else None 
                   for ps, is_correct in zip(processed_strs, format_correct)]
    
    pyomo_outputs = [("", "")] * len(solution_strs)
    valid_indices = [i for i, code in enumerate(pyomo_codes) if code is not None]
    valid_codes = [code for code in pyomo_codes if code is not None]
    
    for i in range(0, len(valid_codes), batch_size):
        batch_codes = valid_codes[i:i + batch_size]
        batch_outputs = run_pyomo_code(batch_codes)
        for j, (stdout, stderr) in enumerate(batch_outputs):
            idx = valid_indices[i + j]
            pyomo_outputs[idx] = (stdout, stderr)
    
    results = []
    for i in range(len(solution_strs)):
        processed_str = processed_strs[i]
   
        gt_answer = str(ground_truths[i].get("solution", "")).strip()
        gt_rounded = str(round(float(gt_answer), 1)) if gt_answer else ""
        format_score = 1 if format_correct[i] else -1
        five_element_score = 0
        five_element_components = {
            'Sets': False,
            'Parameters': False,
            'Variables': False,
            'Objective': False,
            'Constraints': False
        }

        if format_correct[i]:
            think_pattern = r'<think>(.*?)</think>'
            think_match = re.search(think_pattern, processed_str, re.DOTALL)
            if think_match:
                think_content = think_match.group(1)
                
                found_count = 0
                for element in five_element_components.keys():
                    pattern = rf"{element}:?"
                    if re.search(pattern, think_content, re.DOTALL):
                        five_element_components[element] = True
                        found_count += 1
                        five_element_score += 0.2

                if found_count == 0:
                    five_element_score = -1
                
                for element, found in five_element_components.items():
                    status = "FOUND" if found else "MISSING"
            else:
                five_element_score = -1 
        else:
            five_element_score = -1 
        
        # Calculate answer score
        answer_score = 0
        if format_correct[i]:
            pred_stdout, pred_stderr = pyomo_outputs[i]
            pred_answers = extract_obj_value(pred_stdout)
            is_correct = (gt_rounded in pred_answers) and (not pred_stderr.strip())

            if pred_answers:
                
                if is_correct:
                    answer_score = 2
                else:
                    answer_score = -1.5
            else:
                answer_score = -2
        else:
            answer_score = -2
        
        # Total score
        total_score = format_score + five_element_score + answer_score
        
        results.append({
            "score": total_score,
            "format_score": format_score,
            "five_element_score": five_element_score,
            "answer_score": answer_score
        })
    
    return results