# -*- coding: utf-8 -*-
""" Test pressgloss library. """

# Standard library imports
import unittest

# pressgloss imports
import pressgloss.core as PRESSGLOSS
import pressgloss.helpers as helpers

parsetests = ['FRM (ENG) (FRA  ITA) (PRP (PCE (FRA ITA) ))',
              'FRM (ENG) (FRA ITA) (PRP (PCE (FRA ITA) ))',
              'FRM (ENG) (FRA  ITA) (PRP (PCE (FRA ITA)))',
              'FRM ( ENG) (FRA  ITA) (PRP (PCE (FRA ITA) ))',
              'FRM (ENG) (FRA ITA) (PRP (PCE (ENG FRA ITA)))',
              'FRM (ENG) (FRA ITA) (PRP (ALY (ENG FRA ITA) VSS (RUS TUR)))',
              'FRM (ENG) (FRA ITA) (PRP (ALY (ENG FRA ITA)VSS (RUS TUR)))',
              'FRM (ENG) (FRA ITA) (PRP (ALY (ENG FRA ITA) VSS(RUS TUR)))']

dmzexprs = [
            'FRM (FRA) (ENG) (PRP (NOT (DMZ (FRA ENG) (LVP YOR))))',
            'FRM (FRA) (ENG) (PRP (NOT (DMZ (FRA ENG ITA) (LVP YOR))))',
            'FRM (FRA) (ENG) (PRP (NOT (DMZ (FRA ENG ITA) (LVP YOR))))',
            'FRM (FRA) (ENG) (PRP (NOT (DMZ (FRA ENG) (LVP YOR))))',
            'FRM (FRA) (ENG) (PRP (NAR (DMZ (FRA ENG) (LVP YOR))))',
            'FRM (FRA) (ENG) (PRP (NAR (DMZ (FRA ENG ITA) (LVP YOR))))',
            'FRM (FRA) (ENG) (YES (PRP (DMZ (FRA ENG) (LVP YOR))))',
            'FRM (FRA) (ENG) (YES (PRP (DMZ (FRA ENG ITA) (LVP YOR))))',
            'FRM (FRA) (ENG) (YES (PRP (NOT (DMZ (FRA ENG) (LVP YOR)))))',
            'FRM (FRA) (ENG) (YES (PRP (NOT (DMZ (FRA ENG ITA) (LVP YOR)))))',
            'FRM (FRA) (ENG) (YES (PRP (NAR (DMZ (FRA ENG) (LVP YOR)))))',
            'FRM (FRA) (ENG) (YES (PRP (NAR (DMZ (FRA ENG ITA) (LVP YOR)))))',
            'FRM (FRA) (ENG) (REJ (PRP (DMZ (FRA ENG) (LVP YOR))))',
            'FRM (FRA) (ENG) (REJ (PRP (DMZ (FRA ENG ITA) (LVP YOR))))',
            'FRM (FRA) (ENG) (REJ (PRP (NOT (DMZ (FRA ENG) (LVP YOR)))))',
            'FRM (FRA) (ENG) (REJ (PRP (NOT (DMZ (FRA ENG ITA) (LVP YOR)))))',
            'FRM (FRA) (ENG) (REJ (PRP (NAR (DMZ (FRA ENG) (LVP YOR)))))',
            'FRM (FRA) (ENG) (REJ (PRP (NAR (DMZ (FRA ENG ITA) (LVP YOR)))))',
            'FRM (FRA) (ENG) (CCL (PRP (DMZ (FRA ENG) (LVP YOR))))',
            'FRM (FRA) (ENG) (CCL (PRP (DMZ (FRA ENG ITA) (LVP YOR))))',
            'FRM (FRA) (ENG) (CCL (PRP (NOT (DMZ (FRA ENG) (LVP YOR)))))',
            'FRM (FRA) (ENG) (CCL (PRP (NOT (DMZ (FRA ENG ITA) (LVP YOR)))))',
            'FRM (FRA) (ENG) (CCL (PRP (NAR (DMZ (FRA ENG) (LVP YOR)))))',
            'FRM (FRA) (ENG) (CCL (PRP (NAR (DMZ (FRA ENG ITA) (LVP YOR)))))',
            'FRM (FRA) (ENG) (CCL (YES (PRP (DMZ (FRA ENG) (LVP YOR)))))',
            'FRM (FRA) (ENG) (CCL (YES (PRP (DMZ (FRA ENG ITA) (LVP YOR)))))',
            'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (DMZ (FRA ENG) (LVP YOR))))))',
            'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (DMZ (FRA ENG ITA) (LVP YOR))))))',
            'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (DMZ (FRA ENG) (LVP YOR))))))',
            'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (DMZ (FRA ENG ITA) (LVP YOR))))))',
            'FRM (FRA) (ENG) (HUH (PRP (NAR (DMZ (FRA ENG) (LVP YOR)))))',
            'FRM (FRA) (ENG) (BWX (PRP (NAR (DMZ (FRA ENG) (LVP YOR)))))'
           ]

