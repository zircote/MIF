# MIF Namespace

This directory serves as the namespace anchor for MIF JSON-LD vocabulary terms.

The URL `https://raw.githubusercontent.com/zircote/MIF/main/ns/` is used as a prefix in JSON-LD contexts to create IRIs (Internationalized Resource Identifiers) for MIF-specific terms.

## Usage in JSON-LD Context

```json
{
  "@context": {
    "mif": "https://raw.githubusercontent.com/zircote/MIF/main/ns/",
    "Memory": "mif:Memory",
    "memoryType": "mif:memoryType"
  }
}
```

This creates IRIs like:
- `https://raw.githubusercontent.com/zircote/MIF/main/ns/Memory`
- `https://raw.githubusercontent.com/zircote/MIF/main/ns/memoryType`

## Note

JSON-LD namespace prefixes are identifiers for vocabulary terms. While they form valid URLs, they don't need to resolve to actual content—they serve as unique identifiers in the semantic web.
