/**
 * Layout pour pages de documentation.
 *
 * Ce composant suit les meilleures pratiques Next.js 15 App Router
 * et le Design System du projet (Bootstrap 5, Bootstrap Icons).
 */

import { ReactNode } from 'react';
import { DocsSidebar } from '@/components/docs/DocsSidebar';
import { DocsBreadcrumb } from '@/components/docs/DocsBreadcrumb';
import { DocsSearch } from '@/components/docs/DocsSearch';

interface DocsLayoutProps {
  children: ReactNode;
}

export function DocsLayout({ children }: DocsLayoutProps) {
  return (
    <div className="docs-container">
      <div className="docs-sidebar-wrapper">
        <DocsSearch />
        <DocsSidebar />
      </div>
      <main className="docs-main">
        <DocsBreadcrumb />
        <article className="docs-content">{children}</article>
      </main>
    </div>
  );
}

