import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import astroMermaid from "astro-mermaid";

export default defineConfig({
  site: "https://mif-spec.dev",
  integrations: [
    astroMermaid(),
    starlight({
      title: "MIF",
      logo: {
        light: "./src/assets/logo-light.svg",
        dark: "./src/assets/logo-dark.svg",
        replacesTitle: true,
      },
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/zircote/MIF",
        },
      ],
      sidebar: [
        {
          label: "Overview",
          items: [{ label: "Introduction", slug: "index" }],
        },
        {
          label: "Specification",
          items: [
            {
              label: "Core",
              items: [
                { label: "Overview", slug: "specification/overview" },
                { label: "File Format", slug: "specification/file-format" },
                { label: "Data Model", slug: "specification/data-model" },
              ],
            },
            {
              label: "Formats",
              items: [
                {
                  label: "Markdown Format",
                  slug: "specification/markdown-format",
                },
                {
                  label: "JSON-LD Format",
                  slug: "specification/json-ld-format",
                },
              ],
            },
            {
              label: "Data Types",
              items: [
                { label: "Entity Types", slug: "specification/entity-types" },
                {
                  label: "Relationship Types",
                  slug: "specification/relationship-types",
                },
              ],
            },
            {
              label: "Features",
              items: [
                {
                  label: "Temporal Model",
                  slug: "specification/temporal-model",
                },
                {
                  label: "Namespace Model",
                  slug: "specification/namespace-model",
                },
                { label: "Embeddings", slug: "specification/embeddings" },
                { label: "Provenance", slug: "specification/provenance" },
              ],
            },
            {
              label: "Reference",
              items: [
                {
                  label: "Conformance Levels",
                  slug: "specification/conformance",
                },
                {
                  label: "JSON-LD Context",
                  slug: "specification/json-ld-context",
                },
                { label: "Conversion Rules", slug: "specification/conversion" },
                { label: "Security", slug: "specification/security" },
                { label: "Appendices", slug: "specification/appendices" },
              ],
            },
          ],
        },
        {
          label: "Guides",
          items: [
            { label: "Getting Started", slug: "guides/getting-started" },
            { label: "Schema Reference", slug: "guides/schema-reference" },
            { label: "API Reference", slug: "guides/api-reference" },
            { label: "Migration", slug: "guides/migration" },
          ],
        },
        {
          label: "Design",
          items: [
            { label: "Architecture Decisions", slug: "design/decisions" },
          ],
        },
      ],
    }),
  ],
});
