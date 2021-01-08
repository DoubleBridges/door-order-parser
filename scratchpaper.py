"""
class JobDetails(
    job_name: str,
    date: str,
    door_style: {
        name: str,
        species: str,
        outside_prifle: str,
        inside_profile: str,
        panel_profile: str,
        panel_shape: str,
        total: int,
        applied_and_finished_ends: [
            {
                qty: int,
                width: int,
                height: int,
            },
            ...
        ],
        doors: [
            {
                qty: int,
                width: int,
                height: int,
            },
            ...
        ],
        drawers: [
            {
                qty: int,
                width: int,
                height: int,
            },
            ...
        ],
    }
)
"""
