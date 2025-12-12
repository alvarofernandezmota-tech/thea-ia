"""
Shared Context System
Sistema de contexto compartido para coordinación entre agentes.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from threading import Lock
import json


@dataclass
class ContextEntry:
    """Entrada en el contexto compartido"""
    key: str
    value: Any
    owner_agent_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    ttl_seconds: Optional[int] = None
    subscribers: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if entry has expired"""
        if self.ttl_seconds is None:
            return False
        age = (datetime.utcnow() - self.updated_at).total_seconds()
        return age > self.ttl_seconds
    
    def update_value(self, new_value: Any) -> None:
        """Update entry value"""
        self.value = new_value
        self.updated_at = datetime.utcnow()


class SharedContext:
    """Sistema de contexto compartido entre agentes"""
    
    def __init__(self):
        self._context: Dict[str, ContextEntry] = {}
        self._agent_keys: Dict[str, Set[str]] = {}  # agent_id -> keys owned
        self._lock = Lock()
        self._history: List[Dict[str, Any]] = []
        self._max_history_size = 1000
    
    def set(
        self,
        key: str,
        value: Any,
        agent_id: str,
        ttl_seconds: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Establecer valor en contexto"""
        with self._lock:
            if key in self._context:
                entry = self._context[key]
                # Solo el owner puede actualizar
                if entry.owner_agent_id != agent_id:
                    return False
                entry.update_value(value)
                if metadata:
                    entry.metadata.update(metadata)
            else:
                entry = ContextEntry(
                    key=key,
                    value=value,
                    owner_agent_id=agent_id,
                    ttl_seconds=ttl_seconds,
                    metadata=metadata or {}
                )
                self._context[key] = entry
                
                if agent_id not in self._agent_keys:
                    self._agent_keys[agent_id] = set()
                self._agent_keys[agent_id].add(key)
            
            self._add_to_history("set", key, agent_id, value)
            return True
    
    def get(self, key: str, agent_id: Optional[str] = None) -> Optional[Any]:
        """Obtener valor del contexto"""
        with self._lock:
            if key not in self._context:
                return None
            
            entry = self._context[key]
            if entry.is_expired():
                self._remove_entry(key)
                return None
            
            if agent_id:
                self._add_to_history("get", key, agent_id, entry.value)
            
            return entry.value
    
    def get_entry(self, key: str) -> Optional[ContextEntry]:
        """Obtener entrada completa del contexto"""
        with self._lock:
            entry = self._context.get(key)
            if entry and entry.is_expired():
                self._remove_entry(key)
                return None
            return entry
    
    def delete(self, key: str, agent_id: str) -> bool:
        """Eliminar entrada del contexto"""
        with self._lock:
            if key not in self._context:
                return False
            
            entry = self._context[key]
            if entry.owner_agent_id != agent_id:
                return False
            
            self._remove_entry(key)
            self._add_to_history("delete", key, agent_id, None)
            return True
    
    def _remove_entry(self, key: str) -> None:
        """Remover entrada internamente (sin lock)"""
        if key in self._context:
            entry = self._context[key]
            del self._context[key]
            
            if entry.owner_agent_id in self._agent_keys:
                self._agent_keys[entry.owner_agent_id].discard(key)
    
    def subscribe(self, key: str, agent_id: str) -> bool:
        """Suscribirse a cambios en una key"""
        with self._lock:
            if key not in self._context:
                return False
            
            self._context[key].subscribers.add(agent_id)
            return True
    
    def unsubscribe(self, key: str, agent_id: str) -> bool:
        """Desuscribirse de una key"""
        with self._lock:
            if key not in self._context:
                return False
            
            self._context[key].subscribers.discard(agent_id)
            return True
    
    def get_subscribers(self, key: str) -> Set[str]:
        """Obtener suscriptores de una key"""
        with self._lock:
            if key not in self._context:
                return set()
            return self._context[key].subscribers.copy()
    
    def get_agent_keys(self, agent_id: str) -> Set[str]:
        """Obtener keys de un agente"""
        with self._lock:
            return self._agent_keys.get(agent_id, set()).copy()
    
    def cleanup_expired(self) -> List[str]:
        """Limpiar entradas expiradas"""
        with self._lock:
            expired_keys = []
            for key, entry in list(self._context.items()):
                if entry.is_expired():
                    self._remove_entry(key)
                    expired_keys.append(key)
            return expired_keys
    
    def clear_agent_context(self, agent_id: str) -> int:
        """Limpiar todo el contexto de un agente"""
        with self._lock:
            keys = self._agent_keys.get(agent_id, set()).copy()
            for key in keys:
                self._remove_entry(key)
            return len(keys)
    
    def export_context(self, keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """Exportar contexto como dict"""
        with self._lock:
            if keys is None:
                keys = list(self._context.keys())
            
            result = {}
            for key in keys:
                if key in self._context:
                    entry = self._context[key]
                    if not entry.is_expired():
                        result[key] = {
                            "value": entry.value,
                            "owner": entry.owner_agent_id,
                            "created_at": entry.created_at.isoformat(),
                            "updated_at": entry.updated_at.isoformat(),
                            "metadata": entry.metadata
                        }
            return result
    
    def import_context(self, data: Dict[str, Dict[str, Any]], agent_id: str) -> int:
        """Importar contexto desde dict"""
        count = 0
        for key, entry_data in data.items():
            if self.set(
                key=key,
                value=entry_data.get("value"),
                agent_id=agent_id,
                metadata=entry_data.get("metadata")
            ):
                count += 1
        return count
    
    def get_statistics(self) -> Dict[str, int]:
        """Obtener estadísticas del contexto"""
        with self._lock:
            return {
                "total_entries": len(self._context),
                "total_agents": len(self._agent_keys),
                "total_history": len(self._history)
            }
    
    def _add_to_history(self, action: str, key: str, agent_id: str, value: Any) -> None:
        """Agregar acción al historial"""
        self._history.append({
            "action": action,
            "key": key,
            "agent_id": agent_id,
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        if len(self._history) > self._max_history_size:
            self._history = self._history[-self._max_history_size:]
    
    def get_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtener historial de acciones"""
        with self._lock:
            return self._history[-limit:]
