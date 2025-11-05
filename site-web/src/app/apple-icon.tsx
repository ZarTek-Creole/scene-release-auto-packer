/**
 * Génération de favicon Apple Touch Icon pour Next.js 15.
 *
 * Ce fichier génère un Apple Touch Icon pour iOS.
 * Suit les meilleures pratiques Next.js 15 App Router.
 */

import { ImageResponse } from 'next/og';

export const size = {
  width: 180,
  height: 180,
};

export const contentType = 'image/png';

export default function AppleIcon() {
  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 64,
          background: 'linear-gradient(135deg, #0d6efd 0%, #084298 100%)',
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontWeight: 'bold',
        }}
      >
        📚
      </div>
    ),
    {
      ...size,
    }
  );
}

