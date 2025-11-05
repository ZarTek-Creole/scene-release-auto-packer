import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';
import MonitoringMDX from '@/content/docs/guides/monitoring.mdx';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Guide de Monitoring',
  description: 'Mise en place du monitoring avec Structlog, Prometheus et Grafana.',
  openGraph: {
    title: 'Guide de Monitoring - Documentation eBook Scene Packer v2',
    description: 'Mise en place du monitoring avec Structlog, Prometheus et Grafana.',
    url: `${baseUrl}/docs/guides/monitoring`,
    type: 'article',
  },
};

export default function MonitoringGuidePage() {
  return (
    <DocsLayout>
      <MonitoringMDX />
    </DocsLayout>
  );
}