peaceexprs = [
              'FRM (ENG) (FRA ITA) (PRP (PCE (FRA ITA)))',
              'FRM (ENG) (FRA ITA) (PRP (PCE (ENG FRA ITA)))',
              'FRM (ENG) (FRA ITA) (PRP (NOT (PCE (FRA ITA))))',
              'FRM (ENG) (FRA ITA) (PRP (NOT (PCE (ENG FRA ITA))))',
              'FRM (ENG) (FRA ITA) (PRP (NAR (PCE (FRA ITA))))',
              'FRM (ENG) (FRA ITA) (PRP (NAR (PCE (ENG FRA ITA))))',
              'FRM (FRA) (ENG ITA) (YES (PRP (PCE (FRA ITA))))',
              'FRM (FRA) (ENG ITA) (YES (PRP (PCE (ENG FRA ITA))))',
              'FRM (FRA) (ENG ITA) (YES (PRP (NOT (PCE (FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (YES (PRP (NOT (PCE (ENG FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (YES (PRP (NAR (PCE (FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (YES (PRP (NAR (PCE (ENG FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (REJ (PRP (PCE (FRA ITA))))',
              'FRM (FRA) (ENG ITA) (REJ (PRP (PCE (ENG FRA ITA))))',
              'FRM (FRA) (ENG ITA) (REJ (PRP (NOT (PCE (FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (REJ (PRP (NOT (PCE (ENG FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (REJ (PRP (NAR (PCE (FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (REJ (PRP (NAR (PCE (ENG FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (BWX (PRP (PCE (FRA ITA))))',
              'FRM (FRA) (ENG ITA) (BWX (PRP (PCE (ENG FRA ITA))))',
              'FRM (FRA) (ENG ITA) (BWX (PRP (NOT (PCE (FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (BWX (PRP (NOT (PCE (ENG FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (BWX (PRP (NAR (PCE (FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (BWX (PRP (NAR (PCE (ENG FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (HUH (PRP (PCE (FRA ITA))))',
              'FRM (FRA) (ENG ITA) (HUH (PRP (PCE (ENG FRA ITA))))',
              'FRM (FRA) (ENG ITA) (HUH (PRP (NOT (PCE (FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (HUH (PRP (NOT (PCE (ENG FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (HUH (PRP (NAR (PCE (FRA ITA)))))',
              'FRM (FRA) (ENG ITA) (HUH (PRP (NAR (PCE (ENG FRA ITA)))))',
              'FRM (ENG) (FRA ITA) (CCL (PRP (PCE (FRA ITA))))',
              'FRM (ENG) (FRA ITA) (CCL (PRP (PCE (ENG FRA ITA))))',
              'FRM (ENG) (FRA ITA) (CCL (PRP (NOT (PCE (FRA ITA)))))',
              'FRM (ENG) (FRA ITA) (CCL (PRP (NOT (PCE (ENG FRA ITA)))))',
              'FRM (ENG) (FRA ITA) (CCL (PRP (NAR (PCE (FRA ITA)))))',
              'FRM (ENG) (FRA ITA) (CCL (PRP (NAR (PCE (ENG FRA ITA)))))',
              'FRM (ENG) (FRA ITA) (CCL (YES (PRP (PCE (FRA ITA)))))',
              'FRM (ENG) (FRA ITA) (CCL (YES (PRP (PCE (ENG FRA ITA)))))',
              'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NOT (PCE (FRA ITA))))))',
              'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NOT (PCE (ENG FRA ITA))))))',
              'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NAR (PCE (FRA ITA))))))',
              'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NAR (PCE (ENG FRA ITA))))))',
              'FRM (ENG) (FRA) (FCT (PCE (ENG ITA)))',
              'FRM (ENG) (FRA) (FCT (PCE (TUR ITA)))',
              'FRM (ENG) (FRA) (FCT (NOT (PCE (ENG ITA))))',
              'FRM (ENG) (FRA) (FCT (NOT (PCE (FRA ITA))))',
              'FRM (ENG) (FRA) (FCT (NOT (PCE (RUS ITA))))',
              'FRM (ENG) (FRA) (FCT (NAR (PCE (ENG ITA))))'
             ]

