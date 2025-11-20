# Monte Carlo Budget Feasibility Analysis: Zohran Mamdani's NYC Mayoral Policy Agenda

## Project Overview

This project uses Monte Carlo simulation to test whether New York City mayoral candidate Zohran Mamdani's proposed spending policies are fiscally feasible under uncertainty. Rather than relying on single-point estimates, the model simulates thousands of scenarios with probabilistic cost distributions to estimate the likelihood that the total policy costs can be covered by projected new revenue.

## Inspiration

I got the inspiration for this project while scrolling through Instagram reels and came across [this video](https://www.instagram.com/reel/DRN-ovfjOON/?igsh=MWMycDdmNXk3eG9seg==) discussing Mamdani's policy proposals. It sparked my curiosity about the fiscal feasibility of such an ambitious agenda, leading me to build this quantitative analysis.

## Key Policy Areas Analyzed

### Budgetary Policies (Significant Annual Costs)
- **Free City Bus Service**: ~$750M/year
- **Universal Public Childcare**: ~$6B/year (largest cost driver)
- **Affordable Housing Construction**: 200,000 units over 10 years (~$100B total)
- **Five City-Run Grocery Stores**: ~$60M/year
- **Community Safety Department**: Alternative public safety approach
- **Green Schools & Climate Retrofits**: Building improvements
- **Libraries & Social Services**: Expanded funding

### Regulatory Policies (Minimal Direct Costs)
- Rent freeze for rent-stabilized apartments
- $30 minimum wage by 2030
- Tenant protections and deed theft enforcement
- App-based delivery work regulation
- LGBTQIA+ protections and sanctuary city policies

## Methodology

The analysis uses:
- **Budget Threshold**: $10B/year in new revenue (from proposed taxes on corporations and wealthy individuals)
- **Monte Carlo Simulation**: 10,000 iterations with probabilistic cost distributions
- **Uncertainty Modeling**: Each policy cost is modeled with mean and standard deviation to reflect estimation uncertainty
- **Scenario Analysis**: Optimistic, base case, and pessimistic scenarios
- **Sensitivity Analysis**: Tests which policies drive the most fiscal risk

## Files

- **`Monte-Carlo-Simulation.ipynb`**: Complete Jupyter notebook with all analysis, code, and visualizations
- **`Research.md`**: Detailed research on Mamdani's policy proposals and methodology
- **`.gitignore`**: Excludes sensitive files and development artifacts

## Key Questions Answered

- What is the probability that Mamdani's agenda is affordable within the $10B budget threshold?
- Which policies contribute the most to fiscal uncertainty?
- How sensitive is affordability to changes in key assumptions (childcare costs, housing financing, etc.)?
- What would happen if only a subset of policies were implemented?

## Results

The notebook provides:
- Summary statistics on total costs and affordability probability
- Visualizations showing cost distributions vs. budget threshold
- Per-policy cost breakdowns and variance contributions
- Scenario comparisons across different assumption sets
- Human-readable interpretation of fiscal feasibility

For detailed research and policy background, see [`Research.md`](Research.md).

---

**Note**: This is an independent analytical project and is not affiliated with any political campaign or organization.
