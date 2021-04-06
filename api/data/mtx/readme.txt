when updating the MTX catalogue:
- remove entirely exsisting one (.xlsx and .db)
- copy the new one and leave only the following sheets and columns:
    - term:
        termCode, termExtendedName, termScopeNote, deprecated, allFacets, detailLevel, termType
    - attribute:
        code, name, label, scopeNote, attributeReportable, attributeSingleOrRepeatable, deprecated