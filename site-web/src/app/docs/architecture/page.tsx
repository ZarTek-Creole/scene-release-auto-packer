import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';
import ArchitectureMDX from '@/content/docs/architecture.mdx';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Architecture',
  description: 'Vue d\'ensemble de l\'architecture technique',
  openGraph: {
    title: 'Architecture - Documentation eBook Scene Packer v2',
    description: 'Vue d\'ensemble de l\'architecture technique',
    url: `${baseUrl}/docs/architecture`,
    type: 'article',
  },
};

export default function ArchitecturePage() {
  return (
    <DocsLayout>
      <ArchitectureMDX />
    </DocsLayout>
  );
}
