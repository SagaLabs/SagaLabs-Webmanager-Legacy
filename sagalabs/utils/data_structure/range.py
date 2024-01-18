"""
    Represents a range of labs
"""
class Range:
    """
        Represents a range of labs
    """

    def __init__(self, name, labs):

        def get_range_state():

            lab_amount = len(labs)
            def is_lab_running(lab):
                return lab.state == 'Online' or lab.state == 'Unhealthy'
            running_lab_amount = sum(is_lab_running(lab) for lab in labs )


            if lab_amount == 0 or running_lab_amount == 0:
                return ('Offline', 'text-danger')
            elif lab_amount == running_lab_amount:
                return ('Online', 'text-success')
            else:
                return (f'{running_lab_amount}/{lab_amount} Online', 'text-warning')

        (self.state_text, self.state_color) = get_range_state()
        self.name = name
        self.labs = labs
