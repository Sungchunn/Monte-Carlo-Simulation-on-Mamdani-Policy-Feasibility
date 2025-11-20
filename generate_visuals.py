"""
Generate and save key visualizations for the Monte Carlo analysis.
Run this script after executing the main notebook to save publication-ready plots.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Configuration (must match notebook)
BUDGET_THRESHOLD = 5_000_000_000
REVENUE_STD_DEV = 1_500_000_000
N_ITERATIONS = 10_000
RANDOM_SEED = 42
ENABLE_MACRO_FACTOR = True
MACRO_FACTOR_STD = 0.05
CURRENCY_FORMAT = '${:,.0f}'

# Create assets directory if it doesn't exist
assets_dir = Path("assets")
assets_dir.mkdir(exist_ok=True)

print("Loading simulation results...")

# Define budgetary policies
budgetary_policies_data = [
    {'policy_name': 'Free City Buses', 'category': 'transport', 'mean_annual_cost': 750_000_000,
     'distribution_type': 'normal', 'std_dev': 50_000_000, 'is_capital_like': False},
    {'policy_name': 'Universal Public Childcare', 'category': 'childcare', 'mean_annual_cost': 6_000_000_000,
     'distribution_type': 'normal', 'std_dev': 1_500_000_000, 'is_capital_like': False},
    {'policy_name': 'Affordable Housing Program', 'category': 'housing', 'mean_annual_cost': 2_500_000_000,
     'distribution_type': 'lognormal', 'std_dev': 750_000_000, 'is_capital_like': True},
    {'policy_name': 'Five City Grocery Stores', 'category': 'food', 'mean_annual_cost': 60_000_000,
     'distribution_type': 'normal', 'std_dev': 15_000_000, 'is_capital_like': False},
    {'policy_name': 'Community Safety Department', 'category': 'safety', 'mean_annual_cost': 300_000_000,
     'distribution_type': 'normal', 'std_dev': 100_000_000, 'is_capital_like': False},
    {'policy_name': 'Green Schools & Climate Retrofits', 'category': 'climate', 'mean_annual_cost': 200_000_000,
     'distribution_type': 'lognormal', 'std_dev': 75_000_000, 'is_capital_like': True},
    {'policy_name': 'Libraries & Social Services', 'category': 'other', 'mean_annual_cost': 100_000_000,
     'distribution_type': 'normal', 'std_dev': 30_000_000, 'is_capital_like': False}
]

budgetary_policies = pd.DataFrame(budgetary_policies_data)

# Simulation functions
def sample_policy_cost(policy_row: pd.Series, rng: np.random.Generator) -> float:
    dist_type = policy_row['distribution_type']
    mean = policy_row['mean_annual_cost']

    if dist_type == 'normal':
        std = policy_row['std_dev']
        sampled = rng.normal(mean, std)
        return max(0, sampled)
    elif dist_type == 'lognormal':
        std = policy_row['std_dev']
        variance = std ** 2
        mean_sq = mean ** 2
        sigma_sq = np.log(1 + variance / mean_sq)
        sigma = np.sqrt(sigma_sq)
        mu = np.log(mean) - sigma_sq / 2
        return rng.lognormal(mu, sigma)
    else:
        raise ValueError(f"Unknown distribution type: {dist_type}")

def run_single_iteration(policies_df, budget_threshold_mean, budget_threshold_std, rng,
                         enable_macro_factor=True, macro_factor_std=0.05):
    actual_revenue = max(0, rng.normal(budget_threshold_mean, budget_threshold_std))

    if enable_macro_factor:
        macro_factor = np.clip(rng.normal(1.0, macro_factor_std), 0.5, 1.5)
    else:
        macro_factor = 1.0

    total_cost = 0.0
    opex_cost = 0.0
    capex_cost = 0.0

    for idx, policy in policies_df.iterrows():
        base_cost = sample_policy_cost(policy, rng)
        cost = base_cost * macro_factor
        total_cost += cost

        if policy['is_capital_like']:
            capex_cost += cost
        else:
            opex_cost += cost

    budget_surplus = actual_revenue - total_cost
    within_budget = total_cost <= actual_revenue
    double_whammy = (actual_revenue < budget_threshold_mean * 0.9) and (total_cost > total_cost / macro_factor * 1.1)

    return {
        'total_cost': total_cost,
        'opex_cost': opex_cost,
        'capex_cost': capex_cost,
        'actual_revenue': actual_revenue,
        'budget_surplus': budget_surplus,
        'within_budget': within_budget,
        'macro_factor': macro_factor,
        'double_whammy': double_whammy
    }

def run_simulation(policies_df, budget_threshold, revenue_std, n_iterations, random_seed,
                   enable_macro_factor=True, macro_factor_std=0.05):
    rng = np.random.default_rng(random_seed)
    results = []

    for i in range(n_iterations):
        iteration_result = run_single_iteration(
            policies_df, budget_threshold, revenue_std, rng,
            enable_macro_factor=enable_macro_factor, macro_factor_std=macro_factor_std
        )

        row = {
            'iteration': i,
            'total_cost': iteration_result['total_cost'],
            'opex_cost': iteration_result['opex_cost'],
            'capex_cost': iteration_result['capex_cost'],
            'actual_revenue': iteration_result['actual_revenue'],
            'budget_surplus': iteration_result['budget_surplus'],
            'within_budget': iteration_result['within_budget'],
            'macro_factor': iteration_result['macro_factor'],
            'double_whammy': iteration_result['double_whammy']
        }
        results.append(row)

    return pd.DataFrame(results)

print(f"Running {N_ITERATIONS:,} Monte Carlo iterations...")
simulation_results = run_simulation(
    policies_df=budgetary_policies,
    budget_threshold=BUDGET_THRESHOLD,
    revenue_std=REVENUE_STD_DEV,
    n_iterations=N_ITERATIONS,
    random_seed=RANDOM_SEED,
    enable_macro_factor=ENABLE_MACRO_FACTOR,
    macro_factor_std=MACRO_FACTOR_STD
)

# Calculate statistics
mean_total_cost = simulation_results['total_cost'].mean()
mean_revenue = simulation_results['actual_revenue'].mean()
mean_opex = simulation_results['opex_cost'].mean()
mean_capex = simulation_results['capex_cost'].mean()
prob_affordable = simulation_results['within_budget'].mean()

print(f"Simulation complete. Generating visualizations...")

# VISUALIZATION 1: Cost vs Revenue Distribution
print("  1/4: Cost vs Revenue Distribution...")
plt.figure(figsize=(10, 6))
plt.hist(simulation_results['total_cost'] / 1e9, bins=50, alpha=0.6, color='steelblue',
         edgecolor='black', label='Total Cost', density=False)
plt.hist(simulation_results['actual_revenue'] / 1e9, bins=50, alpha=0.6, color='green',
         edgecolor='black', label='Actual Revenue', density=False)
plt.axvline(BUDGET_THRESHOLD / 1e9, color='darkgreen', linestyle='--', linewidth=2,
            label=f'Mean Revenue (${BUDGET_THRESHOLD/1e9:.1f}B)')
plt.axvline(mean_total_cost / 1e9, color='darkblue', linestyle=':', linewidth=2,
            label=f'Mean Cost (${mean_total_cost/1e9:.2f}B)')
plt.xlabel('Cost / Revenue ($ Billions)', fontsize=12, fontweight='bold')
plt.ylabel('Frequency', fontsize=12, fontweight='bold')
plt.title('Cost vs Revenue Distributions: The Funding Gap', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(assets_dir / 'cost_revenue_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# VISUALIZATION 2: OpEx vs CapEx Breakdown
print("  2/4: OpEx vs CapEx Breakdown...")
plt.figure(figsize=(8, 6))
categories = ['Operating Expenses\n(Hard to Cut)', 'Capital Expenses\n(Can Delay)']
values = [mean_opex / 1e9, mean_capex / 1e9]
colors = ['#e74c3c', '#3498db']
bars = plt.bar(categories, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
plt.axhline(BUDGET_THRESHOLD / 1e9, color='green', linestyle='--', linewidth=2,
            label=f'Mean Revenue (${BUDGET_THRESHOLD/1e9:.0f}B)')
plt.ylabel('Cost ($ Billions)', fontsize=12, fontweight='bold')
plt.title('Operating vs Capital Expenses: Political Flexibility', fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.15,
             f'${val:.2f}B', ha='center', va='bottom', fontweight='bold', fontsize=11)
plt.tight_layout()
plt.savefig(assets_dir / 'opex_capex_breakdown.png', dpi=300, bbox_inches='tight')
plt.close()

# VISUALIZATION 3: Revenue vs Cost Scatter
print("  3/4: Revenue vs Cost Scatter...")
plt.figure(figsize=(10, 8))
colors_scatter = ['green' if w else 'red' for w in simulation_results['within_budget']]
plt.scatter(simulation_results['actual_revenue'] / 1e9, simulation_results['total_cost'] / 1e9,
           alpha=0.2, c=colors_scatter, s=15)
plt.plot([2, 12], [2, 12], 'k--', linewidth=2, label='Break-even line')
plt.xlabel('Actual Revenue ($ Billions)', fontsize=12, fontweight='bold')
plt.ylabel('Total Cost ($ Billions)', fontsize=12, fontweight='bold')
plt.title('Revenue vs Cost: Affordable (Green) vs Deficit (Red) Scenarios',
         fontsize=14, fontweight='bold')
plt.legend(fontsize=10)
plt.grid(alpha=0.3)
# Add annotations
affordable_pct = prob_affordable * 100
plt.text(0.05, 0.95, f'Affordable: {affordable_pct:.2f}%\n(Green dots)',
         transform=plt.gca().transAxes, fontsize=11, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
plt.tight_layout()
plt.savefig(assets_dir / 'revenue_cost_scatter.png', dpi=300, bbox_inches='tight')
plt.close()

# VISUALIZATION 4: Scenario Comparison
print("  4/4: Scenario Comparison...")

# Run scenario simulations
scenarios = {
    'Optimistic\n($8B Revenue)': {
        'cost_mult': 0.85, 'std_mult': 0.7,
        'budget': 8_000_000_000, 'rev_std': 1_200_000_000
    },
    'Base Case\n($5B Revenue)': {
        'cost_mult': 1.0, 'std_mult': 1.0,
        'budget': BUDGET_THRESHOLD, 'rev_std': REVENUE_STD_DEV
    },
    'Pessimistic\n($3B Revenue)': {
        'cost_mult': 1.20, 'std_mult': 1.3,
        'budget': 3_000_000_000, 'rev_std': 1_000_000_000
    }
}

scenario_results = {}
for scenario_name, params in scenarios.items():
    scenario_policies = budgetary_policies.copy()
    scenario_policies['mean_annual_cost'] *= params['cost_mult']
    scenario_policies['std_dev'] *= params['cost_mult'] * params['std_mult']

    scenario_sim = run_simulation(
        scenario_policies, params['budget'], params['rev_std'],
        3_000, RANDOM_SEED, ENABLE_MACRO_FACTOR, MACRO_FACTOR_STD
    )

    scenario_results[scenario_name] = {
        'prob_affordable': scenario_sim['within_budget'].mean() * 100
    }

plt.figure(figsize=(10, 6))
scenario_names = list(scenario_results.keys())
affordability = [scenario_results[s]['prob_affordable'] for s in scenario_names]
colors_scenario = ['green', 'orange', 'red']
bars = plt.bar(scenario_names, affordability, color=colors_scenario, alpha=0.7,
               edgecolor='black', linewidth=2)
plt.axhline(50, color='black', linestyle='--', linewidth=1.5, label='50% Threshold')
plt.ylabel('Probability Affordable (%)', fontsize=12, fontweight='bold')
plt.title('Affordability Probability Across Fiscal Scenarios', fontsize=14, fontweight='bold')
plt.ylim(0, 100)
plt.legend(fontsize=10)
plt.grid(axis='y', alpha=0.3)
for bar, prob in zip(bars, affordability):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 3,
             f'{prob:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
plt.tight_layout()
plt.savefig(assets_dir / 'scenario_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"\n✓ All visualizations saved to {assets_dir}/")
print(f"  - cost_revenue_distribution.png")
print(f"  - opex_capex_breakdown.png")
print(f"  - revenue_cost_scatter.png")
print(f"  - scenario_comparison.png")
