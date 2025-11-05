import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';
import FaqMDX from '@/content/docs/faq.mdx';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'FAQ',
  description: 'Questions fréquentes',
  openGraph: {
    title: 'FAQ - Documentation eBook Scene Packer v2',
    description: 'Questions fréquentes',
    url: `${baseUrl}/docs/faq`,
    type: 'article',
  },
};

export default function FaqPage() {
  return (
    <DocsLayout>
      <FaqMDX />
    </DocsLayout>
  );
}

