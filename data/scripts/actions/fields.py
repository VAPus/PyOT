def _verify(creature, thing, position):
    if creature.position != position: return
    
    if not creature.hasCondition(getattr(game.const, 'CONDITION_%s' % (thing.field.upper()))):
        every = (thing.fieldTicks or 2000)/1000
        if thing.fieldStart:
            creature.condition(PercentCondition(getattr(game.const, 'CONDITION_%s' % (thing.field.upper())), startdmg=thing.fieldStart, percent=0.933)) # Magic constant. I dunno, seems ok for fields hehe.
        else:
            creature.condition(Condition(getattr(game.const, 'CONDITION_%s' % (thing.field.upper())), length=every * (thing.fieldCount or 1), every=every, damage=thing.fieldDamage))
    call_later((thing.fieldTicks or 2000)/1000, _verify, creature, thing, position)

def callback(creature, thing, position, **k):
    if thing.fieldDamage:
        every = (thing.fieldTicks or 2000)/1000
        if thing.fieldStart:
            creature.condition(PercentCondition(getattr(game.const, 'CONDITION_%s' % (thing.field.upper())), startdmg=thing.fieldStart, percent=0.933)) # Magick constant. Seems ok for poison fields.
        else:
            creature.condition(Condition(getattr(game.const, 'CONDITION_%s' % (thing.field.upper())), length=every * (thing.fieldCount or 1), every=every, damage=thing.fieldDamage))
        call_later(every, _verify, creature, thing, position)
    
registerForAttr('walkOn', 'fieldDamage', callback)
