/**
 * Composant JsonLd pour structured data (SEO).
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et les standards Schema.org pour le SEO.
 */

interface JsonLdProps {
  data: Record<string, unknown>;
}

export function JsonLd({ data }: JsonLdProps) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
