"""
FSM Context Merging System - H03 Advanced Context Management
Implementa estrategias inteligentes de merge context con windowing.

H03 FASE 1 - BLOQUE 1.2 - TAREA 1.2.2
"""

from typing import Dict, Any, Optional, List, Literal
from enum import Enum
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


class MergeStrategy(Enum):
    """Estrategias de merge para context."""
    OVERWRITE = "overwrite"  # Sobrescribe valores existentes
    APPEND = "append"        # Añade a listas existentes
    MERGE = "merge"          # Combina dicts recursivamente
    WINDOWING = "windowing"  # Mantiene últimos N elementos


class ContextMergingEngine:
    """
    Motor de merge context con múltiples estrategias.
    
    Características H03:
    - Merge strategies (overwrite, append, merge, windowing)
    - Context windowing (últimos N mensajes)
    - Session isolation (contexto por usuario)
    - Smart merge para structures profundas
    - Timestamp tracking
    
    Usage:
        engine = ContextMergingEngine(max_history=10)
        merged = engine.merge(old_context, new_context, strategy="merge")
    """
    
    def __init__(self, max_history: int = 10):
        """
        Inicializa engine de merging.
        
        Args:
            max_history: Máximo de elementos históricos a mantener
        """
        self.max_history = max_history
        logger.debug(f"[ContextMergingEngine] Initialized with max_history={max_history}")
    
    # ==================== MERGE STRATEGIES ====================
    
    def merge(self, 
              old_context: Dict[str, Any], 
              new_context: Dict[str, Any],
              strategy: Literal["overwrite", "append", "merge", "windowing"] = "merge") -> Dict[str, Any]:
        """
        Merges dos contexts usando estrategia especificada.
        
        Args:
            old_context: Context existente
            new_context: Context nuevo a mergear
            strategy: Estrategia de merge
            
        Returns:
            Context mergeado
        """
        if strategy == MergeStrategy.OVERWRITE.value or strategy == "overwrite":
            return self._merge_overwrite(old_context, new_context)
        elif strategy == MergeStrategy.APPEND.value or strategy == "append":
            return self._merge_append(old_context, new_context)
        elif strategy == MergeStrategy.MERGE.value or strategy == "merge":
            return self._merge_recursive(old_context, new_context)
        elif strategy == MergeStrategy.WINDOWING.value or strategy == "windowing":
            return self._merge_windowing(old_context, new_context)
        else:
            logger.warning(f"[ContextMergingEngine] Unknown strategy '{strategy}', using 'merge'")
            return self._merge_recursive(old_context, new_context)
    
    def _merge_overwrite(self, old_context: Dict[str, Any], new_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        OVERWRITE: Sobrescribe valores existentes con nuevos.
        
        Estrategia simple: old + new (new gana)
        """
        result = dict(old_context)
        result.update(new_context)
        logger.debug(f"[ContextMergingEngine] Overwrite merge: {len(new_context)} new fields")
        return result
    
    def _merge_append(self, old_context: Dict[str, Any], new_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        APPEND: Añade valores nuevos a listas existentes.
        
        Para listas: old_list + new_list
        Para otros: sobrescribe
        """
        result = dict(old_context)
        
        for key, new_value in new_context.items():
            if key in result and isinstance(result[key], list) and isinstance(new_value, list):
                # Append a listas existentes (evitar duplicados)
                result[key] = list(set(result[key] + new_value))
            else:
                # Sobrescribir para otros tipos
                result[key] = new_value
        
        logger.debug(f"[ContextMergingEngine] Append merge: lists merged")
        return result
    
    def _merge_recursive(self, old_context: Dict[str, Any], new_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        MERGE: Combina dicts recursivamente.
        
        Para dicts: merge recursivo
        Para listas: append
        Para otros: sobrescribe
        """
        result = dict(old_context)
        
        for key, new_value in new_context.items():
            if key in result:
                old_value = result[key]
                
                # Ambos son dicts: merge recursivo
                if isinstance(old_value, dict) and isinstance(new_value, dict):
                    result[key] = self._merge_recursive(old_value, new_value)
                
                # Ambos son listas: append
                elif isinstance(old_value, list) and isinstance(new_value, list):
                    result[key] = old_value + new_value
                
                # Otros tipos: sobrescribe
                else:
                    result[key] = new_value
            else:
                # Key nuevo: simplemente añadir
                result[key] = new_value
        
        logger.debug(f"[ContextMergingEngine] Recursive merge: {len(new_context)} keys processed")
        return result
    
    def _merge_windowing(self, old_context: Dict[str, Any], new_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        WINDOWING: Mantiene últimos N elementos de listas.
        
        Limpia histórico para no saturar memoria
        """
        result = self._merge_recursive(old_context, new_context)
        
        # Aplicar windowing a listas
        for key, value in result.items():
            if isinstance(value, list) and len(value) > self.max_history:
                # Mantener últimos N elementos
                result[key] = value[-self.max_history:]
                logger.debug(f"[ContextMergingEngine] Windowed '{key}': {len(value)} → {len(result[key])}")
        
        return result
    
    # ==================== CONTEXT WINDOWING ====================
    
    def apply_windowing(self, context: Dict[str, Any], keys: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Aplica windowing a keys específicas o a todas las listas.
        
        Args:
            context: Context a procesar
            keys: Keys específicas, None = todas las listas
            
        Returns:
            Context con windowing aplicado
        """
        result = dict(context)
        
        if keys is None:
            # Aplicar a TODAS las listas
            keys = [k for k, v in context.items() if isinstance(v, list)]
        
        for key in keys:
            if key in result and isinstance(result[key], list):
                if len(result[key]) > self.max_history:
                    result[key] = result[key][-self.max_history:]
                    logger.debug(f"[ContextMergingEngine] Windowed '{key}' to last {self.max_history}")
        
        return result
    
    # ==================== CONTEXT ISOLATION ====================
    
    def create_isolated_context(self, user_id: str, base_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Crea context aislado por usuario.
        
        Args:
            user_id: ID del usuario
            base_context: Context base (opcional)
            
        Returns:
            Context aislado con metadatos de usuario
        """
        context = base_context or {}
        context["user_id"] = user_id
        context["session_start"] = datetime.now(timezone.utc).isoformat()
        context["message_history"] = []
        
        logger.debug(f"[ContextMergingEngine] Created isolated context for user {user_id}")
        return context
    
    # ==================== UTILITIES ====================
    
    def get_context_stats(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retorna estadísticas del context.
        
        Args:
            context: Context a analizar
            
        Returns:
            Stats dict
        """
        stats = {
            "total_keys": len(context),
            "lists": sum(1 for v in context.values() if isinstance(v, list)),
            "dicts": sum(1 for v in context.values() if isinstance(v, dict)),
            "total_list_items": sum(len(v) for v in context.values() if isinstance(v, list)),
        }
        
        return stats
    
    def prune_context(self, context: Dict[str, Any], keep_keys: List[str]) -> Dict[str, Any]:
        """
        Poda context manteniendo solo keys específicas.
        
        Args:
            context: Context original
            keep_keys: Keys a mantener
            
        Returns:
            Context podado
        """
        result = {k: context[k] for k in keep_keys if k in context}
        
        logger.debug(f"[ContextMergingEngine] Pruned context: {len(context)} → {len(result)} keys")
        return result
