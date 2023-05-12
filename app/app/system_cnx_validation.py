################################### System connections validation ###################################
class Validation():
    @staticmethod
    def validate_system_connections(component_list):
        continuity_check = False
        used = []
        unused = []
        for component in component_list:
            unused.append(component.terminals)
        terminal_pair_count = len(unused)
        used.append(unused[0])
        unused.remove(unused[0])

        for used_pair in used:
            for used_pair_terminal in used_pair:
                if used_pair_terminal != 0:
                    for unused_pair in unused:
                        if used_pair_terminal in unused_pair:
                            used.append(unused_pair)
                            unused.remove(unused_pair)
                            break
            if len(used) == terminal_pair_count:
                continuity_check = True
                break
        return continuity_check

