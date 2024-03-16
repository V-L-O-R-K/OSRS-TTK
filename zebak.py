from monsters import *
from weapons import *
from thralls import *

# Zebak restores magic level and def level at a rate of ~1 / 60 seconds = 100 ticks

num_to_kill = 10000
thrall_active = True

# will prob only be editing these 4 variables + raid/path level to run sims
raid_level = 415
path_level = 3

use_spec = False # zcb
lightbearer = False
seercull = False
adrenaline = False

spec_accuracy = 74.81  # percent

normal_spec_cost = 750  # https://oldschool.runescape.wiki/w/Liquid_adrenaline#2_dose
seercull_spec_cost = 1000

if not lightbearer:  # assumes magus
    shadow_max_hit_roll = 114896
    shadow_max = 84
else:
    shadow_max_hit_roll = 104876
    shadow_max = 80

shadow = StandardWeapon(5, shadow_max, shadow_max_hit_roll)
zcb = StandardWeapon(5, 50, 40922)

thrall = Thrall()

if adrenaline:
    spec_cost = normal_spec_cost/2
    seercull_spec_cost = seercull_spec_cost/2
else:
    spec_cost = normal_spec_cost

ttk_ticks = []
num_specs = []
seercull_hits = []

for i in range(num_to_kill):
    if seercull:  # TODO Fix this so it rolls a number instead of using the average
        seercull_hit = randint(0, 26)
        zebak = TombsMonster(raid_level, path_level, 70, 100-seercull_hit, 160, 200, 110, 580)  # 13 is average seercull hit
        spec_energy = 1000 - seercull_spec_cost
    else:
        zebak = TombsMonster(raid_level, path_level, 70, 100, 160, 200, 110, 580)
        spec_energy = 1000  # It's actually out of 1000 not 100 so no rounding occurs for adrenaline usage

    tick = 1
    started_spec_regen = 1
    last_regen_tick = 0

    player_attack_cd = 1  # so you attack on first tick
    thrall_attack_cd = 1  # so it attacks on first tick
    specs_this_kill = 0


    print(f'STARTING KILL NUMBER {i+1} of {num_to_kill}')
    while zebak.current_hp > 0:
        if tick - last_regen_tick == 100 and zebak.magic_level < 100:  # zeb regens stats every ~60 sec (100 ticks)
            zebak.magic_level += 1
            last_regen_tick = tick
            print(f'Zebak regened 1 magic level on tick {last_regen_tick}\n'
                  f'seercul hit a {seercull_hit} and zeb mage lvl is now {zebak.magic_level}')

        # regen spec if less than 1000 and appropriate number of ticks passed
        if spec_energy < 1000 and lightbearer is False:
            if tick - started_spec_regen == 50:
                spec_energy += 10
                started_spec_regen = tick
                print(f'Tick {tick}: Regained 10 Spec without lightbearer | {spec_energy} spec remaining')
        elif spec_energy < 1000 and lightbearer is True:
            if tick - started_spec_regen == 25:
                spec_energy += 10
                started_spec_regen = tick
                print(f'Tick {tick}: Regained 10 Spec with lightbearer | {spec_energy} spec remaining')

        # check if it's a tick we can attack
        if player_attack_cd == 1:

            # spec with ZCB if we have energy ... only spec if average hit will be > shadow average hit
            if use_spec and spec_energy >= spec_cost and (0.22 * zebak.current_hp * spec_accuracy) > (shadow_max/2*shadow.hit_chance(zebak.max_roll_vs_magic)):
                if spec_energy == 1000:
                    started_spec_regen = tick

                specs_this_kill += 1
                spec_energy -= spec_cost

                if uniform(0, 1000) <= spec_accuracy * 10:
                    attempted_hit = int(zebak.current_hp * 0.22)
                    if attempted_hit > 110:
                        damage = 110
                    elif 1 < attempted_hit < 110:
                        damage = attempted_hit
                    elif attempted_hit < 1:
                        damage = 1

                    zebak.current_hp -= damage
                    print(f"Tick {tick}: Specc'd Zebak for {damage} | {zebak.current_hp} hp remaining | {spec_energy} spec remaining")
                else:
                    print(
                        f"Tick {tick}: Specc'd Zebak for MISSED | {zebak.current_hp} hp remaining | {spec_energy} spec remaining")

                player_attack_cd = zcb.attack_speed

            # otherwise attack with Shadow
            elif uniform(0, 1000) <= shadow.hit_chance(zebak.max_roll_vs_magic) * 1000:  # roll for shadow to hit
                damage = shadow.roll_damage()
                zebak.current_hp -= damage

                print(f'Tick {tick} Hit Zebak for {damage} | {zebak.current_hp} hp remaining')
                player_attack_cd = shadow.attack_speed
            else:
                print(f'Tick {tick} Hit Zebak for MISSED | {zebak.current_hp} hp remaining')
                player_attack_cd = shadow.attack_speed

        # if we can't attack this tick we wait
        else:
            player_attack_cd -= 1

        # check if it's a tick a thrall can attack
        if thrall_active and thrall_attack_cd == 1:
            thrall_damage = thrall.roll_damage()
            zebak.current_hp -= thrall_damage
            print(f'Tick {tick}: Thrall hit Zebak for {thrall_damage} | {zebak.current_hp} hp remaining')
            thrall_attack_cd = thrall.attack_speed
        else:
            thrall_attack_cd -= 1

        tick += 1

    # individual kill message
    print(f'KILL {i+1}: TTK {tick} ticks ({round(tick * .6, 2)} seconds)\n\n')

    # reset for next simulated kill
    zebak.current_hp = zebak.max_hp

    # append specs and ttk to list for averaging later
    num_specs.append(specs_this_kill)
    ttk_ticks.append(tick)
    if seercull:
        seercull_hits.append(seercull_hit)


