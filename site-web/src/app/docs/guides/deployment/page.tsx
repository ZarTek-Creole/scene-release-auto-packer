import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';
import DeploymentMDX from '@/content/docs/guides/deployment.mdx';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Guide de Déploiement',
  description: 'Instructions détaillées pour le déploiement en production.',
  openGraph: {
    title: 'Guide de Déploiement - Documentation eBook Scene Packer v2',
    description: 'Instructions détaillées pour le déploiement en production.',
    url: `${baseUrl}/docs/guides/deployment`,
    type: 'article',
  },
};

export default function DeploymentGuidePage() {
  return (
    <DocsLayout>
      <DeploymentMDX />
    </DocsLayout>
  );
}

