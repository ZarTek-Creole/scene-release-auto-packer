import { DocsLayout } from '@/components/docs/DocsLayout';
import type { Metadata } from 'next';

const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://ebook-scene-packer.example.com';

export const metadata: Metadata = {
  title: 'Documentation',
  description: 'Documentation complète de l\'application eBook Scene Packer v2',
  openGraph: {
    title: 'Documentation - eBook Scene Packer v2',
    description: 'Documentation complète de l\'application eBook Scene Packer v2',
    url: `${baseUrl}/docs`,
    type: 'website',
  },
  twitter: {
    card: 'summary',
    title: 'Documentation - eBook Scene Packer v2',
    description: 'Documentation complète de l\'application eBook Scene Packer v2',
  },
};

export default function DocsPage() {
  return (
    <DocsLayout>
      <h1>Documentation</h1>
      <p>
        Bienvenue dans la documentation d'eBook Scene Packer v2.
      </p>
      <p>
        Cette application permet de créer automatiquement des packages de releases eBook
        conformes aux règles Scene.
      </p>
      <h2>Vue d'ensemble</h2>
      <p>
        eBook Scene Packer v2 est une application moderne développée avec Flask (backend)
        et React 19 (frontend), permettant de créer et gérer des releases eBook selon les
        standards Scene.
      </p>
      <h2>Fonctionnalités principales</h2>
      <ul>
        <li>
          <strong>Wizard 9 étapes</strong> : Création guidée de releases avec validation
          automatique
        </li>
        <li>
          <strong>Gestion des releases</strong> : Liste, recherche, filtres, édition,
          suppression
        </li>
        <li>
          <strong>Rules Management</strong> : Gestion des règles Scene locales et
          téléchargement depuis scenerules.org
        </li>
        <li>
          <strong>Utilisateurs & Rôles</strong> : Système de permissions granulaires
        </li>
        <li>
          <strong>Configurations</strong> : Gestion des APIs externes et destinations
          FTP/SSH
        </li>
      </ul>
      <h2>Navigation</h2>
      <p>
        Utilisez la barre latérale pour naviguer dans la documentation. Vous trouverez :
      </p>
      <ul>
        <li>
          <strong>Installation</strong> : Guide complet d'installation et configuration
        </li>
        <li>
          <strong>Démarrage rapide</strong> : Guide rapide pour commencer
        </li>
        <li>
          <strong>Architecture</strong> : Détails techniques de l'architecture
        </li>
        <li>
          <strong>API Reference</strong> : Documentation complète de l'API REST
        </li>
        <li>
          <strong>Guides</strong> : Guides pratiques (déploiement, performance, sécurité)
        </li>
        <li>
          <strong>Exemples</strong> : Exemples d'utilisation
        </li>
        <li>
          <strong>FAQ</strong> : Questions fréquentes
        </li>
      </ul>
    </DocsLayout>
  );
}