allianceexprs = [
                'FRM (ENG) (FRA ITA) (PRP (ALY (ENG FRA ITA) VSS (RUS TUR)))',
                'FRM (ENG) (FRA ITA) (PRP (ALY (FRA ITA) VSS (RUS TUR)))',
                'FRM (ENG) (FRA) (PRP (ALY (FRA ITA) VSS (RUS TUR)))',
                'FRM (ENG) (FRA ITA) (PRP (NOT (ALY (ENG FRA ITA) VSS (RUS TUR))))',
                'FRM (ENG) (FRA ITA) (PRP (NOT (ALY (FRA ITA) VSS (ENG))))',
                'FRM (ENG) (FRA ITA) (PRP (NOT (ALY (FRA ITA) VSS (RUS TUR))))',
                'FRM (ENG) (FRA ITA) (PRP (NAR (ALY (ENG FRA ITA) VSS (RUS TUR))))',
                'FRM (ENG) (FRA ITA) (PRP (NAR (ALY (FRA ITA) VSS (ENG))))',
                'FRM (ENG) (FRA ITA) (PRP (NAR (ALY (FRA ITA) VSS (RUS TUR))))',
                'FRM (FRA) (ENG ITA) (YES (PRP (ALY (ENG FRA ITA) VSS (RUS TUR))))',
                'FRM (FRA) (ENG ITA) (YES (PRP (ALY (FRA ITA) VSS (RUS TUR))))',
                'FRM (FRA) (ENG ITA) (YES (PRP (NOT (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (YES (PRP (NOT (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (YES (PRP (NAR (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (YES (PRP (NAR (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (REJ (PRP (ALY (ENG FRA ITA) VSS (RUS TUR))))',
                'FRM (FRA) (ENG ITA) (REJ (PRP (ALY (FRA ITA) VSS (RUS TUR))))',
                'FRM (FRA) (ENG ITA) (REJ (PRP (NOT (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (REJ (PRP (NOT (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (REJ (PRP (NAR (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (REJ (PRP (NAR (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (BWX (PRP (ALY (ENG FRA ITA) VSS (RUS TUR))))',
                'FRM (FRA) (ENG ITA) (BWX (PRP (NOT (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (BWX (PRP (ALY (FRA ITA) VSS (RUS TUR))))',
                'FRM (FRA) (ENG ITA) (BWX (PRP (NOT (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (BWX (PRP (NAR (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (BWX (PRP (NAR (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (HUH (PRP (ALY (ENG FRA ITA) VSS (RUS TUR))))',
                'FRM (FRA) (ENG ITA) (HUH (PRP (ALY (FRA ITA) VSS (RUS TUR))))',
                'FRM (FRA) (ENG ITA) (HUH (PRP (NOT (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (HUH (PRP (NOT (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (HUH (PRP (NAR (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (FRA) (ENG ITA) (HUH (PRP (NAR (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (ENG) (FRA ITA) (CCL (PRP (ALY (ENG FRA ITA) VSS (RUS TUR))))',
                'FRM (ENG) (FRA ITA) (CCL (PRP (ALY (FRA ITA) VSS (RUS TUR))))',
                'FRM (ENG) (FRA ITA) (CCL (PRP (NOT (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (ENG) (FRA ITA) (CCL (PRP (NOT (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (ENG) (FRA ITA) (CCL (PRP (NAR (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (ENG) (FRA ITA) (CCL (PRP (NAR (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (ENG) (FRA ITA) (CCL (YES (PRP (ALY (ENG FRA ITA) VSS (RUS TUR)))))',
                'FRM (ENG) (FRA ITA) (CCL (YES (PRP (ALY (FRA ITA) VSS (RUS TUR)))))',
                'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NOT (ALY (ENG FRA ITA) VSS (RUS TUR))))))',
                'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NOT (ALY (FRA ITA) VSS (RUS TUR))))))',
                'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NAR (ALY (ENG FRA ITA) VSS (RUS TUR))))))',
                'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NAR (ALY (FRA ITA) VSS (RUS TUR))))))',
                'FRM (ENG) (FRA) (FCT (ALY (ENG ITA) VSS (RUS TUR)))',
                'FRM (ENG) (FRA) (FCT (ALY (TUR ITA) VSS (RUS)))',
                'FRM (ENG) (FRA) (FCT (ALY (TUR ITA) VSS (ENG)))',
                'FRM (ENG) (FRA) (FCT (NOT (ALY (ENG ITA) VSS (RUS TUR))))',
                'FRM (ENG) (FRA) (FCT (NOT (ALY (RUS ITA) VSS (ENG))))',
                'FRM (ENG) (FRA) (FCT (NOT (ALY (RUS ITA) VSS (FRA))))',
                'FRM (ENG) (FRA) (FCT (NAR (ALY (ENG ITA) VSS (RUS TUR))))'
                ]

