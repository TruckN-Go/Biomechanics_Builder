jump_shot_phases = ['flight','loading','propulsion']
icon_dict = dict()
for phases in jump_shot_phases:
    icon_dict[phases] = wheel.recolor_icons(os.path.join(os.getcwd(),'icons', 'jump_shot_' + phases + '.png'), graph_color)