print('\n****************************************************')
print(f'\nDEBUG\nZebak total hp = {zebak.max_hp}')
print(f'Shadow accuracy = {shadow.hit_chance(zebak.max_roll_vs_magic)}')
print(f'Shadow dps = {shadow.dps(zebak.max_roll_vs_magic)} (w/ thrall = {shadow.dps(zebak.max_roll_vs_magic) + 0.625}')
print(f'ZCB normal accuracy = {zcb.hit_chance(zebak.max_roll_vs_range)}')

print('\n************************************************************\n'
      f'Raid Level: {raid_level} | Path Level: {path_level} | Sample Size: {num_to_kill}\n'
      f'Using specs: {use_spec} | Lightbearer: {lightbearer} | Adrenaline: {adrenaline} | Thralls: {thrall_active} | Seercull: {seercull}')
print(f'Shadow max: {shadow_max} | Shadow attack roll: {shadow_max_hit_roll} | ZCB spec accuracy: {spec_accuracy}%')

print(f'\nAverage time to kill (TTK) = {round(sum(ttk_ticks)/len(ttk_ticks), 2)} ticks = {round(sum(ttk_ticks)/len(ttk_ticks)*0.6, 2)} sec')
print(f'Average number of specs/kill = {sum(num_specs)/len(num_specs)}')
print('************************************************************\n')

# useful for when seercull is rolling a random number ... gives you the idea of the potential but tbh I think it's more about shadow rng than seercull
if seercull:
    low_ttk_seercull_hits = []
    best_ttks = []
    for n, t in enumerate(ttk_ticks):
        if t < sum(ttk_ticks)/len(ttk_ticks) * (1-.3413):  # if it's over 1 standard deviation lower than the mean...
            print(f'Seercull hit a {seercull_hits[n]} and the kill took {t} ticks ({round(t*0.6, 2)} seconds)')
            low_ttk_seercull_hits.append(seercull_hits[n])
            best_ttks.append(t)

    average_sc = sum(low_ttk_seercull_hits)/len(low_ttk_seercull_hits)
    average_best_ttks = sum(best_ttks)/len(best_ttks)
    print(f'Best times had an average seercull hit of {average_sc} and an average ttk of {average_best_ttks} ({average_best_ttks * 0.6} seconds)')

    print(f'The average time was {round(sum(ttk_ticks)/len(ttk_ticks), 2)} ticks')




