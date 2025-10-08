# ESQUEMAS BASE DE DATOS - THEA IA 2.0

## 🗄️ Diseño de Tablas PostgreSQL

### Tabla: users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    language_code VARCHAR(10) DEFAULT 'es',
    timezone VARCHAR(50) DEFAULT 'UTC',
    is_active BOOLEAN DEFAULT true,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: events
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    start_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    end_datetime TIMESTAMP WITH TIME ZONE,
    location VARCHAR(500),
    event_type VARCHAR(50) DEFAULT 'personal', -- personal, work, medical, etc
    status VARCHAR(20) DEFAULT 'active', -- active, cancelled, completed
    reminder_minutes INTEGER DEFAULT 30,
    recurrence_rule VARCHAR(200), -- RRULE format for recurring events
    external_id VARCHAR(255), -- for Google Calendar sync
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: notes
```sql
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500),
    content TEXT NOT NULL,
    category VARCHAR(100) DEFAULT 'general',
    tags TEXT[], -- array of tags
    priority INTEGER DEFAULT 1, -- 1=low, 2=medium, 3=high
    is_pinned BOOLEAN DEFAULT false,
    reminder_datetime TIMESTAMP WITH TIME ZONE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: conversations
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(255) NOT NULL,
    current_state VARCHAR(50) NOT NULL,
    context_data JSONB DEFAULT '{}',
    last_message_id VARCHAR(255),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);
```

### Tabla: message_history
```sql
CREATE TABLE message_history (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    message_id VARCHAR(255) NOT NULL,
    user_message TEXT,
    bot_response TEXT,
    intent_detected VARCHAR(100),
    entities_extracted JSONB DEFAULT '{}',
    confidence_score FLOAT,
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: notifications
```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL, -- reminder, cancellation, update
    scheduled_for TIMESTAMP WITH TIME ZONE NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'pending', -- pending, sent, failed
    retry_count INTEGER DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔗 Relaciones y Constraints

### Índices recomendados
```sql
-- Usuarios
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;

-- Eventos
CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_datetime ON events(start_datetime);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_user_datetime ON events(user_id, start_datetime);

-- Notas
CREATE INDEX idx_notes_user_id ON notes(user_id);
CREATE INDEX idx_notes_created_at ON notes(created_at);
CREATE INDEX idx_notes_tags ON notes USING GIN(tags);
CREATE INDEX idx_notes_pinned ON notes(is_pinned) WHERE is_pinned = true;

-- Conversaciones
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_session_id ON conversations(session_id);
CREATE INDEX idx_conversations_active ON conversations(is_active) WHERE is_active = true;

-- Historial mensajes
CREATE INDEX idx_message_history_conversation_id ON message_history(conversation_id);
CREATE INDEX idx_message_history_created_at ON message_history(created_at);

-- Notificaciones
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_scheduled_for ON notifications(scheduled_for);
CREATE INDEX idx_notifications_status ON notifications(status);
```

### Triggers para updated_at
```sql
-- Función para actualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para cada tabla
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_events_updated_at BEFORE UPDATE ON events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notes_updated_at BEFORE UPDATE ON notes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## 🏗️ Modelos SQLAlchemy (Python)

### Modelo User
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BIGINT, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BIGINT, unique=True, nullable=False)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    language_code = Column(String(10), default='es')
    timezone = Column(String(50), default='UTC')
    is_active = Column(Boolean, default=True)
    preferences = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user")
```

### Modelo Event
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship
from .base import Base

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime)
    location = Column(String(500))
    event_type = Column(String(50), default='personal')
    status = Column(String(20), default='active')
    reminder_minutes = Column(Integer, default=30)
    recurrence_rule = Column(String(200))
    external_id = Column(String(255))
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = relationship("User", back_populates="events")
    notifications = relationship("Notification", back_populates="event")
```

### Modelo Note
```python
class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(500))
    content = Column(Text, nullable=False)
    category = Column(String(100), default='general')
    tags = Column(ARRAY(Text))
    priority = Column(Integer, default=1)
    is_pinned = Column(Boolean, default=False)
    reminder_datetime = Column(DateTime)
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = relationship("User", back_populates="notes")
```

---

## 📊 Mapeo Entidad-Relación (ER)

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    USERS    │──────▶│   EVENTS    │──────▶│NOTIFICATIONS│
│             │ 1:N   │             │ 1:N   │             │
│ • id (PK)   │       │ • id (PK)   │       │ • id (PK)   │
│ • telegram_id│       │ • user_id(FK)│       │ • event_id(FK)│
│ • username  │       │ • title     │       │ • scheduled │
│ • first_name│       │ • start_dt  │       │ • sent_at   │
│ • language  │       │ • location  │       │ • status    │
│ • timezone  │       │ • status    │       └─────────────┘
│ • preferences│       │ • metadata  │
└─────────────┘       └─────────────┘
       │
       │ 1:N
       ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    NOTES    │       │CONVERSATIONS│──────▶│MESSAGE_HIST │
│             │       │             │ 1:N   │             │
│ • id (PK)   │       │ • id (PK)   │       │ • id (PK)   │
│ • user_id(FK)│       │ • user_id(FK)│       │ • conv_id(FK)│
│ • title     │       │ • session_id│       │ • user_msg  │
│ • content   │       │ • state     │       │ • bot_resp  │
│ • category  │       │ • context   │       │ • intent    │
│ • tags[]    │       │ • is_active │       │ • entities  │
│ • priority  │       └─────────────┘       │ • confidence│
└─────────────┘                             └─────────────┘
```

---

## 🚀 Scripts de Migración Alembic

### Archivo inicial de migración
```python
"""Initial database schema

Revision ID: 001_initial
Revises: 
Create Date: 2025-10-08

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Crear tabla users
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('telegram_id', sa.BIGINT(), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column('first_name', sa.String(length=255), nullable=True),
        sa.Column('last_name', sa.String(length=255), nullable=True),
        sa.Column('language_code', sa.String(length=10), nullable=True),
        sa.Column('timezone', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('telegram_id')
    )
    
    # Crear tabla events
    op.create_table('events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_datetime', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_datetime', sa.DateTime(timezone=True), nullable=True),
        sa.Column('location', sa.String(length=500), nullable=True),
        sa.Column('event_type', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('reminder_minutes', sa.Integer(), nullable=True),
        sa.Column('recurrence_rule', sa.String(length=200), nullable=True),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices
    op.create_index('idx_users_telegram_id', 'users', ['telegram_id'])
    op.create_index('idx_events_user_id', 'events', ['user_id'])
    op.create_index('idx_events_datetime', 'events', ['start_datetime'])

def downgrade():
    op.drop_index('idx_events_datetime')
    op.drop_index('idx_events_user_id') 
    op.drop_index('idx_users_telegram_id')
    op.drop_table('events')
    op.drop_table('users')
```