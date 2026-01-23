---
# Image generation provider
provider: svg

# SVG-specific settings
svg_style: illustrated

# Dark mode support
# false = light mode only, true = dark mode only, both = generate both variants
dark_mode: both

# Output settings
output_path: .github/social-preview.svg
dimensions: 1280x640
include_text: true
colors: auto

# README infographic settings
infographic_output: .github/readme-infographic.svg
infographic_style: hybrid

# Upload to repository (requires gh CLI)
upload_to_repo: false
---

# GitHub Social Plugin Configuration

This configuration was created by `/github-social:setup`.

## Current Settings

| Setting | Value |
|---------|-------|
| Provider | SVG (free, instant) |
| Style | Illustrated (organic paths, hand-drawn aesthetic) |
| Dark Mode | Both variants |
| Output | `.github/social-preview.svg` |

## SVG Style: Illustrated

The illustrated style creates:
- Organic SVG paths with flowing, natural curves
- Hand-drawn aesthetic with warm colors
- Visual metaphors for the project domain
- Approachable, friendly appearance

## Dark Mode: Both

Two files will be generated:
- `.github/social-preview.svg` (light mode)
- `.github/social-preview-dark.svg` (dark mode)

## Commands

Generate social preview:
```
/github-social:social-preview
```

Enhance README with badges and infographic:
```
/github-social:readme-enhance
```

Run all skills:
```
/github-social:all
```

## Modifying Settings

Edit this file or run `/github-social:setup` again.
