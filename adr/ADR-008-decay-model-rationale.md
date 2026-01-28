# ADR-008: Decay Model Rationale

## Status

Accepted

## Date

2026-01-27

## Context

AI memory systems need mechanisms to:
- Prioritize recent/relevant memories
- Deprecate stale information
- Manage memory storage growth
- Model natural forgetting curves

Human memory research shows memories decay over time unless reinforced. This aligns with AI system needs for relevance ranking.

## Decision

Implement a **configurable decay model** with:

### Decay Types
```yaml
decay:
  model: "exponential"  # none | linear | exponential | step
  halfLife: "P14D"      # ISO 8601 duration
  currentStrength: 0.85 # 0.0-1.0
```

### Supported Models

1. **none** - Memory never decays (permanent)
2. **linear** - Strength decreases at constant rate
3. **exponential** - Strength follows exponential decay curve
4. **step** - Strength drops at defined thresholds

### Default Half-Lives by Memory Type

| Memory Type | Default Half-Life | Rationale |
|-------------|-------------------|-----------|
| Semantic | P30D (30 days) | Facts change slowly |
| Episodic | P7D (7 days) | Events become less relevant |
| Procedural | P14D (14 days) | Processes need periodic refresh |

### Reinforcement

Accessing or explicitly reinforcing a memory resets decay:
```yaml
temporal:
  lastAccessed: "2026-01-27T10:00:00Z"
  accessCount: 5
  lastReinforced: "2026-01-25T15:00:00Z"
```

## Consequences

### Positive
- Automatic relevance ranking based on recency
- Storage management via garbage collection of weak memories
- Mirrors human memory behavior (familiar mental model)
- Configurable per memory or per type
- Supports "permanent" memories via `model: none`

### Negative
- Adds complexity to memory management
- Requires background decay calculation
- May accidentally deprecate important memories
- Tuning half-lives requires experimentation

## Implementation Notes

### Decay Calculation
```
currentStrength = initialStrength * (0.5 ^ (elapsed / halfLife))
```

### Garbage Collection Threshold
Memories with `currentStrength < 0.1` are candidates for:
- Archival (move to cold storage)
- Compression (reduce to summary)
- Deletion (with user consent)

### Reinforcement Triggers
- Direct access (read)
- Explicit reinforcement command
- Citation by other memories
- User interaction referencing memory

## References

- Ebbinghaus forgetting curve (1885)
- Spaced repetition research
- ACT-R memory decay model
