import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Guides - Documentation eBook Scene Packer v2',
  description: 'Guides pratiques pour déploiement, performance, sécurité, monitoring',
};

export default function GuidesPage() {
  return (
    <DocsLayout>
      <h1>Guides</h1>
      <p>
        Guides pratiques pour utiliser et déployer eBook Scene Packer v2.
      </p>
      <h2>Guides disponibles</h2>
      <ul>
        <li>
          <a href="/docs/guides/deployment">Déploiement</a> : Guide complet pour déployer en production
        </li>
        <li>
          <a href="/docs/guides/performance">Performance</a> : Optimisations et meilleures pratiques
        </li>
        <li>
          <a href="/docs/guides/security">Sécurité</a> : Meilleures pratiques de sécurité
        </li>
        <li>
          <a href="/docs/guides/monitoring">Monitoring</a> : Monitoring et observabilité
        </li>
      </ul>
    </DocsLayout>
  );
}

