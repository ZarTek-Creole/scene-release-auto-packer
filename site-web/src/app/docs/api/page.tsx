import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';
import ApiMDX from '@/content/docs/api.mdx';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'API Reference',
  description: 'Documentation complète de l\'API REST',
  openGraph: {
    title: 'API Reference - Documentation eBook Scene Packer v2',
    description: 'Documentation complète de l\'API REST',
    url: `${baseUrl}/docs/api`,
    type: 'article',
  },
};

export default function ApiPage() {
  return (
    <DocsLayout>
      <ApiMDX />
    </DocsLayout>
  );
}

