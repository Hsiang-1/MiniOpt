SYSTEM_PROMPT='You are a helpful assistant.'
USER_PROMPT=r'''Please classify the following optimization problem into one of these technical types based on the mathematical formulation and decision variables, not just surface-level descriptions:

1. Linear Programming (LP): Problems with linear objective function and linear constraints, all continuous variables
2. Integer Programming (IP): Problems with linear or nonlinear components where ALL variables are discrete/integer
3. Mixed Integer Linear Programming (MILP): Problems with linear components containing BOTH continuous and discrete variables
4. Nonlinear Programming (NLP): Problems with nonlinear objective function and/or nonlinear constraints (variables may be continuous/discrete)
5. Combinatorial Optimization (CO): Problems focused on selecting/discrete structures (graphs, permutations, sets) with typically binary variables
6. Multi-objective Programming (MOP): Problems explicitly optimizing multiple conflicting objectives simultaneously
7. Second-Order Cone Programming (SOCP): Problems with a linear objective function, linear constraints, and second-order cone constraints (e.g., \(\|Ax + b\| \leq c^T x + d\))  

# Problem:
{{Question}}

# Output
Analyze the mathematical structure step by step and classify its type. Finally, output the type abbreviation in the following format:
Type: Abbreviation of the type

Note: 
- Focus on the fundamental mathematical formulation, not application domain
- Check variable types (continuous/discrete/binary) and objective/constraint linearity
- For MOP, there must be explicit multiple objectives
- For pure discrete problems with special structures (e.g. graphs), prefer CO over IP'''