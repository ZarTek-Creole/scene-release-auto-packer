import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';
import PerformanceMDX from '@/content/docs/guides/performance.mdx';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Guide de Performance',
  description: 'Conseils et techniques pour optimiser les performances de l\'application.',
  openGraph: {
    title: 'Guide de Performance - Documentation eBook Scene Packer v2',
    description: 'Conseils et techniques pour optimiser les performances de l\'application.',
    url: `${baseUrl}/docs/guides/performance`,
    type: 'article',
  },
};

export default function PerformanceGuidePage() {
  return (
    <DocsLayout>
      <PerformanceMDX />
    </DocsLayout>
  );
}

