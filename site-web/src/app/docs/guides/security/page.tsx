import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';
import SecurityMDX from '@/content/docs/guides/security.mdx';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Guide de Sécurité',
  description: 'Bonnes pratiques et configurations pour sécuriser l\'application.',
  openGraph: {
    title: 'Guide de Sécurité - Documentation eBook Scene Packer v2',
    description: 'Bonnes pratiques et configurations pour sécuriser l\'application.',
    url: `${baseUrl}/docs/guides/security`,
    type: 'article',
  },
};

export default function SecurityGuidePage() {
  return (
    <DocsLayout>
      <SecurityMDX />
    </DocsLayout>
  );
}

