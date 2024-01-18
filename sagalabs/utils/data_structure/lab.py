"""
    Represents a lab, which is a collection of entities
"""
class Lab:
    """
        Represents a lab, which is a collection of entities
    """
    def __init__(self, name, entity_json, entity_state_json):

        def get_state():
            if len(entity_state_json) == 0:
                return "Undefined"

            try:
                is_all_running = all(entity["running"] for entity in entity_state_json)
                is_no_running = all(not entity["running"] for entity in entity_state_json)
            except KeyError:
                return "Undefined"

            if is_all_running:
                return "Online"
            elif is_no_running:
                return "Offline"
            else:
                return "Unhealthy"

        def get_state_color_class(state):
            if state == "Online":
                return "text-success"
            elif state == "Offline":
                return "text-danger"
            elif state == "Unhealthy":
                return "text-warning"
            elif state == "Undefined":
                return "text-secondary"
        
        def is_vpn_downloadable(state):
            return state == "Online" or state == "Unhealthy"

        def get_public_ip():
            for entity in entity_json:
                try:
                    if entity["type"] == 'Microsoft.Network/publicIPAddresses':
                        return entity["ip_address"]
                except KeyError:
                    pass
            return "Undefined"

        self.name = name
        self.state = get_state()
        self.state_color = get_state_color_class(self.state)
        self.is_vpn_downloadable = is_vpn_downloadable(self.state)
        self.public_ip = get_public_ip()
