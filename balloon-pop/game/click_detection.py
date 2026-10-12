"""
Click detection for balloon hits.
"""


def check_pop(balloons, click_pos):
    """Return the balloon that was clicked, or None if no hit is found."""
    if click_pos is None:
        return None

    click_x, click_y = click_pos

    # Check the most recently drawn balloon first so overlapping balloons
    # behave naturally and the hit test matches the visible circle.
    for balloon in reversed(balloons):
        dx = click_x - balloon.x
        dy = click_y - balloon.y
        distance_squared = dx * dx + dy * dy
        radius_squared = balloon.radius * balloon.radius

        if distance_squared <= radius_squared:
            return balloon

    return None