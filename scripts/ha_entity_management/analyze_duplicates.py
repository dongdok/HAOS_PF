import json
from collections import defaultdict

def analyze_duplicates():
    # Load the raw entity dump
    with open('ha_entities_dump.json', 'r', encoding='utf-8') as f:
        entities = json.load(f)
        
    print(f"Total Entities Loaded: {len(entities)}")
    
    # We will build a map of devices based on their base names
    # Heuristic: base names usually don't have _2 or _3.
    # We want to identify entities that have the same base name but different suffixes.
    
    base_name_map = defaultdict(list)
    
    for entity in entities:
        entity_id = entity.get('entity_id', '')
        state = entity.get('state', '')
        
        # We only care about active/available entities for disabling purposes,
        # but let's map them all first to see the structure.
        
        # Extract base name by removing common suffixes
        base_id = entity_id
        if base_id.endswith('_2'):
            base_id = base_id[:-2]
        elif base_id.endswith('_3'):
            base_id = base_id[:-2]
        
        base_name_map[base_id].append(entity)
        
    print(f"\nGrouping by base entity_id ({len(base_name_map)} unique base IDs):")
    
    duplicates_to_disable = []
    
    for base_id, group in base_name_map.items():
        if len(group) > 1:
            # We found a group with multiple entities sharing the same base name
            print(f"\n--- Base ID: {base_id} ---")
            for e in group:
                eid = e.get('entity_id')
                name = e.get('attributes', {}).get('friendly_name', 'Unknown')
                status = e.get('state')
                print(f"  - {eid} ({name}) | Status: {status}")
                
                # If it's a _2 or _3 and it's not already disabled (state != 'unavailable' or similar), 
                # we flag it for our action list.
                # Actually, in HA, 'disabled' entities might not appear in /api/states at all,
                # or they might have specific states. Let's assume if they are here, they might need disabling.
                if (eid.endswith('_2') or eid.endswith('_3')):
                    duplicates_to_disable.append({
                        'entity_id': eid,
                        'name': name,
                        'state': status
                    })
                    
    print(f"\nTarget Entities to Disable (Total: {len(duplicates_to_disable)}):")
    for d in sorted(duplicates_to_disable, key=lambda x: x['entity_id']):
        print(f" - {d['entity_id']} ({d['name']})")
        
    # Save the target list to a file for review
    with open('targets_to_disable.json', 'w', encoding='utf-8') as f:
        json.dump(duplicates_to_disable, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    analyze_duplicates()
