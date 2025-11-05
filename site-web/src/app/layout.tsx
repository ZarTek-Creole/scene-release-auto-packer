import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import '@/styles/globals.css';
import { Header } from '@/components/Header';

const inter = Inter({ subsets: ['latin'] });

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: 'eBook Scene Packer v2 - Packaging Automatique de Releases eBook',
    template: '%s | eBook Scene Packer v2',
  },
  description:
    'Application moderne pour packaging automatique de releases eBook selon les règles Scene. Wizard 9 étapes, conformité stricte, génération NFO automatique.',
  keywords: [
    'ebook',
    'scene',
    'packaging',
    'automation',
    'nfo',
    'wizard',
    'scene rules',
    'ebook release',
    'packaging tool',
  ],
  authors: [{ name: 'eBook Scene Packer Team' }],
  creator: 'eBook Scene Packer Team',
  publisher: 'eBook Scene Packer Team',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: 'website',
    locale: 'fr_FR',
    url: baseUrl,
    siteName: 'eBook Scene Packer v2',
    title: 'eBook Scene Packer v2 - Packaging Automatique de Releases eBook',
    description:
      'Application moderne pour packaging automatique de releases eBook selon les règles Scene. Wizard 9 étapes, conformité stricte, génération NFO automatique.',
    images: [
      {
        url: `${baseUrl}/og-image.png`,
        width: 1200,
        height: 630,
        alt: 'eBook Scene Packer v2',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'eBook Scene Packer v2',
    description:
      'Application moderne pour packaging automatique de releases eBook selon les règles Scene.',
    images: [`${baseUrl}/og-image.png`],
    creator: '@ebookscenepacker',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  alternates: {
    canonical: baseUrl,
  },
  verification: {
    // À ajouter lors du déploiement
    // google: 'your-google-verification-code',
    // yandex: 'your-yandex-verification-code',
    // bing: 'your-bing-verification-code',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" data-theme="light">
      <body className={inter.className}>
        <a href="#main-content" className="skip-link">
          Aller au contenu principal
        </a>
        <Header />
        <main id="main-content">{children}</main>
      </body>
    </html>
  );
}
