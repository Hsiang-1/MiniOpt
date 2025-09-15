SYSTEM_PROMPT='You are a helpful assistant.'
USER_PROMPT=r'''You are an expert in optimization problems. Your task is to convert the given gurobipy code into pyomo code.

**Instructions:**
1. Don't give any explanation, just provide the converted pyomo code in the following format:
```python
[pyomo code here]
```
2. Please note that the following solvers are available for use: 'glpk', 'cbc', 'ipopt', 'scip'. Other solvers should not be utilized.
3. Please add `from pyomo.environ import *` at the beginning of your code.
4. Please print the optimal objective value at the end of the code.

**Gurobipy code:**
{gurobipy}'''