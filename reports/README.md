---
diataxis_type: reference
---

# Research Reports

This directory contains market research reports generated using the sigint research framework.

## Available Reports

| Report | Topic | Status | Date |
|--------|-------|--------|------|
| [mif-memory-interchange-format](./mif-memory-interchange-format/) | Memory Interchange Format (MIF) - Open Standard for AI Memory Interoperability | Complete | 2026-01-23 |

## Report Structure

Each report directory contains:

```text
report-name/
├── README.md           # Report overview and navigation
├── executive-brief.md  # 1-page decision summary
├── report.md           # Comprehensive analysis
└── trend-models.md     # Scenario modeling (when applicable)
```

## Generating New Reports

Use the sigint research commands:

> **Note:** The `sigint` research framework is an internal tool not included in this repository.
> The commands below are shown for reference; generating new reports requires the sigint plugin.

```bash
# Start a new research session
/sigint:start "Your research topic"

# Check status
/sigint:status

# Deep-dive into specific areas
/sigint:augment "competitor pricing"

# Generate final report
/sigint:report
```

## Research Methodologies

Reports may include analysis using these methodologies:

- **Competitive Analysis** - Market players, positioning, feature comparison
- **Market Sizing** - TAM/SAM/SOM, growth rates, segment analysis
- **Trend Analysis** - Pattern detection, scenario modeling, forecasting
- **Customer Research** - Personas, jobs-to-be-done, pain points
- **Technology Assessment** - Feasibility, architecture, integration
- **Financial Analysis** - Revenue models, unit economics, pricing
- **Regulatory Review** - Compliance requirements, risk assessment
