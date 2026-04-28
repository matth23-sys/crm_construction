# -*- coding: utf-8 -*-
from django.db.models import Q, Prefetch
from .models.entities import Opportunity, OpportunityStage, OpportunityStageHistory
from .models.choices import OpportunityStatus

def get_opportunity_list(filters=None, user=None):
    """
    Retorna queryset de oportunidades con optimizaciones.
    Filtros opcionales: status, stage, responsible, client, search.
    """
    qs = Opportunity.objects.select_related(
        'client', 'responsible', 'stage'          # ← CAMBIADO: 'current_stage' → 'stage'
    ).prefetch_related(
        Prefetch('stage_history', queryset=OpportunityStageHistory.objects.order_by('-created_at'))
    ).all()

    if not filters:
        return qs

    if 'status' in filters and filters['status']:
        qs = qs.filter(status=filters['status'])

    if 'stage' in filters and filters['stage']:
        qs = qs.filter(stage_id=filters['stage'])   # ← CAMBIADO: current_stage_id → stage_id

    if 'responsible' in filters and filters['responsible']:
        qs = qs.filter(responsible_id=filters['responsible'])

    if 'client' in filters and filters['client']:
        qs = qs.filter(client_id=filters['client'])

    if 'search' in filters and filters['search']:
        search = filters['search']
        qs = qs.filter(
            Q(title__icontains=search) |
            Q(client__legal_name__icontains=search) |
            Q(client__commercial_name__icontains=search)
        )

    return qs

def get_kanban_board(user=None):
    """
    Retorna un diccionario con etapas y sus oportunidades.
    """
    stages = OpportunityStage.objects.filter(is_active=True).order_by('position')  # ← CAMBIADO: 'order' → 'position'
    opportunities = Opportunity.objects.filter(
        status__in=[OpportunityStatus.OPEN, OpportunityStatus.WON, OpportunityStatus.LOST]
    ).select_related('client', 'responsible', 'stage')   # ← CAMBIADO: 'current_stage' → 'stage'

    board = {}
    for stage in stages:
        board[stage.id] = {
            'stage': stage,
            'opportunities': [opp for opp in opportunities if opp.stage_id == stage.id]  # ← CAMBIADO: current_stage_id → stage_id
        }
    return board

def get_opportunity_detail(opportunity_id, user=None):
    """
    Retorna una oportunidad con todas las relaciones precargadas.
    """
    return Opportunity.objects.select_related(
        'client', 'responsible', 'stage'      # ← CAMBIADO: 'current_stage' → 'stage'
    ).prefetch_related(
        Prefetch('stage_history', queryset=OpportunityStageHistory.objects.order_by('-created_at'))
    ).get(pk=opportunity_id)