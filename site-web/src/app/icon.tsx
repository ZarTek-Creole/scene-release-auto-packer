/**
 * Génération de favicon pour Next.js 15.
 *
 * Ce fichier génère un favicon programmatiquement en utilisant ImageResponse.
 * Suit les meilleures pratiques Next.js 15 App Router.
 */

import { ImageResponse } from 'next/og';

export const size = {
  width: 32,
  height: 32,
};

export const contentType = 'image/png';

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 24,
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

