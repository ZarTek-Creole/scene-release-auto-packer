import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';
import QuickStartMDX from '@/content/docs/quick-start.mdx';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Démarrage rapide',
  description: 'Guide rapide pour démarrer avec eBook Scene Packer v2',
  openGraph: {
    title: 'Démarrage rapide - Documentation eBook Scene Packer v2',
    description: 'Guide rapide pour démarrer avec eBook Scene Packer v2',
    url: `${baseUrl}/docs/quick-start`,
    type: 'article',
  },
};

export default function QuickStartPage() {
  return (
    <DocsLayout>
      <QuickStartMDX />
    </DocsLayout>
  );
}
