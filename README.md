# E-commerce Conversion A/B Test Project

## Overview

This project demonstrates how experimental design and data-driven decision making can be applied in an e-commerce environment.

Using customer behavior data, the project simulates an A/B testing scenario to compare the performance of two user groups and evaluate whether a product, UI, or marketing change leads to measurable business improvement.

The objective is to determine whether the new variation (Group B) delivers statistically meaningful uplift compared with the control group (Group A).

---

## Business Question

Can a product or experience change improve customer conversion performance?

Examples include:

- Purchase conversion rate improvement
- Add-to-cart rate increase
- Checkout completion uplift
- Revenue per visitor optimization
- User engagement improvement

---

## Project Goals

- Design a realistic A/B testing framework
- Compare key performance metrics between two groups
- Evaluate uplift and statistical significance
- Provide clear business recommendations based on results
- Visualize findings for decision makers

---

## Dataset

Publicly available e-commerce customer behavior dataset.

Possible variables:

- user_id
- session_id
- device_type
- traffic_source
- viewed_product
- add_to_cart
- purchased
- purchase_amount
- experiment_group (A / B)

---

## Methodology

### 1. Data Preparation

- Clean missing values
- Validate experiment groups
- Remove duplicate sessions
- Define conversion events

### 2. KPI Definition

Primary metrics:

- Conversion Rate
- Add-to-Cart Rate
- Average Order Value
- Revenue per User

### 3. Statistical Testing

Methods may include:

- Two-proportion z-test
- Chi-square test
- T-test
- Confidence Interval Analysis

### 4. Interpretation

- Is the uplift statistically significant?
- Is the business impact meaningful?
- Should Group B be adopted?

---

## (Example) Output: Work In Progress...

| Metric | Group A | Group B | Result |
|-------|--------|--------|--------|
| Conversion Rate | 4.8% | 5.5% | +14.6% uplift |
| Add-to-Cart Rate | 11.2% | 12.6% | Improved |
| Revenue per User | $8.40 | $9.05 | Increased |

---

## Tools Used

- Python
- Pandas
- NumPy
- SciPy / Statsmodels
- Matplotlib / Seaborn
- Jupyter Notebook

---

## Key Takeaways

This project highlights how experimentation can support smarter business decisions by replacing intuition with measurable evidence.

A/B testing is one of the most practical ways to optimize user experience, improve conversion, and guide product or marketing strategy.

---

## Folder Structure

```text
ecommerce_ab_test_project/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── ab_test_analysis.ipynb
├── outputs/
│   ├── charts/
│   └── tables/
├── src/
│   └── utils.py
├── README.md
└── requirements.txt
```

---

## Future Improvements
- Segment-level experiment analysis
- Mobile vs Desktop comparison
- Traffic source performance analysis
- Bayesian A/B testing
- Sequential testing methods

---

## Author

Ji-Eun Son

Business, Data & AI Portfolio Project
