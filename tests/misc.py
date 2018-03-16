from core.simulation.model.server_selection_rule import SelectionRule

if __name__ == "__main__":
    for ssr in SelectionRule:
        print(ssr.name)