drawexprs = [
            'FRM (ENG) (FRA ITA) (PRP (DRW))',
            'FRM (ENG) (FRA ITA) (PRP (DRW (ENG FRA ITA)))',
            'FRM (ENG) (FRA ITA) (PRP (NOT (DRW)))',
            'FRM (ENG) (FRA ITA) (PRP (NOT (DRW (ENG FRA ITA))))',
            'FRM (ENG) (FRA ITA) (PRP (NAR (DRW)))',
            'FRM (ENG) (FRA ITA) (PRP (NAR (DRW (ENG FRA ITA))))',
            'FRM (FRA) (ENG ITA) (YES (PRP (DRW)))',
            'FRM (FRA) (ENG ITA) (YES (PRP (DRW (ENG FRA ITA))))',
            'FRM (FRA) (ENG ITA) (YES (PRP (NOT (DRW))))',
            'FRM (FRA) (ENG ITA) (YES (PRP (NOT (DRW (ENG FRA ITA)))))',
            'FRM (FRA) (ENG ITA) (YES (PRP (NAR (DRW))))',
            'FRM (FRA) (ENG ITA) (YES (PRP (NAR (DRW (ENG FRA ITA)))))',
            'FRM (FRA) (ENG ITA) (REJ (PRP (DRW)))',
            'FRM (FRA) (ENG ITA) (REJ (PRP (DRW (ENG FRA ITA))))',
            'FRM (FRA) (ENG ITA) (REJ (PRP (NOT (DRW))))',
            'FRM (FRA) (ENG ITA) (REJ (PRP (NOT (DRW (ENG FRA ITA)))))',
            'FRM (FRA) (ENG ITA) (REJ (PRP (NAR (DRW))))',
            'FRM (FRA) (ENG ITA) (REJ (PRP (NAR (DRW (ENG FRA ITA)))))',
            'FRM (FRA) (ENG ITA) (BWX (PRP (DRW)))',
            'FRM (FRA) (ENG ITA) (BWX (PRP (DRW (ENG FRA ITA))))',
            'FRM (FRA) (ENG ITA) (BWX (PRP (NOT (DRW))))',
            'FRM (FRA) (ENG ITA) (BWX (PRP (NOT (DRW (ENG FRA ITA)))))',
            'FRM (FRA) (ENG ITA) (BWX (PRP (NAR (DRW))))',
            'FRM (FRA) (ENG ITA) (BWX (PRP (NAR (DRW (ENG FRA ITA)))))',
            'FRM (FRA) (ENG ITA) (HUH (PRP (DRW)))',
            'FRM (FRA) (ENG ITA) (HUH (PRP (DRW (ENG FRA ITA))))',
            'FRM (FRA) (ENG ITA) (HUH (PRP (NOT (DRW))))',
            'FRM (FRA) (ENG ITA) (HUH (PRP (NOT (DRW (ENG FRA ITA)))))',
            'FRM (FRA) (ENG ITA) (HUH (PRP (NAR (DRW))))',
            'FRM (FRA) (ENG ITA) (HUH (PRP (NAR (DRW (ENG FRA ITA)))))',
            'FRM (ENG) (FRA ITA) (CCL (PRP (DRW)))',
            'FRM (ENG) (FRA ITA) (CCL (PRP (DRW (ENG FRA ITA))))',
            'FRM (ENG) (FRA ITA) (CCL (PRP (NOT (DRW))))',
            'FRM (ENG) (FRA ITA) (CCL (PRP (NOT (DRW (ENG FRA ITA)))))',
            'FRM (ENG) (FRA ITA) (CCL (PRP (NAR (DRW))))',
            'FRM (ENG) (FRA ITA) (CCL (PRP (NAR (DRW (ENG FRA ITA)))))',
            'FRM (ENG) (FRA ITA) (CCL (YES (PRP (DRW))))',
            'FRM (ENG) (FRA ITA) (CCL (YES (PRP (DRW (ENG FRA ITA)))))',
            'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NOT (DRW)))))',
            'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NOT (DRW (ENG FRA ITA))))))',
            'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NAR (DRW)))))',
            'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NAR (DRW (ENG FRA ITA))))))',
            'FRM (ENG) (FRA) (FCT (DRW))',
            'FRM (ENG) (FRA) (FCT (DRW (ENG FRA ITA)))',
            'FRM (ENG) (FRA) (FCT (NOT (DRW)))',
            'FRM (ENG) (FRA) (FCT (NOT (DRW (ENG FRA ITA))))',
            'FRM (ENG) (FRA) (FCT (NAR (DRW)))',
            ]

