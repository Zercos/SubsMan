from typing import Sequence


def chunk_generator(lst: Sequence, chunk_size: int) -> Sequence:
    """Generator which yields the chunks of sequential of specified size

    :param lst: An sequential object to divide into chunks
    :type lst: Sequence
    :param chunk_size: A size of one chunk
    :type chunk_size: int
    :return: An sequential object in size of chunk_size
    :rtype: Sequence
    """

    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]
