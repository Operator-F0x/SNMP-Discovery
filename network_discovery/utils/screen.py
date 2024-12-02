from screeninfo import get_monitors

def get_screen_size():
    """
    Get the size of the primary monitor in pixels.

    This function retrieves the width and height of the primary monitor
    using the `get_monitors` function from the `screeninfo` module.

    Returns:
        tuple: A tuple containing the width and height of the primary monitor in pixels.

    Example:
        >>> width, height = get_screen_size()
        >>> print(f"Width: {width}, Height: {height}")
        Width: 1920, Height: 1080
    """
    monitor = get_monitors()[0]
    width_px = monitor.width
    height_px = monitor.height
    return width_px, height_px