soloexprs = [
            'FRM (ENG) (FRA) (PRP (SLO (FRA)))',
            'FRM (ENG) (FRA) (PRP (NOT (SLO (FRA))))',
            'FRM (ENG) (FRA) (PRP (NAR (SLO (FRA))))',
            'FRM (FRA) (ENG) (YES (PRP (SLO (FRA))))',
            'FRM (FRA) (ENG) (YES (PRP (NOT (SLO (FRA)))))',
            'FRM (FRA) (ENG ITA) (YES (PRP (NAR (SLO (FRA)))))',
            'FRM (FRA) (ENG) (REJ (PRP (SLO (FRA))))',
            'FRM (FRA) (ENG) (REJ (PRP (NOT (SLO (FRA)))))',
            'FRM (FRA) (ENG ITA) (REJ (PRP (NAR (SLO (FRA)))))',
            'FRM (FRA) (ENG) (BWX (PRP (SLO (FRA))))',
            'FRM (FRA) (ENG) (BWX (PRP (NOT (SLO (FRA)))))',
            'FRM (FRA) (ENG ITA) (BWX (PRP (NAR (SLO (FRA)))))',
            'FRM (FRA) (ENG) (HUH (PRP (SLO (FRA))))',
            'FRM (FRA) (ENG) (HUH (PRP (NOT (SLO (FRA)))))',
            'FRM (FRA) (ENG ITA) (HUH (PRP (NAR (SLO (FRA)))))',
            'FRM (ENG) (FRA) (CCL (PRP (SLO (FRA))))',
            'FRM (ENG) (FRA) (CCL (PRP (NOT (SLO (FRA)))))',
            'FRM (ENG) (FRA ITA) (CCL (PRP (NAR (SLO (FRA)))))',
            'FRM (ENG) (FRA) (CCL (YES (PRP (SLO (FRA)))))',
            'FRM (ENG) (FRA) (CCL (YES (PRP (NOT (SLO (FRA))))))',
            'FRM (ENG) (FRA ITA) (CCL (YES (PRP (NAR (SLO (FRA))))))',
            'FRM (ENG) (FRA) (FCT (SLO (ENG)))',
            'FRM (ENG) (FRA) (FCT (SLO (TUR)))',
            'FRM (ENG) (FRA) (FCT (NOT (SLO (ENG))))',
            'FRM (ENG) (FRA) (FCT (NAR (SLO (ENG))))'
            ]

