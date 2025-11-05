import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';
import InstallationMDX from '@/content/docs/installation.mdx';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Installation',
  description: 'Guide complet d\'installation et de configuration',
  openGraph: {
    title: 'Installation - Documentation eBook Scene Packer v2',
    description: 'Guide complet d\'installation et de configuration',
    url: `${baseUrl}/docs/installation`,
    type: 'article',
  },
};

export default function InstallationPage() {
  return (
    <DocsLayout>
      <InstallationMDX />
    </DocsLayout>
  );
}
