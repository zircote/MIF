---
id: decision-react-frontend
type: semantic
created: 2026-01-10T09:00:00Z
modified: 2026-01-12T14:30:00Z
namespace: _semantic/decisions
title: "Use React for Dashboard Frontend"
tags:
  - frontend
  - architecture
  - technology-choice
aliases:
  - "React Decision"
  - "Frontend Framework Choice"
---

# Use React for Dashboard Frontend

## Context

We need to choose a frontend framework for the new analytics dashboard. The team evaluated React, Vue.js, and Angular.

## Decision

We will use **React** with TypeScript for the dashboard frontend.

### Rationale

- Team has 3+ years of React experience
- Better TypeScript integration than Vue 2.x
- Larger ecosystem for data visualization (Recharts, Victory, Nivo)
- Company standard for new projects

## Consequences

- Set up Vite for build tooling
- Use React Query for server state
- Component library: Radix UI + Tailwind CSS
- Testing: Vitest + React Testing Library

## Relationships

- supersedes [[vue-exploration-2025]]
- relates-to [[frontend-architecture-standards]]
- part-of [[project-x-technical-decisions]]

## Entities

- @[[React|Technology]]
- @[[TypeScript|Technology]]
- @[[Vue.js|Technology]]
- @[[Project X Dashboard|Concept]]
