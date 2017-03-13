if config.regenerationTresshold > 0:
    def check(player, damage=0):
        return (player.data['health']-damage < config.regenerationTresshold \
           and not player.hasCondition(CONDITION_INFIGHT) and not (player.extraIcons & CONDITION_PROTECTIONZONE))

    def regenerator(player):
        if check(player):
            player.setHealth(config.regenerationTresshold)

    @register('hit', b'player')
    def regen(creature, creature2, damage, **k):
        if check(creature2, damage):
            call_later(config.regenerationDelay, regenerator, creature2)
