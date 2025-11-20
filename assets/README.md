# Visualization Assets

## How to Generate Visuals

1. Open `Monte-Carlo-Simulation.ipynb` in Jupyter
2. Run all cells (Kernel → Restart & Run All)
3. When visualizations appear, right-click each plot and select "Save Image As..."
4. Save to this `/assets` directory with the filenames below

## Required Visualizations

### From Section 7: Visualizations

**Cell 24 - Main Analysis Grid (2x3 layout):**

Extract these individual plots:

1. **`cost_revenue_distribution.png`**
   - Top-left plot: Overlaid histograms of cost (blue) vs revenue (green)
   - Shows the fundamental mismatch between what's needed vs what's available

2. **`opex_capex_breakdown.png`**
   - Top-right plot: Bar chart showing Operating vs Capital expenses
   - Critical for understanding political flexibility in cuts

3. **`revenue_cost_scatter.png`**
   - Bottom-left plot: Scatter plot with green (affordable) and red (deficit) dots
   - Shows correlation between revenue and cost under macro shocks

4. **`scenario_comparison.png`**
   - From Section 8, Cell 29: Bar chart comparing Optimistic/Base/Pessimistic scenarios
   - Shows affordability probability across fiscal scenarios

## Optional (For Deep Dives)

- **`per_policy_breakdown.png`**: Cell 26 - Pie chart showing which policies consume the budget
- **`macro_factor_distribution.png`**: Cell 24 (bottom-right) - Shows economy-wide shock distribution
- **`cdf_comparison.png`**: Cell 24 (middle-bottom) - Cumulative distribution functions

## Notes

- Images should be **high resolution** (at least 1200px wide)
- Use **PNG format** for best quality
- Ensure legends and axis labels are clearly visible
- If matplotlib default DPI is too low, increase with: `plt.savefig('filename.png', dpi=300)`

---

*These visualizations support the README.md findings and make the fiscal math tangible.*