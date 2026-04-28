def compare_hashes(hashes1, hashes2):
    if not hashes1 or not hashes2:
        return 0   # ✅ prevent crash

    distances = []

    for h1 in hashes1:
        for h2 in hashes2:
            distances.append(h1 - h2)

    if not distances:
        return 0   # extra safety

    best = min(distances)
    similarity = (1 - best / 64) * 100

    return similarity