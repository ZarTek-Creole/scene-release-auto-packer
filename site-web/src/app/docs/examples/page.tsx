import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';
import ExamplesMDX from '@/content/docs/examples.mdx';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Exemples',
  description: 'Exemples d\'utilisation de l\'API',
  openGraph: {
    title: 'Exemples - Documentation eBook Scene Packer v2',
    description: 'Exemples d\'utilisation de l\'API',
    url: `${baseUrl}/docs/examples`,
    type: 'article',
  },
};

export default function ExamplesPage() {
  return (
    <DocsLayout>
      <ExamplesMDX />
    </DocsLayout>
  );
}

