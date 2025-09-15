SYSTEM_PROMPT='You are a helpful assistant.'
USER_PROMPT=r'''Please classify the following optimization problem into one of these application domains based on the core decision-making context and primary business function, not just keywords mentioned in the problem:

1. Supply Chain: Decisions about inventory management, distribution network, warehousing operations
2. Finance: Decisions about portfolio management, investments, risk management, financial planning
3. Manufacturing: Decisions about production processes, quality control, factory operations
4. Transportation: Decisions about routing, vehicle scheduling, fleet management, traffic flow, carrier selection
5. Healthcare: Decisions about medical staff scheduling, patient flow, hospital resources
6. Energy: Decisions about power generation, energy conservation, grid distribution
7. Technology: Decisions about network design, data center operations, cloud resources
8. Retail: Decisions about store operations, pricing, inventory, equipment, store layout
9. Agriculture: Decisions about farming operations, crop planning, irrigation
10. Logistics: Decisions about delivery operations, warehouse management, distribution
11. Resources: Decisions about raw materials, equipment allocation, material management
12. Marketing: Decisions about campaign planning, budget allocation, target selection
13. Education: Decisions about course scheduling, resource allocation in schools
14. Environment: Decisions about environmental protection, emissions control, conservation
15. Construction: Decisions about project planning, construction resource allocation
16. Military: Decisions about military operations, deployment, supply management
17. Sports: Decisions about game scheduling, team formation, strategy
18. Telecommunications: Decisions about network coverage, bandwidth allocation
19. Aviation: Decisions about flight scheduling, crew assignment, airport operations
20. Services: Decisions about service operations, staff scheduling, capacity management
21. Public utilities: Decisions about utility services, infrastructure management, service delivery
22. Other: Problems that don't clearly fit into above categories

# Problem:
{{Question}}

# Output
Let's think step by step,give the analysis of the problem and classify it into one of the above application domains.Finally, output the name of the domain in the following format:
Category: Name of the Domain

Note: 
- Focus on the fundamental business function and decision-making context
- Don't be misled by secondary keywords or background story
- Consider who is making the decision and what is their primary business purpose'''