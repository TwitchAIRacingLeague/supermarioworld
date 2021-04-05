import retro
from datetime import datetime
import time
import random
import itertools
import time
import gzip


def get_all_pairwise_actions(possible_actions):
    groupings = []
    for each in itertools.permutations(possible_actions.keys(),2):
        groupings.append(possible_actions[each[0]] + possible_actions[each[1]])
    return groupings

def dash(possible_actions, direction, taps):
    set_of_actions = []
    for i in range(taps):
        set_of_actions.append(possible_actions[direction] + possible_actions["B"])
    return set_of_actions

def run(possible_actions, direction, run_distance):
    set_of_actions = []
    for i in range(run_distance):
        set_of_actions.append(possible_actions[direction])
    return set_of_actions

def jump(possible_actions, direction, jump_duration):
    set_of_actions = []

    set_of_actions.append(possible_actions["A"])
    set_of_actions.append(possible_actions["A"])
    set_of_actions.append(possible_actions["A"])
    for i in range(jump_duration):
        set_of_actions.append(possible_actions["A"] + possible_actions[direction])
       # set_of_actions.append(possible_actions[direction])

    return set_of_actions

def shoot(possible_actions, direction, jump_duration):
    set_of_actions = []

    set_of_actions.append(possible_actions[direction])
    for i in range(jump_duration):
        set_of_actions.append(possible_actions["X"])
       # set_of_actions.append(possible_actions[direction])

    return set_of_actions

def actions_available(possible_actions):
    #https://info.sonicretro.org/index.php?title=File:Sonic2_MD_US_manual.pdf&page=7

    x = {"run_left_X_frames" : run(possible_actions, "LEFT", 100), # This could be a variable amount of running
         "run_left_Y_frames" : run(possible_actions, "LEFT", 200), # This could be a variable amount of running
         "run_right_X_frames" : run(possible_actions, "RIGHT", 100), # This could be a variable amount of running
         "run_right_Y_frames" : run(possible_actions, "RIGHT", 200), # This could be a variable amount of running
         "dash_right_X_times" : dash(possible_actions, "RIGHT", 100),
         "dash_left_X_times" : dash(possible_actions, "LEFT", 100),
         "jump_right_X_frames" : jump(possible_actions, "RIGHT", 50),
         "jump_left_X_frames" : jump(possible_actions, "LEFT", 50),
         "shoot_left_frames" : shoot(possible_actions, "LEFT", 10),
         "shoot_left_frames" : shoot(possible_actions, "RIGHT", 10),
         #"jump_up_X_frames" : jump(possible_actions, "RIGHT", 5),
         
     }
    return x[list(x.keys())[random.randint(0,len(x.keys())-1)]]

def save_state_to_file(env, name="test.state"):
    
    content = env.em.get_state()
    with gzip.open(name, 'wb') as f:
        f.write(content)

def main():

    actions_by_value = {"B" : 2**12, "Y" : 2**11, "SELECT" : 2**9, "START" : 2**8, "UP" : 2**7, "DOWN" : 2**6, "LEFT" : 2**5, "RIGHT" : 2**4, "A" : 2**3, "X" : 2**2, "L" : 2**1, "R" : 2**0} # "MODE" : 2**9
    # Experiment with making an example like actions_by_value with snes
    env = retro.make(game='SuperMarioWorld-Snes')
    obs = env.reset()

    # ["B", "Y", "SELECT", "START", "UP", "DOWN", "LEFT", "RIGHT", "A", "X", "L", "R"],
    # START: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    # Do Nothing [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # "A" [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]

    while True:
        action_sequence = actions_available(actions_by_value)
        for i in action_sequence:
            binary_value = str(bin(i))
            binary_value = ''.join(list(binary_value)[2:])
            action = list(map(int,list(str(binary_value).zfill(12))))
            obs, rew, done, info = env.step(action)
            env.render()
            

            time.sleep(1.0/60.0)
            
            #if done:
                #print ("DONE?")
                #if info["lives"] != 0:
                #    print ("bdone", done)
                #    print (info)
                #    print (rew)
                #    #print ("WHAT???")
                #    #input()
                #    #level_index += 1
                #    env.close()
                #    env = retro.make(game='SuperMarioWorld-Snes', state="VanillaDome1")
                #obs = env.reset()
                #continue
    env.close()


if __name__ == "__main__":
    main()

'''
/home/hotdog/.local/lib/python3.6/site-packages/retro/data/stable/SonicTheHedgehog2-Genesis/

contest.json
data.json
metadata.json
scenario.json
script.lua
xpos.json
'''