---
id: 7f3a8b2c-1d4e-5f6a-9b0c-2d3e4f5a6b7c
type: preference
created: 2026-01-15T10:30:00Z
modified: 2026-01-20T14:22:00Z
namespace: acme-corp/jane-doe/project-x
title: "Dark Mode UI Preference"
tags:
  - preference
  - ui
  - accessibility
aliases:
  - "Dark Mode Preference"
  - "UI Theme Choice"

temporal:
  valid_from: 2026-01-15T00:00:00Z
  valid_until: null
  recorded_at: 2026-01-15T10:30:00Z
  ttl: P365D
  decay:
    model: exponential
    half_life: P30D
    strength: 0.92
    last_reinforced: 2026-01-20T14:22:00Z
  access_count: 8
  last_accessed: 2026-01-20T14:22:00Z

provenance:
  source_type: user_explicit
  source_ref: conversation:conv-2026-01-15-001
  agent: claude-3-opus
  agent_version: "20240229"
  confidence: 0.98
  trust_level: user_stated

embedding:
  model: text-embedding-3-small
  model_version: "2024-01"
  dimensions: 1536
  source_text: "User prefers dark mode for all applications including IDE, terminal, and web apps"
  normalized: true

extensions:
  subcog:
    domain: user
    hash: "sha256:4c04b32ddc2053b5a8f9e2d1c0b7a6e5d4c3b2a1"
---

# Dark Mode UI Preference

User strongly prefers dark mode for all applications. ^main-preference

## Details

This preference applies to: ^details

- **IDE/Editor**: VS Code, JetBrains IDEs
- **Terminal**: iTerm2, built-in terminal
- **Web applications**: GitHub, documentation sites
- **Mobile apps**: When available

## Context

User mentioned eye strain with light themes during extended coding sessions. Dark mode reduces eye fatigue and is preferred for:

- Late-night coding sessions
- Low-light environments
- General aesthetic preference

## Reinforcement History

This preference has been confirmed multiple times:

1. 2026-01-15: Initial statement during onboarding
2. 2026-01-16: Confirmed when setting up VS Code
3. 2026-01-18: Applied to terminal configuration
4. 2026-01-20: Extended to web application preferences

## Relationships

- relates-to [[ide-configuration-preferences]]
- relates-to [[terminal-setup]]
- part-of [[user-jane-doe-profile]]

## Entities

- @[[Jane Doe|Person]]
- @[[VS Code|Technology]]
- @[[Dark Mode|Concept]]
- @[[Accessibility|Concept]]