moveexprs = [
              'FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) HLD)))',
              'FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) MTO YOR)))',
              'FRM (FRA) (ENG) (PRP (DMZ (FRA ENG) (LVP YOR)))',
              'FRM (FRA) (ENG) (PRP (DMZ (FRA ENG ITA) (LVP YOR)))',
              'FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON)))',
              'FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) SUP (FRA AMY YOR))))',
              'FRM (FRA) (ENG) (PRP (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON)))',
              'FRM (FRA) (ENG) (PRP (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH))))',
              'FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) RTO YOR)))',
              'FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) DSB)))',
              'FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) BLD)))',
              'FRM (FRA) (ENG) (PRP (XDO ((ENG FLT LVP) BLD)))',
              'FRM (FRA) (ENG) (PRP (XDO ((ENG AMY LVP) REM)))',
              'FRM (FRA) (ENG) (PRP (XDO (ENG WVE)))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG AMY LVP) HLD))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG AMY LVP) MTO YOR))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG AMY LVP) SUP (FRA AMY YOR)))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH)))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG AMY LVP) RTO YOR))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG AMY LVP) DSB))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG AMY LVP) BLD))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG FLT LVP) BLD))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO ((ENG AMY LVP) REM))))',
              'FRM (FRA) (ENG) (PRP (NOT (XDO (ENG WVE))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG AMY LVP) HLD))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG AMY LVP) MTO YOR))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG AMY LVP) SUP (FRA AMY YOR)))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH)))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG AMY LVP) RTO YOR))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG AMY LVP) DSB))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG AMY LVP) BLD))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG FLT LVP) BLD))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO ((ENG AMY LVP) REM))))',
              'FRM (FRA) (ENG) (PRP (NAR (XDO (ENG WVE))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG AMY LVP) HLD))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG AMY LVP) MTO YOR))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG AMY LVP) SUP (FRA AMY YOR)))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH)))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG AMY LVP) RTO YOR))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG AMY LVP) DSB))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG AMY LVP) BLD))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG FLT LVP) BLD))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO ((ENG AMY LVP) REM))))',
              'FRM (FRA) (ENG) (YES (PRP (XDO (ENG WVE))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG AMY LVP) HLD)))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG AMY LVP) MTO YOR)))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON)))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG AMY LVP) SUP (FRA AMY YOR))))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON)))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH))))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG AMY LVP) RTO YOR)))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG AMY LVP) DSB)))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG AMY LVP) BLD)))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG FLT LVP) BLD)))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO ((ENG AMY LVP) REM)))))',
              'FRM (FRA) (ENG) (YES (PRP (NOT (XDO (ENG WVE)))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG AMY LVP) HLD)))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG AMY LVP) MTO YOR)))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON)))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG AMY LVP) SUP (FRA AMY YOR))))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON)))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH))))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG AMY LVP) RTO YOR)))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG AMY LVP) DSB)))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG AMY LVP) BLD)))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG FLT LVP) BLD)))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO ((ENG AMY LVP) REM)))))',
              'FRM (FRA) (ENG) (YES (PRP (NAR (XDO (ENG WVE)))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG AMY LVP) HLD))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG AMY LVP) MTO YOR))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG AMY LVP) SUP (FRA AMY YOR)))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH)))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG AMY LVP) RTO YOR))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG AMY LVP) DSB))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG AMY LVP) BLD))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG FLT LVP) BLD))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO ((ENG AMY LVP) REM))))',
              'FRM (FRA) (ENG) (REJ (PRP (XDO (ENG WVE))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG AMY LVP) HLD)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG AMY LVP) MTO YOR)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG AMY LVP) SUP (FRA AMY YOR))))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH))))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG AMY LVP) RTO YOR)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG AMY LVP) DSB)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG AMY LVP) BLD)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG FLT LVP) BLD)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO ((ENG AMY LVP) REM)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NOT (XDO (ENG WVE)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG AMY LVP) HLD)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG AMY LVP) MTO YOR)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG AMY LVP) SUP (FRA AMY YOR))))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH))))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG AMY LVP) RTO YOR)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG AMY LVP) DSB)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG AMY LVP) BLD)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG FLT LVP) BLD)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO ((ENG AMY LVP) REM)))))',
              'FRM (FRA) (ENG) (REJ (PRP (NAR (XDO (ENG WVE)))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG AMY LVP) HLD))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG AMY LVP) MTO YOR))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG AMY LVP) SUP (FRA AMY YOR)))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH)))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG AMY LVP) RTO YOR))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG AMY LVP) DSB))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG AMY LVP) BLD))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG FLT LVP) BLD))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO ((ENG AMY LVP) REM))))',
              'FRM (FRA) (ENG) (CCL (PRP (XDO (ENG WVE))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG AMY LVP) HLD)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG AMY LVP) MTO YOR)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG AMY LVP) SUP (FRA AMY YOR))))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH))))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG AMY LVP) RTO YOR)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG AMY LVP) DSB)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG AMY LVP) BLD)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG FLT LVP) BLD)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO ((ENG AMY LVP) REM)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NOT (XDO (ENG WVE)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG AMY LVP) HLD)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG AMY LVP) MTO YOR)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG AMY LVP) SUP (FRA AMY YOR))))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH))))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG AMY LVP) RTO YOR)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG AMY LVP) DSB)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG AMY LVP) BLD)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG FLT LVP) BLD)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO ((ENG AMY LVP) REM)))))',
              'FRM (FRA) (ENG) (CCL (PRP (NAR (XDO (ENG WVE)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG AMY LVP) HLD)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG AMY LVP) MTO YOR)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG AMY LVP) SUP (FRA AMY YOR))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG AMY LVP) RTO YOR)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG AMY LVP) DSB)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG AMY LVP) BLD)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG FLT LVP) BLD)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO ((ENG AMY LVP) REM)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (XDO (ENG WVE)))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG AMY LVP) HLD))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG AMY LVP) MTO YOR))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG AMY LVP) SUP (FRA AMY YOR)))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH)))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG AMY LVP) RTO YOR))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG AMY LVP) DSB))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG AMY LVP) BLD))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG FLT LVP) BLD))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO ((ENG AMY LVP) REM))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NOT (XDO (ENG WVE))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG AMY LVP) HLD))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG AMY LVP) MTO YOR))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG AMY LVP) SUP (FRA AMY YOR) MTO LON))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG AMY LVP) SUP (FRA AMY YOR)))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG AMY YOR) CTO LON VIA (NAO IRI NTH)))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG AMY LVP) RTO YOR))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG AMY LVP) DSB))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG AMY LVP) BLD))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG FLT LVP) BLD))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO ((ENG AMY LVP) REM))))))',
              'FRM (FRA) (ENG) (CCL (YES (PRP (NAR (XDO (ENG WVE))))))',
              'FRM (FRA) (ENG) (HUH (PRP (NAR (XDO ((ENG AMY LVP) MTO YOR)))))',
              'FRM (FRA) (ENG) (BWX (PRP (NAR (XDO ((ENG AMY LVP) MTO YOR)))))'
               ]

