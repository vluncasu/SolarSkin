# Architectural design archive

[Original twenty-module office building and kinetic facade](19_original_office.md).

The folder identifiers below match the original design records. Several mounting revisions retain the same exterior rendering. Use the CAD and print inventory of the selected revision to identify its hardware.

## Compact office, six modules

![Animated Compact office, six modules](../media/renders/compact_motion.gif)

[Open the animated Blender scene](../cad/earlier_offices/COMPACT_OFFICE.blend).

Source assembly family: `SOLARSKIN_COMPACT_OFFICE_6`.

## Aurora pavilion

![Animated Aurora pavilion](../media/renders/aurora_motion.gif)

[Open the animated Blender scene](../cad/earlier_offices/AURORA_PAVILION.blend).

Source assembly family: `SOLARSKIN_AURORA_9`.

## Rigid office, eight modules

![Animated Rigid office, eight modules](../media/renders/rigid_motion.gif)

[Open the animated Blender scene](../cad/earlier_offices/RIGID_OFFICE.blend).

Source assembly family: `SOLARSKIN_OFFICE_RIGID_8`.

## Office, nine modules

![Office, nine modules - source elevation](../media/renders/archive_office_9_architect.webp)

Source assembly family: `SOLARSKIN_OFFICE_9_ARCHITECT`.

## Integrated facade

![Integrated facade - source elevation](../media/renders/archive_16_integrat.webp)

Source assembly family: `SOLARSKIN_16_INTEGRAT`. [Open the saved views](21_revision_views.md#integrated-facade).

## Rapid office

![Rapid office - source elevation](../media/renders/archive_16_v5_rapid.webp)

Source assembly family: `SOLARSKIN_16_V5_RAPID`. [Open the saved views](21_revision_views.md#rapid-office).

## Unified facade

![Unified facade - source elevation](../media/renders/archive_16_fatada_unitara.webp)

Source assembly family: `SOLARSKIN_16_FATADA_UNITARA`. [Open the saved views](21_revision_views.md#unified-facade).

## Compact accents

![Compact accents - source elevation](../media/renders/archive_16_compact_accente.webp)

Source assembly family: `SOLARSKIN_16_COMPACT_ACCENTE`. [Open the saved views](21_revision_views.md#compact-accents).

## Sculptural envelope

![Sculptural envelope - source elevation](../media/renders/archive_16_sculptural.webp)

Source assembly family: `SOLARSKIN_16_SCULPTURAL`. [Open the saved views](21_revision_views.md#sculptural-envelope).

## Furnished office

![Furnished office - source elevation](../media/renders/archive_16_interior_complet.webp)

Source assembly family: `SOLARSKIN_16_INTERIOR_COMPLET`. [Open the saved views](21_revision_views.md#furnished-office).

## Interior supports

![Interior supports - source elevation](../media/renders/archive_16_reazeme_interior.webp)

Source assembly family: `SOLARSKIN_16_REAZEME_INTERIOR`. [Open the saved views](21_revision_views.md#interior-supports).

## Connector revision

![Connector revision - source elevation](../media/renders/archive_16_conectori.webp)

Source assembly family: `SOLARSKIN_16_CONECTORI`. [Open the saved views](21_revision_views.md#connector-revision).

## Revised mounts

![Revised mounts - source elevation](../media/renders/archive_16_reazeme_interior.webp)

Source assembly family: `SOLARSKIN_16_PRINDERI_REVIZUITE`. [Open the saved views](21_revision_views.md#revised-mounts).

## Marked parts

![Marked parts - source elevation](../media/renders/archive_16_reazeme_interior.webp)

Source assembly family: `SOLARSKIN_16_PIESE_MARCATE`. [Open the saved views](21_revision_views.md#marked-parts).

## Engraved parts

![Engraved parts - source elevation](../media/renders/archive_16_reazeme_interior.webp)

Source assembly family: `SOLARSKIN_16_GRAVATE`. [Open the saved views](21_revision_views.md#engraved-parts).

## Threaded mounting revision

![Threaded mounting revision - source elevation](../media/renders/archive_16_filet_prioritar.webp)

Source assembly family: `SOLARSKIN_16_FILET_PRIORITAR`. [Open the saved views](21_revision_views.md#threaded-mounting-revision).



## Motion in the downloadable scenes

The three preview assemblies preserve their building geometry and module
placement. The moving components use transforms sampled every six frames
from the original 10 mm mechanism. Each module has its own parent placement
in its building. Press Space in Blender to play the 241-frame sequence.

We reopened the delivered files and compared the world transforms of each
leaf at frames 1 and 121. All 36 leaves in Compact, 54 in Aurora and 48 in
Rigid change pose. The earlier twenty-module building retains its original
animation; all 120 of its leaves change pose between the same sampled frames.
[Read the verification record](../verification/original_offices_motion.json).
