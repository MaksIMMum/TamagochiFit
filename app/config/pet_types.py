"""Pet type definitions and evolution paths."""
from typing import Dict, List

PET_TYPES = {
    "cherry": {
        "name": "Cherry Pet",
        "emoji": "🍒",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/cherry/cherry egg.png"},
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/cherry/cherry newborn.png"},
            3: {"species": "kid", "emoji": "🐤", "image": "/static/images/characters/cherry/cherry kid.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/cherry/cherry teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/cherry/cherry adult.png"},
        }
    },
    "cyan": {
        "name": "Cyan Pet",
        "emoji": "🔷",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/cyan/cyan egg.png"},
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/cyan/cyan newborn.png"},
            3: {"species": "child", "emoji": "🐤", "image": "/static/images/characters/cyan/cyan child.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/cyan/cyan teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/cyan/cyan adult.png"},
        }
    },
    "dark_blue": {
        "name": "Dark Blue Pet",
        "emoji": "🔵",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/dark blue/dark blue egg.png"},
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/dark blue/dark blue newborn.png"},
            3: {"species": "child", "emoji": "🐤", "image": "/static/images/characters/dark blue/dark blue child.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/dark blue/dark blue teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/dark blue/dark blue adult.png"},
        }
    },
    "green": {
        "name": "Green Pet",
        "emoji": "🟢",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/green/green egg.png"},
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/green/green newborn.png"},
            3: {"species": "child", "emoji": "🐤", "image": "/static/images/characters/green/green child.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/green/green teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/green/green adult.png"},
        }
    },
    "purple": {
        "name": "Purple Pet",
        "emoji": "🟣",
        "evolution_chain": {
            1: {"species": "egg", "emoji": "🥚", "image": "/static/images/characters/purple/purple egg.png"},
            2: {"species": "newborn", "emoji": "🐣", "image": "/static/images/characters/purple/purple newborn.png"},
            3: {"species": "child", "emoji": "🐤", "image": "/static/images/characters/purple/purple child.png"},
            5: {"species": "teen", "emoji": "🐦", "image": "/static/images/characters/purple/purple teen.png"},
            8: {"species": "adult", "emoji": "🦅", "image": "/static/images/characters/purple/purple adult.png"},
        }
    },
}

def get_pet_type(pet_type_id: str) -> Dict:
    """Get pet type config by ID. Raises ValueError if not found."""
    if pet_type_id not in PET_TYPES:
        raise ValueError(f"Unknown pet type: {pet_type_id}")
    return PET_TYPES[pet_type_id]

def get_all_pet_types() -> List[Dict]:
    """Return list of all available pet types with basic info."""
    return [
        {
            "id": key,
            "name": value["name"],
            "emoji": value["emoji"],
            "preview_image": value.get("evolution_chain", {}).get(3, {}).get("image", ""),
            "evolution_chain": value["evolution_chain"]
        }
        for key, value in PET_TYPES.items()
    ]

def get_species_for_level(pet_type_id: str, level: int) -> Dict:
    """
    Get the species, emoji, and image for a given pet type at a specific level.
    Returns {"species": str, "emoji": str, "image": str}
    """
    pet_type = get_pet_type(pet_type_id)
    evolution_chain = pet_type["evolution_chain"]

    current_species = None
    for level_threshold in sorted(evolution_chain.keys()):
        if level >= level_threshold:
            current_species = evolution_chain[level_threshold]

    return current_species or evolution_chain[1]
