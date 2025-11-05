"""Mixins pour modèles SQLAlchemy."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from web.extensions import db


class TimestampMixin:
    """Mixin pour ajouter created_at et updated_at automatiquement.
    
    Ce mixin suit les meilleures pratiques Context7 pour Flask-SQLAlchemy.
    Utilise datetime.now(timezone.utc) au lieu de datetime.utcnow() (deprecated Python 3.12+).
    
    Utilisation :
        class Rule(TimestampMixin, db.Model):
            id: Mapped[int] = mapped_column(primary_key=True)
            name: Mapped[str] = mapped_column(db.String(200), nullable=False)
            # created_at et updated_at automatiquement ajoutés
    """
    
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