compositions = [
               'FRM (FRA) (ENG) (PRP (IFF (XDO ((ENG AMY LVP) MTO YOR)) (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON))))',
               'FRM (FRA) (ENG) (PRP (AND (XDO ((ENG AMY LVP) MTO YOR)) (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON))))',
               'FRM (FRA) (ENG) (PRP (ORR (XDO ((ENG AMY LVP) MTO YOR)) (XDO ((ENG FLT NTH) CVY (FRA AMY BRE) CTO LON))))',
               ]

badexprs = [
            'BORK BORK BORK',
            ''
           ]

class PowerListTest(unittest.TestCase):
  """ Tests building lists of countries from trigrams. """
  def test(self):
    self.assertEqual(helpers.listOfPowers(['ENG'], 'ENG', ['FRA', 'ITA']), 'me')
    self.assertEqual(helpers.listOfPowers(['ENG'], 'ENG', ['FRA', 'ITA'], 'Subjective'), 'I')
    self.assertEqual(helpers.listOfPowers(['FRA'], 'ENG', ['FRA']), 'you')
    self.assertEqual(helpers.listOfPowers(['FRA', 'ENG'], 'ENG', ['FRA']), 'you and me')
    self.assertEqual(helpers.listOfPowers(['FRA', 'ENG'], 'ENG', ['FRA'], case='Subjective'), 'you and I')
    self.assertEqual(helpers.listOfPowers(['FRA', 'ENG', 'ITA'], 'ENG', ['FRA']), 'you, Italy and me')
    self.assertEqual(helpers.listOfPowers(['FRA', 'ENG', 'ITA'], 'ENG', ['FRA'], case='Subjective'), 'you, Italy and I')
    self.assertEqual(helpers.listOfPowers(['FRA', 'ITA'], 'ENG', ['FRA', 'ITA']), 'you two')
    self.assertEqual(helpers.listOfPowers(['FRA', 'ITA'], 'ENG', ['FRA']), 'you and Italy')
    self.assertEqual(helpers.listOfPowers(['FRA', 'ITA', 'RUS'], 'ENG', ['FRA']), 'you, Italy and Russia')
    self.assertEqual(helpers.listOfPowers(['FRA', 'ITA', 'RUS'], 'ENG', ['FRA', 'ITA']), 'you two and Russia')
    self.assertEqual(helpers.listOfPowers(['FRA', 'ITA', 'RUS'], 'ENG', ['TUR']), 'France, Italy and Russia')

