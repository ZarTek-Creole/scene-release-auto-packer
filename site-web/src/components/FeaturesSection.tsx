/**
 * Composant FeaturesSection pour afficher les fonctionnalités principales.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 */

import { FeatureCard } from './FeatureCard';

const features = [
  {
    icon: 'magic',
    title: 'Wizard 9 Étapes',
    description:
      'Processus guidé en 9 étapes pour créer des releases conformes aux règles Scene. '
      + 'Validation automatique à chaque étape avec feedback visuel instantané. '
      + 'Interface intuitive qui guide pas à pas de la sélection du groupe jusqu\'à la finalisation.',
    link: '/docs/architecture',
  },
  {
    icon: 'file-earmark-check',
    title: 'Conformité Scene',
    description:
      'Validation automatique selon les règles Scene officielles. '
      + 'Intégration avec scenerules.org pour télécharger les règles à jour. '
      + 'Gestion des règles locales avec support de règles personnalisées.',
    link: '/docs/guides/security',
  },
  {
    icon: 'file-text',
    title: 'Génération NFO',
    description:
      'Génération automatique de fichiers NFO conformes aux standards Scene. '
      + 'Templates personnalisables avec aperçu en temps réel. '
      + 'Support de multiples formats et encodages.',
    link: '/docs/api',
  },
  {
    icon: 'people',
    title: 'Gestion Utilisateurs',
    description:
      'Système complet de gestion d\'utilisateurs avec rôles et permissions granulaires. '
      + 'Support multi-utilisateurs avec audit trail complet. '
      + 'Gestion des groupes et équipes.',
    link: '/docs/architecture',
  },
  {
    icon: 'sliders',
    title: 'Configurations',
    description:
      'Configuration flexible des destinations FTP/SSH, APIs d\'enrichissement, '
      + 'et règles de packaging. Support de multiples environnements. '
      + 'Gestion centralisée des configurations.',
    link: '/docs/guides/deployment',
  },
  {
    icon: 'graph-up',
    title: 'Dashboard & Statistiques',
    description:
      'Tableau de bord complet avec statistiques en temps réel. '
      + 'Suivi des releases et des jobs de packaging. '
      + 'Graphiques et métriques détaillées pour une vue d\'ensemble optimale.',
    link: '/features',
  },
];

export function FeaturesSection() {
  return (
    <section className="features-section py-5 bg-light">
      <div className="container">
        <div className="text-center mb-5">
          <h2 className="display-5 fw-bold mb-3">Fonctionnalités Principales</h2>
          <p className="lead text-muted">
            Tout ce dont vous avez besoin pour créer des releases eBook conformes
            aux règles Scene. Des outils puissants et une interface intuitive pour
            un packaging professionnel.
          </p>
        </div>

        <div className="row g-4">
          {features.map((feature) => (
            <div key={feature.icon} className="col-md-6 col-lg-4">
              <FeatureCard
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
                link={feature.link}
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
