import pulp
import pandas as pd

# Step 1: Define the business problem
# Example: A factory produces two products, A and B. Each product requires time on two machines: M1 and M2.
# The goal is to maximize profit while staying within machine time constraints.

# Data
products = ['A', 'B']
profit_per_unit = {'A': 50, 'B': 40}  # Profit per unit of products
machine_time = {
    'M1': {'A': 3, 'B': 2},  # Time required on Machine 1 for A and B
    'M2': {'A': 4, 'B': 3},  # Time required on Machine 2 for A and B
}
machine_availability = {'M1': 240, 'M2': 200}  # Available time for each machine

# Step 2: Define the Linear Programming Problem
prob = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: Number of units to produce for each product
x = {product: pulp.LpVariable(f"Units_of_{product}", lowBound=0, cat='Continuous') for product in products}

# Objective Function: Maximize total profit
prob += pulp.lpSum([profit_per_unit[p] * x[p] for p in products]), "Total_Profit"

# Constraints: Machine availability
for machine, times in machine_time.items():
    prob += pulp.lpSum([times[p] * x[p] for p in products]) <= machine_availability[machine], f"{machine}_Constraint"

# Step 3: Solve the problem
prob.solve()

# Step 4: Display the results
print("Status:", pulp.LpStatus[prob.status])

# Optimal solution
solution = {var.name: var.varValue for var in prob.variables()}
print("Optimal production plan:")
for product, value in solution.items():
    print(f"{product}: {value} units")

# Optimal profit
print("Total Profit:", pulp.value(prob.objective))

# Step 5: Insights
# Save results to a DataFrame for better presentation
results_df = pd.DataFrame({
    "Product": [p for p in products],
    "Optimal_Units": [x[p].varValue for p in products],
    "Profit_Per_Unit": [profit_per_unit[p] for p in products],
})
results_df["Total_Profit"] = results_df["Optimal_Units"] * results_df["Profit_Per_Unit"]

print("\nDetailed Results:")
print(results_df)

# Save insights to a CSV file
results_df.to_csv("optimization_results.csv", index=False)