class ParseTest(unittest.TestCase):
  """ Tests parsing of various quasi-compliant DAIDE strings. """
  def test(self):
    for curdaide in parsetests:
      self.assertEqual(len(helpers.daide2lists(curdaide)), 4)

class DMZTest(unittest.TestCase):
  """ Tests different DMZ press expressions in Objective tone. """
  def test(self):
    for curdaide in dmzexprs:
      print('Testing ' + curdaide)
      self.assertTrue('Ahem' not in PRESSGLOSS.daide2gloss(curdaide, ['Objective']))

class PeaceTest(unittest.TestCase):
  """ Tests different peace agreement press expressions in Objective tone. """
  def test(self):
    for curdaide in peaceexprs:
      print('Testing ' + curdaide)
      self.assertTrue('Ahem' not in PRESSGLOSS.daide2gloss(curdaide, ['Objective']))

class AllianceTest(unittest.TestCase):
  """ Tests different alliance press expressions in Objective tone. """
  def test(self):
    for curdaide in allianceexprs:
      print('Testing ' + curdaide)
      self.assertTrue('Ahem' not in PRESSGLOSS.daide2gloss(curdaide, ['Objective']))

class DrawTest(unittest.TestCase):
  """ Tests different draw press expressions in Objective tone. """
  def test(self):
    for curdaide in drawexprs:
      print('Testing ' + curdaide)
      self.assertTrue('Ahem' not in PRESSGLOSS.daide2gloss(curdaide, ['Objective']))

class SoloTest(unittest.TestCase):
  """ Tests different solo win press expressions in Objective tone. """
  def test(self):
    for curdaide in soloexprs:
      print('Testing ' + curdaide)
      self.assertTrue('Ahem' not in PRESSGLOSS.daide2gloss(curdaide, ['Objective']))

class BadTest(unittest.TestCase):
  """ Tests different badly constructed press expressions in Objective tone. """
  def test(self):
    for curdaide in badexprs:
      print('Testing ' + curdaide)
      self.assertTrue('Ahem' in PRESSGLOSS.daide2gloss(curdaide, ['Objective']))

class MoveTest(unittest.TestCase):
  """ Tests different level 20 moves in Objective tone. """
  def test(self):
    for curdaide in moveexprs:
      print('Testing ' + curdaide)
      self.assertTrue('Ahem' not in PRESSGLOSS.daide2gloss(curdaide, ['Objective']))

class ComposeTest(unittest.TestCase):
  """ Tests different level 30 and 100 expressions in Objective tone. """
  def test(self):
    for curdaide in compositions:
      print('Testing ' + curdaide)
      self.assertTrue('Ahem' not in PRESSGLOSS.daide2gloss(curdaide, ['Objective']))

if __name__ == '__main__':
  unittest.main()